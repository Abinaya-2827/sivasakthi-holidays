from django.shortcuts import render
from .models import Package

# Category-level copy from the brief — one description/icon per tour
# type, not per individual Package row (a park could have several
# Family Tour packages that all share this description).
TOUR_TYPE_INFO = {
    "Family Tour": {
        "icon": "bi-people-fill",
        "description": "Comfortable family vacations with sightseeing, hotels, transport, and fun activities suitable for all ages.",
    },
    "Corporate Tour": {
        "icon": "bi-briefcase-fill",
        "description": "Professional company outings, employee trips, team-building events, conferences, and business travel.",
    },
    "Temple Tour": {
        "icon": "bi-building",
        "description": "Pilgrimage packages covering famous temples with comfortable transport and accommodation.",
    },
    "Friends Tour": {
        "icon": "bi-people",
        "description": "Adventure-filled group trips for college friends and young travelers with sightseeing and entertainment.",
    },
    "Weekend Getaway": {
        "icon": "bi-compass",
        "description": "Short 1–3 day trips to nearby hill stations, waterfalls, beaches, and scenic destinations.",
    },
    "Honeymoon Tour": {
        "icon": "bi-heart-fill",
        "description": "Romantic honeymoon packages with luxury stays, candlelight dinners, scenic destinations, and couple experiences.",
    },
}


def _is_complete(p):
    """A package card is only shown once it has everything it needs to
    render properly: a real image, a valid/known category, and the core
    text fields. This keeps stale or half-filled rows (e.g. leftover
    from an old seed run, or a package started in admin but not
    finished) from ever showing up as an empty/broken card."""
    if p.tour_type not in TOUR_TYPE_INFO:
        return False
    if not p.image:
        return False
    if not p.destination_text.strip() or not p.duration.strip():
        return False
    if not p.facilities_list():
        return False
    return True


def package_list(request):
    packages = Package.objects.filter(is_active=True)
    tour_type = request.GET.get("type", "")

    if tour_type:
        packages = packages.filter(tour_type=tour_type)

    packages = [p for p in packages if _is_complete(p)]
    for p in packages:
        info = TOUR_TYPE_INFO[p.tour_type]
        p.icon = info["icon"]
        p.description = info["description"]

    return render(request, "package_list.html", {
        "packages": packages,
        "tour_types": Package.TOUR_TYPES,
        "selected_type": tour_type,
    })
