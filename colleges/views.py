from django.shortcuts import render

from .models import College


def college_list(request):
    colleges = College.objects.all()
    return render(request, "colleges/list.html", {"colleges": colleges})
