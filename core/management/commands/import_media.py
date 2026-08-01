"""
Self-service image importer.

Drop your real photos into the folders below (create them if they
don't exist yet), then run:

    python manage.py import_media

media_imports/
    destinations/   one image per destination — filename must match
                     the destination NAME (spaces or dashes both work,
                     case-insensitive). e.g. "Kerala.jpg", "kodaikanal.png",
                     "all-local-tamil-nadu-tours.jpg"
    packages/        one image per package type — filename must match
                     the TOUR TYPE. e.g. "Family Tour.jpg", "temple-tour.png"
    hero/            any number of images — each becomes a new hero
                     slide (title = the filename, cleaned up)
    gallery/         any number of images — each becomes a new gallery
                     photo (caption = the filename, cleaned up)

Matching is fuzzy: "kodai-kanal.jpg", "Kodaikanal.PNG", and
"KODAIKANAL.jpg" all match the "Kodaikanal" destination. Any file
that doesn't match an existing destination/package name is reported
and skipped (with a suggestion) rather than silently ignored.

Already-imported gallery/hero images are not re-added on a second
run — matched by filename, so re-running is always safe.

Logo and bus photos are NOT handled here (they're static files, not
database images) — see README.md for how to replace those directly.
"""
import re
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from destinations.models import Destination
from packages.models import Package
from gallery.models import GalleryImage
from core.models import HeroSlide

BASE_IMPORT_DIR = Path("media_imports")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def normalize(text):
    """Lowercase, strip everything but letters/numbers, for fuzzy matching."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def humanize(filename):
    """'family-tour_final.jpg' -> 'Family Tour Final'"""
    stem = Path(filename).stem
    words = re.split(r"[-_]+", stem)
    return " ".join(w.capitalize() for w in words if w)


class Command(BaseCommand):
    help = "Import real photos from media_imports/ into destinations, packages, gallery, and hero slides."

    def handle(self, *args, **options):
        if not BASE_IMPORT_DIR.exists():
            self.stdout.write(self.style.WARNING(
                f"No '{BASE_IMPORT_DIR}/' folder found. Create it with "
                "destinations/, packages/, hero/, and gallery/ subfolders, "
                "add your images, then run this command again."
            ))
            return

        self._import_matched(BASE_IMPORT_DIR / "destinations", Destination, "name")
        self._import_matched(BASE_IMPORT_DIR / "packages", Package, "tour_type")
        self._import_new(BASE_IMPORT_DIR / "hero", HeroSlide, "title")
        self._import_new(BASE_IMPORT_DIR / "gallery", GalleryImage, "caption")

    def _image_files(self, folder):
        if not folder.exists():
            return []
        return sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS)

    def _import_matched(self, folder, model, name_field):
        """For destinations/packages: match filename to an existing row by name and replace its image."""
        files = self._image_files(folder)
        if not files:
            return

        existing = {normalize(getattr(obj, name_field)): obj for obj in model.objects.all()}

        for path in files:
            key = normalize(path.stem)
            obj = existing.get(key)
            if not obj:
                self.stdout.write(self.style.WARNING(
                    f"  Skipped {path.name} — no {model.__name__} named "
                    f"'{humanize(path.name)}'. Check spelling, or add it "
                    f"in the admin panel first."
                ))
                continue

            with open(path, "rb") as f:
                obj.image.save(path.name, File(f), save=True)
            self.stdout.write(self.style.SUCCESS(f"  Updated {model.__name__}: {getattr(obj, name_field)}"))

    def _import_new(self, folder, model, name_field):
        """For hero/gallery: every file becomes a new row, skipped if already imported by filename."""
        files = self._image_files(folder)
        if not files:
            return

        already = set(model.objects.values_list(name_field, flat=True))

        for path in files:
            label = humanize(path.name)
            if label in already:
                continue

            obj = model(**{name_field: label})
            with open(path, "rb") as f:
                obj.image.save(path.name, File(f), save=False)
            obj.save()
            self.stdout.write(self.style.SUCCESS(f"  Added {model.__name__}: {label}"))
