from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("tour_type", "destination_text", "duration", "starting_price", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("tour_type", "is_active")
