from django.contrib import admin

from .models import College


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "district", "contact_phone"]
    search_fields = ["name", "code", "district"]
