from django.contrib import admin

from .models import DocumentType


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "fee_rs", "processing_days", "is_active"]
    list_filter = ["is_active"]
    prepopulated_fields = {"slug": ("name",)}
