from django.shortcuts import render

from catalog.models import DocumentType
from config.pricing import MINIMUM_SERVICE_FEE_RS


def landing(request):
    active = DocumentType.objects.filter(is_active=True)
    return render(
        request,
        "pages/landing.html",
        {
            "document_types": active[:6],
            "service_fee": MINIMUM_SERVICE_FEE_RS,
        },
    )
