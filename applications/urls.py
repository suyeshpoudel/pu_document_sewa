from django.urls import path

from . import views

urlpatterns = [
    path("apply/", views.ApplyView.as_view(), name="apply"),
    path("apply/<int:document_type_id>/", views.ApplyView.as_view(), name="apply_for"),
    path("mine/", views.MyApplicationsView.as_view(), name="my_applications"),
    path("<int:pk>/", views.ApplicationDetailView.as_view(), name="application_detail"),
    path("<int:pk>/cancel/", views.cancel_application, name="cancel_application"),
    path("admin/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path(
        "admin/<int:pk>/", views.AdminApplicationDetailView.as_view(), name="admin_application_detail"
    ),
    path(
        "admin/<int:pk>/status/", views.AdminStatusUpdateView.as_view(), name="admin_status_update"
    ),
]
