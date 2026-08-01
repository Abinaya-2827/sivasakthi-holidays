"""
Seeds demo content (destinations, packages, hero slides, testimonials,
why-choose-us, gallery) using the placeholder images shipped in
static/images/, so the site looks complete before real photos are added.

Usage: python manage.py seed_site
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from destinations.models import Destination
from packages.models import Package
from core.models import HeroSlide, Testimonial, WhyChooseUs

IMAGES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "static" / "images"

DESTINATIONS = [
    ("Kerala", "God's Own Country — backwaters, hills, and beaches.", True, False),
    ("Goa", "Sun, sand, and a laid-back coastal vibe.", True, False),
    ("Kodaikanal", "A cool hill station with misty lakes and pine forests.", True, False),
    ("Ooty", "The Queen of Hill Stations, famous for its tea gardens.", True, False),
    ("Karnataka", "Palaces, temples, and the tech capital Bangalore.", False, False),
    ("Sabarimala", "A sacred pilgrimage destination in the Western Ghats.", False, False),
    ("Kutralam", "Famous for its natural waterfalls, the 'Spa of the South'.", False, True),
    ("Madurai", "Home to the iconic Meenakshi Amman Temple.", True, True),
    ("Rameswaram", "A holy island town with the Ramanathaswamy Temple.", False, True),
    ("Kanyakumari", "Where three seas meet at India's southern tip.", True, True),
    ("Thanjavur", "Home to the majestic Brihadeeswarar Temple.", False, True),
    ("Tiruchendur", "A coastal temple town devoted to Lord Murugan.", False, True),
    ("Yercaud", "A quiet hill station in the Shevaroy Hills.", False, False),
    ("Valparai", "Tea estates and wildlife in the Anamalai Hills.", False, False),
    ("Hogenakkal", "Known as the 'Niagara of India' for its waterfalls.", False, True),
    ("Courtallam", "Nine scenic waterfalls in the Western Ghats.", False, True),
    ("Coimbatore", "The gateway to the Nilgiris, a bustling city break.", False, True),
    ("Chennai", "Tamil Nadu's capital — culture, beaches, and food.", False, True),
    ("Tamil Nadu Tours", "All local Tamil Nadu tours, tailored to you.", False, True),
]

PACKAGES = [
    ("Family Tour", "Kerala, Ooty & Kodaikanal", "4 Days / 3 Nights", "AC Bus\nHotel Stay\nBreakfast & Dinner\nSightseeing"),
    ("Friends Tour", "Goa", "3 Days / 2 Nights", "AC/Non-AC Bus\nBudget Stay\nGroup Discounts\nLocal Guide"),
    ("Corporate Tour", "Coimbatore & Valparai", "2 Days / 1 Night", "Luxury Bus\nResort Stay\nTeam Activities\nMeals Included"),
    ("Temple Tour", "Madurai, Rameswaram & Kanyakumari", "3 Days / 2 Nights", "AC Bus\nLodge Stay\nEarly Darshan Assistance\nAll Meals"),
    ("Honeymoon Tour", "Kerala Backwaters", "4 Days / 3 Nights", "Private AC Vehicle\nHouseboat Stay\nCandlelight Dinner\nSightseeing"),
    ("Weekend Getaway", "Yercaud", "2 Days / 1 Night", "AC Bus\nHotel Stay\nBreakfast\nSightseeing"),
]

TESTIMONIALS = [
    ("Karthik R.", "Madurai", "Sivasakthi Holidays made our Kerala trip so smooth. Comfortable bus and a friendly driver!", 5),
    ("Priya S.", "Trichy", "Booked our college trip to Goa with them — great experience end to end.", 5),
    ("Anand & Divya", "Coimbatore", "Perfect honeymoon package. Everything was well organised.", 5),
    ("Meena K.", "Chennai", "Our temple tour to Rameswaram was peaceful and well planned.", 5),
]

WHY_CHOOSE_US = [
    ("bi-shield-check", "Safe & Comfortable", "Well-maintained buses and experienced, careful drivers."),
    ("bi-people", "Family Friendly", "Trusted by families, colleges, and corporate groups alike."),
    ("bi-award", "Years of Experience", "A track record of smooth, well-planned South India tours."),
    ("bi-headset", "Always Reachable", "Message us on WhatsApp anytime — we reply fast."),
]


class Command(BaseCommand):
    help = "Seed demo content using placeholder images."

    def _image(self, filename):
        path = IMAGES_DIR / filename
        return File(open(path, "rb")) if path.exists() else None

    def handle(self, *args, **options):
        created = 0

        for name, desc, popular, local in DESTINATIONS:
            if Destination.objects.filter(name=name).exists():
                continue
            fname = name.lower().replace(" ", "-") + ".jpg"
            d = Destination(name=name, short_description=desc, description=desc,
                             is_popular=popular, is_local_tamilnadu=local)
            img = self._image(fname)
            if img:
                d.image.save(fname, img, save=False)
            d.save()
            created += 1

        for tour_type, dest_text, duration, facilities in PACKAGES:
            if Package.objects.filter(tour_type=tour_type, destination_text=dest_text).exists():
                continue
            fname = "pkg-" + tour_type.lower().replace(" ", "-") + ".jpg"
            p = Package(tour_type=tour_type, destination_text=dest_text, duration=duration, facilities=facilities)
            img = self._image(fname)
            if img:
                p.image.save(fname, img, save=False)
            p.save()
            created += 1

        hero_data = [
            ("Explore South India With Us", "Family, college, corporate & temple tours — planned with care.", "hero1.jpg"),
            ("Comfortable Buses, Experienced Drivers", "Safe, smooth journeys across Tamil Nadu, Kerala & Karnataka.", "hero2.jpg"),
            ("Temple & Honeymoon Tours", "Sacred journeys and romantic getaways, planned end to end.", "hero3.jpg"),
        ]
        for title, subtitle, fname in hero_data:
            if HeroSlide.objects.filter(title=title).exists():
                continue
            s = HeroSlide(title=title, subtitle=subtitle)
            img = self._image(fname)
            if img:
                s.image.save(fname, img, save=False)
            s.save()
            created += 1

        for name, location, message, rating in TESTIMONIALS:
            if not Testimonial.objects.filter(name=name).exists():
                Testimonial.objects.create(name=name, location=location, message=message, rating=rating)
                created += 1

        for icon, title, desc in WHY_CHOOSE_US:
            if not WhyChooseUs.objects.filter(title=title).exists():
                WhyChooseUs.objects.create(icon=icon, title=title, description=desc)
                created += 1

        # NOTE: this command used to also seed 6 generic "Trip Photo N"
        # placeholder gallery images here. Those have been replaced with
        # real customer trip photos (see media_imports/gallery/ and
        # `python manage.py import_media`), so seed_site no longer
        # creates placeholder gallery cards at all — re-running this
        # command is safe and won't bring them back.

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} item(s)."))
