from django.contrib import admin
from .models import HeroSlide, Testimonial, ContactMessage, PaymentProof, WhyChooseUs


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "rating", "is_active", "submitted_on")
    list_editable = ("is_active",)
    list_filter = ("is_active", "rating")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "submitted_on", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    readonly_fields = ("name", "phone", "email", "message", "submitted_on")


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "note", "uploaded_on", "is_verified")
    list_editable = ("is_verified",)
    list_filter = ("is_verified",)


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
