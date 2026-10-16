from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.decorators.http import require_POST

from accounts.models import Role

from .forms import ApplicationFileForm, ApplicationForm, StatusUpdateForm
from .models import Application, ApplicationFile, ApplicationStatus


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.role in (Role.ADMIN, Role.COLLEGE_STAFF)


def _handle_files(application, file_type, files):
    for f in files or []:
        ApplicationFile.objects.create(application=application, file_type=file_type, file=f)


class ApplyView(LoginRequiredMixin, View):
    template_name = "applications/apply.html"

    def get(self, request, document_type_id=None):
        initial = {}
        if document_type_id:
            initial["document_type"] = document_type_id
        form = ApplicationForm(initial=initial)
        file_form = ApplicationFileForm()
        return render(
            request,
            self.template_name,
            {"form": form, "file_form": file_form},
        )

    def post(self, request, document_type_id=None):
        form = ApplicationForm(request.POST)
        file_form = ApplicationFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                application = form.save(commit=False)
                application.student = request.user
                application.status = ApplicationStatus.SUBMITTED
                application.save()
                _handle_files(
                    application,
                    file_form.cleaned_data["file_type"],
                    file_form.cleaned_data.get("files"),
                )
            messages.success(request, "Application submitted successfully.")
            return redirect("application_detail", pk=application.pk)
        elif form.is_valid() and not file_form.is_valid():
            messages.error(request, "Please fix the errors in the uploaded files.")
        return render(
            request,
            self.template_name,
            {"form": form, "file_form": file_form},
        )


class MyApplicationsView(LoginRequiredMixin, ListView):
    template_name = "applications/mine.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).select_related(
            "document_type", "college"
        )


class ApplicationDetailView(LoginRequiredMixin, View):
    template_name = "applications/detail.html"

    def get(self, request, pk):
        application = get_object_or_404(
            Application.objects.select_related(
                "document_type", "college", "student", "shipment"
            ).prefetch_related("files", "payments"),
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
    if application.status in (
        ApplicationStatus.SUBMITTED,
        ApplicationStatus.UNDER_REVIEW,
        ApplicationStatus.DRAFT,
    ):
        application.status = ApplicationStatus.CANCELLED
        application.save(update_fields=["status", "updated_at"])
        messages.success(request, "Application cancelled.")
    else:
        messages.error(request, "This application can no longer be cancelled.")
    return redirect("application_detail", pk=pk)


class AdminDashboardView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = "applications/dashboard.html"
    context_object_name = "applications"

    def get_queryset(self):
        qs = Application.objects.select_related(
            "document_type", "student", "college"
        ).prefetch_related("files")
        status = self.request.GET.get("status")
        if status and status in ApplicationStatus.values:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = ApplicationStatus.choices
        ctx["current_status"] = self.request.GET.get("status", "")
        return ctx


class AdminStatusUpdateView(LoginRequiredMixin, StaffRequiredMixin, View):
    template_name = "applications/status_update.html"

    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        form = StatusUpdateForm(instance=application)
        return render(
            request, self.template_name, {"application": application, "form": form}
        )

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        form = StatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application #{application.pk} updated.")
            return redirect("admin_application_detail", pk=application.pk)
        return render(
            request, self.template_name, {"application": application, "form": form}
        )


class AdminApplicationDetailView(LoginRequiredMixin, StaffRequiredMixin, View):
    template_name = "applications/admin_detail.html"

    def get(self, request, pk):
        application = get_object_or_404(
            Application.objects.select_related(
                "document_type", "college", "student", "shipment"
            ).prefetch_related("files", "payments"),
            pk=pk,
        )
        return render(request, self.template_name, {"application": application})
