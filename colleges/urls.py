from django.urls import path

from . import views

urlpatterns = [
    path("", views.college_list, name="college_list"),
]
