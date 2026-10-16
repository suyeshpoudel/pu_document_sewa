from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from accounts.models import Role
from applications.models import Application, ApplicationStatus
from catalog.models import DocumentType
from colleges.models import College

from .forms import OfficeCollegeForm, OfficeDocumentForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.role == Role.ADMIN


class OfficeSectionMixin:
    office_section = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["office_section"] = self.office_section
        return ctx


class OfficeOverviewView(AdminRequiredMixin, OfficeSectionMixin, TemplateView):
    template_name = "office/overview.html"
    office_section = "overview"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apps = Application.objects.all()
        ctx["stat_pending"] = apps.filter(
            status__in=[ApplicationStatus.SUBMITTED, ApplicationStatus.RECEIPT_VERIFIED]
        ).count()
        ctx["stat_collecting"] = apps.filter(status=ApplicationStatus.COLLECTING).count()
        ctx["stat_dispatched"] = apps.filter(status=ApplicationStatus.DISPATCHED).count()
        ctx["stat_delivered"] = apps.filter(status=ApplicationStatus.DELIVERED).count()
        ctx["stat_total"] = apps.count()
        ctx["stat_documents"] = DocumentType.objects.count()
        ctx["stat_colleges"] = College.objects.count()
        ctx["recent_applications"] = apps.select_related("document_type", "student")[:10]
        return ctx


class OfficeDocumentListView(AdminRequiredMixin, OfficeSectionMixin, ListView):
    template_name = "office/documents.html"
    context_object_name = "documents"
    queryset = DocumentType.objects.prefetch_related("includes")
    office_section = "documents"


class OfficeDocumentCreateView(AdminRequiredMixin, OfficeSectionMixin, CreateView):
    model = DocumentType
    form_class = OfficeDocumentForm
    template_name = "office/document_form.html"
    success_url = reverse_lazy("office_documents")
    office_section = "documents"

    def form_valid(self, form):
        messages.success(self.request, f"Document “{form.cleaned_data['name']}” added.")
        return super().form_valid(form)


class OfficeDocumentUpdateView(AdminRequiredMixin, OfficeSectionMixin, UpdateView):
    model = DocumentType
    form_class = OfficeDocumentForm
    template_name = "office/document_form.html"
    success_url = reverse_lazy("office_documents")
    office_section = "documents"

    def form_valid(self, form):
        messages.success(self.request, f"Document “{form.cleaned_data['name']}” updated.")
        return super().form_valid(form)


class OfficeDocumentDeleteView(AdminRequiredMixin, OfficeSectionMixin, DeleteView):
    model = DocumentType
    template_name = "office/document_delete.html"
    success_url = reverse_lazy("office_documents")
    office_section = "documents"

    def form_valid(self, form):
        name = self.object.name
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Cannot delete “{name}” — existing applications reference it.",
            )
            return redirect("office_documents")
        messages.success(self.request, f"Document “{name}” deleted.")
        return response


class OfficeCollegeListView(AdminRequiredMixin, OfficeSectionMixin, ListView):
    template_name = "office/colleges.html"
    context_object_name = "colleges"
    queryset = College.objects.all()
    office_section = "colleges"


class OfficeCollegeCreateView(AdminRequiredMixin, OfficeSectionMixin, CreateView):
    model = College
    form_class = OfficeCollegeForm
    template_name = "office/college_form.html"
    success_url = reverse_lazy("office_colleges")
    office_section = "colleges"

    def form_valid(self, form):
        messages.success(self.request, f"College “{form.cleaned_data['name']}” added.")
        return super().form_valid(form)


class OfficeCollegeUpdateView(AdminRequiredMixin, OfficeSectionMixin, UpdateView):
    model = College
    form_class = OfficeCollegeForm
    template_name = "office/college_form.html"
    success_url = reverse_lazy("office_colleges")
    office_section = "colleges"

    def form_valid(self, form):
        messages.success(self.request, f"College “{form.cleaned_data['name']}” updated.")
        return super().form_valid(form)


class OfficeCollegeDeleteView(AdminRequiredMixin, OfficeSectionMixin, DeleteView):
    model = College
    template_name = "office/college_delete.html"
    success_url = reverse_lazy("office_colleges")
    office_section = "colleges"

    def form_valid(self, form):
        name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, f"College “{name}” deleted.")
        return response


class OfficeApplicationListView(AdminRequiredMixin, OfficeSectionMixin, ListView):
    template_name = "office/applications.html"
    context_object_name = "applications"
    office_section = "applications"

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
