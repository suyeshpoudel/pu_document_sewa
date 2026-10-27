from django.shortcuts import get_object_or_404, render

from config.pricing import MINIMUM_SERVICE_FEE_RS

from .models import DocumentType


def document_list(request):
    docs = DocumentType.objects.filter(is_active=True)
    return render(
        request,
        "catalog/list.html",
        {
            "document_types": docs,
            "minimum_service_fee": MINIMUM_SERVICE_FEE_RS,
        },
    )


def document_detail(request, slug):
    doc = get_object_or_404(DocumentType, slug=slug, is_active=True)
    return render(request, "catalog/detail.html", {"doc": doc})
