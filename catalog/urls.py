from django.urls import path

from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("<slug:slug>/", views.document_detail, name="document_detail"),
]
