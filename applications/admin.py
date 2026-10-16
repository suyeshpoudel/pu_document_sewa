from django.contrib import admin

from .models import Application, ApplicationFile, Payment, Shipment


class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "document_type", "status", "created_at"]
    list_filter = ["status", "document_type"]
    search_fields = ["full_name", "symbol_no", "reg_no", "tracking_no"]
    inlines = [ApplicationFileInline, PaymentInline]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "application", "courier", "tracking_id", "status"]
