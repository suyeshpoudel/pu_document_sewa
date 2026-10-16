from django.urls import path

from . import views

urlpatterns = [
    path("", views.OfficeOverviewView.as_view(), name="office_home"),
    path("documents/", views.OfficeDocumentListView.as_view(), name="office_documents"),
    path("documents/new/", views.OfficeDocumentCreateView.as_view(), name="office_document_create"),
    path(
        "documents/<int:pk>/edit/",
        views.OfficeDocumentUpdateView.as_view(),
        name="office_document_update",
    ),
    path(
        "documents/<int:pk>/delete/",
        views.OfficeDocumentDeleteView.as_view(),
        name="office_document_delete",
    ),
    path("colleges/", views.OfficeCollegeListView.as_view(), name="office_colleges"),
    path("colleges/new/", views.OfficeCollegeCreateView.as_view(), name="office_college_create"),
    path(
        "colleges/<int:pk>/edit/",
        views.OfficeCollegeUpdateView.as_view(),
        name="office_college_update",
    ),
    path(
        "colleges/<int:pk>/delete/",
        views.OfficeCollegeDeleteView.as_view(),
        name="office_college_delete",
    ),
    path("applications/", views.OfficeApplicationListView.as_view(), name="office_applications"),
]
