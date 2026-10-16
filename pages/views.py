from django.shortcuts import render

from catalog.models import DocumentType


def landing(request):
    active = DocumentType.objects.filter(is_active=True)
    service_fee = active.values_list("fee_rs", flat=True).first() or 500
    return render(
        request,
        "pages/landing.html",
        {
            "document_types": active[:6],
            "service_fee": service_fee,
        },
    )
