from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_popular", "is_local_tamilnadu", "order")
    list_editable = ("is_popular", "is_local_tamilnadu", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
