from django.db import models


class Package(models.Model):
    TOUR_TYPES = [
        ("Family Tour", "Family Tour"),
        ("Corporate Tour", "Corporate Tour"),
        ("Temple Tour", "Temple Tour"),
        ("Friends Tour", "Friends Tour"),
        ("Weekend Getaway", "Weekend Getaway"),
        ("Honeymoon Tour", "Honeymoon Tour"),
    ]

    tour_type = models.CharField(max_length=30, choices=TOUR_TYPES)
    destination_text = models.CharField(max_length=200, help_text="e.g. Kerala, Ooty & Kodaikanal")
    duration = models.CharField(max_length=50, help_text="e.g. 3 Days / 2 Nights")
    facilities = models.TextField(help_text="One facility per line, e.g. AC Bus, Hotel Stay, Breakfast")
    starting_price = models.CharField(
        max_length=50, blank=True,
        help_text="e.g. ₹4,999 per person — shown as a 'starting from' price on the card",
    )
    popular_destinations = models.CharField(
        max_length=300, blank=True,
        help_text="Comma-separated, e.g. Kerala, Ooty, Munnar",
    )
    image = models.ImageField(upload_to="packages/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "tour_type"]

    def __str__(self):
        return f"{self.tour_type} - {self.destination_text}"

    def facilities_list(self):
        return [line.strip() for line in self.facilities.splitlines() if line.strip()]

    def popular_destinations_list(self):
        return [d.strip() for d in self.popular_destinations.split(",") if d.strip()]

    def whatsapp_message(self):
        return f"Hello Sivasakthi Holidays, I would like to book this trip ({self.tour_type} - {self.destination_text})."
