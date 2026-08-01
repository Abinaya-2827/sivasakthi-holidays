import re
from collections import OrderedDict

from django.shortcuts import render

from .models import GalleryImage

# Trailing " 1", " 2", etc. groups multiple photos from the same trip
# into one album (e.g. "Group trip 1".."Group trip 4" -> "Group Trip",
# 4 photos). A caption with no trailing number is its own 1-photo album.
_TRAILING_NUMBER = re.compile(r"\s*\d+\s*$")

# Optional hand-written blurbs for specific albums. Anything not listed
# here falls back to a generic photo-count description automatically.
ALBUM_DESCRIPTIONS = {
    "Group Trip": "Snapshots from one of our group tours — good roads, better company.",
    "Family Group Tour": "A joyful multi-family group trip, from ghat-road stops to a two-bus convoy on the hills.",
    "College Group Tour": "College friends on the road — a decorated night stop, misty hill roads, and playful countryside photo breaks.",
    "Forest Route Group Photo": "A scenic forest route, captured mid-journey.",
    "Santa Monica Tours Group": "Another happy group, another great trip with us.",
}


def _album_name(caption):
    """'Group trip 1' -> 'Group Trip'. 'Sunset Beach' -> 'Sunset Beach'."""
    stripped = _TRAILING_NUMBER.sub("", caption or "").strip()
    stripped = stripped or "Trip Photos"
    return " ".join(word.capitalize() for word in stripped.split())


def gallery(request):
    images = GalleryImage.objects.exclude(image="").order_by("-uploaded_on")

    # Group by normalized album name, independent of queryset ordering
    # (a dict keeps this correct even if captions aren't pre-sorted).
    grouped = OrderedDict()
    for img in images:
        grouped.setdefault(_album_name(img.caption), []).append(img)

    albums = []
    for album_name, photos in grouped.items():
        albums.append({
            "name": album_name,
            "cover": photos[0],
            "photos": photos,
            "count": len(photos),
            "description": ALBUM_DESCRIPTIONS.get(
                album_name, f"{len(photos)} photo{'s' if len(photos) != 1 else ''} from this trip."
            ),
        })

    # Most-photos-first so the fullest albums lead the page.
    albums.sort(key=lambda a: a["count"], reverse=True)

    return render(request, "gallery.html", {"albums": albums})
