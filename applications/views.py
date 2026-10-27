from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, RedirectView
from django.views.decorators.http import require_POST

from accounts.models import Role
from config.pricing import MINIMUM_SERVICE_FEE_RS, minimum_service_fee

from .forms import ApplicationForm, StatusUpdateForm
from .models import Application, ApplicationStatus, Shipment


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.role == Role.ADMIN


class ApplyView(LoginRequiredMixin, View):
    template_name = "applications/apply.html"

    def get(self, request, document_type_id=None):
        initial = {
            "full_name": request.user.name,
            "phone": request.user.phone,
            "college": request.user.college_id,
        }
        if document_type_id:
            initial["document_type"] = document_type_id
        form = ApplicationForm(initial=initial)
        return render(
            request,
            self.template_name,
            {"form": form, "minimum_service_fee": MINIMUM_SERVICE_FEE_RS},
        )

    def post(self, request, document_type_id=None):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                application = form.save(commit=False)
                application.student = request.user
                application.status = ApplicationStatus.SUBMITTED
                application.service_fee_rs = minimum_service_fee(
                    application.document_type.fee_rs
                )
                application.save()
            messages.success(request, "Application submitted. We'll verify your receipt shortly.")
            return redirect("application_detail", pk=application.pk)
        return render(
            request,
            self.template_name,
            {"form": form, "minimum_service_fee": MINIMUM_SERVICE_FEE_RS},
        )


class MyApplicationsView(LoginRequiredMixin, ListView):
    template_name = "applications/mine.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).select_related(
            "document_type", "college"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        applications = ctx["applications"]
        ctx["total_count"] = len(applications)
        ctx["active_count"] = sum(
            1
            for application in applications
            if application.status
            not in (
                ApplicationStatus.DELIVERED,
                ApplicationStatus.REJECTED,
                ApplicationStatus.CANCELLED,
            )
        )
        ctx["delivered_count"] = sum(
            1
            for application in applications
            if application.status == ApplicationStatus.DELIVERED
        )
        return ctx


class ApplicationDetailView(LoginRequiredMixin, View):
    template_name = "applications/detail.html"

    def get(self, request, pk):
        application = get_object_or_404(
            Application.objects.select_related(
                "document_type", "college", "student", "shipment"
            ).prefetch_related("files"),
            pk=pk,
        )
        if request.user.role != Role.ADMIN and application.student_id != request.user.id:
            messages.error(request, "You do not have access to that application.")
            return redirect("my_applications")
        return render(request, self.template_name, {"application": application})


@login_required
@require_POST
def cancel_application(request, pk):
    application = get_object_or_404(Application, pk=pk, student=request.user)
    if application.cancelable:
        application.status = ApplicationStatus.CANCELLED
        application.save(update_fields=["status", "updated_at"])
        messages.success(request, "Application cancelled.")
    else:
        messages.error(request, "This application can no longer be cancelled.")
    return redirect("application_detail", pk=pk)


class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, RedirectView):
    pattern_name = "office_applications"
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        query = self.request.META.get("QUERY_STRING", "")
        url = super().get_redirect_url(*args, **kwargs)
        return f"{url}?{query}" if query else url


class AdminStatusUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "applications/status_update.html"

    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        form = StatusUpdateForm(instance=application)
        return render(
            request,
            self.template_name,
            {
                "application": application,
                "form": form,
                "minimum_service_fee": MINIMUM_SERVICE_FEE_RS,
            },
        )

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        form = StatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            with transaction.atomic():
                application = form.save()
                if application.status == ApplicationStatus.DISPATCHED:
                    Shipment.objects.update_or_create(
                        application=application,
                        defaults={
                            **form.shipment_data(),
                            "cod_amount_rs": application.service_fee_rs,
                        },
                    )
            messages.success(request, f"Application #{application.pk} updated.")
            return redirect("admin_application_detail", pk=application.pk)
        return render(
            request,
            self.template_name,
            {
                "application": application,
                "form": form,
                "minimum_service_fee": MINIMUM_SERVICE_FEE_RS,
            },
        )


class AdminApplicationDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "applications/admin_detail.html"

    def get(self, request, pk):
        application = get_object_or_404(
            Application.objects.select_related(
                "document_type", "college", "student", "shipment"
            ).prefetch_related("files"),
            pk=pk,
        )
        return render(request, self.template_name, {"application": application})
