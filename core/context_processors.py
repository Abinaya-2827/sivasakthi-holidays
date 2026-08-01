from django.conf import settings


def site_info(request):
    """Makes business contact details available in every template."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_PHONE": settings.SITE_PHONE,
        "SITE_WHATSAPP": settings.SITE_WHATSAPP,
        "SITE_EMAIL": settings.SITE_EMAIL,
        "SITE_INSTAGRAM": settings.SITE_INSTAGRAM,
        "SITE_ADDRESS": settings.SITE_ADDRESS,
        "SITE_UPI_ID": settings.SITE_UPI_ID,
    }
