from django.contrib import admin

from .models import Application, ApplicationFile, Shipment


class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "document_type",
        "urgency",
        "service_fee_rs",
        "pu_reference_no",
        "status",
        "created_at",
    ]
    list_filter = ["status", "document_type", "urgency"]
    search_fields = ["full_name", "pu_reference_no", "phone", "student__email"]
    inlines = [ApplicationFileInline]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "application", "courier", "tracking_id", "status"]
