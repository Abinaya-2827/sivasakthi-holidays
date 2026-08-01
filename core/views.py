from django.shortcuts import render, redirect
from django.contrib import messages

from destinations.models import Destination
from packages.models import Package
from gallery.models import GalleryImage
from .models import HeroSlide, Testimonial, WhyChooseUs
from .forms import ContactForm, PaymentProofForm


def home(request):
    context = {
        "hero_slides": HeroSlide.objects.filter(is_active=True),
        "why_choose_us": WhyChooseUs.objects.all(),
        "default_why_choose_us": [
            ("bi-shield-check", "Safe & Comfortable", "Well-maintained buses and careful drivers on every route."),
            ("bi-people", "Family Friendly", "Trusted by families, colleges, and corporate groups alike."),
            ("bi-award", "Experienced Team", "Years of experience planning South India's best routes."),
            ("bi-headset", "Always Reachable", "WhatsApp us anytime — we reply fast."),
        ],
        "popular_destinations": Destination.objects.filter(is_popular=True)[:8],
        "gallery_preview": GalleryImage.objects.all()[:8],
        "testimonials": Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, "home.html", context)


def about(request):
    about_points = [
        ("bi-shield-check", "Safe & Comfortable Travel", "Every trip is planned with safety and comfort as the top priority."),
        ("bi-people", "Family Trips", "Warm, well-planned getaways for families of all sizes."),
        ("bi-mortarboard", "College Tours", "Fun, safe, budget-friendly trips for student groups."),
        ("bi-briefcase", "Corporate & Group Tours", "Smooth logistics for company outings and large groups."),
        ("bi-building", "Temple Tours", "Comfortable pilgrimage trips to sacred destinations."),
        ("bi-heart", "Honeymoon Tours", "Private, romantic getaways tailored for couples."),
        ("bi-person-badge", "Experienced Drivers", "Skilled, road-tested drivers who know every route."),
        ("bi-truck", "Comfortable Buses", "Well-maintained coaches built for long, smooth journeys."),
    ]
    return render(request, "about.html", {"about_points": about_points})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We'll get back to you shortly.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def payment(request):
    if request.method == "POST":
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment screenshot received. We'll confirm your booking shortly.")
            return redirect("payment")
    else:
        form = PaymentProofForm()

    return render(request, "payment.html", {"form": form})
