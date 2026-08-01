from django.db import models


class HeroSlide(models.Model):
    """A slide in the homepage hero image slider."""
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="hero/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonial shown on the homepage."""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    submitted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_on"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class ContactMessage(models.Model):
    """Message submitted via the Contact page form."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_on"]

    def __str__(self):
        return f"{self.name} - {self.submitted_on:%d %b %Y}"


class PaymentProof(models.Model):
    """Screenshot a customer uploads after paying via UPI."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=200, blank=True, help_text="e.g. package name or trip date")
    screenshot = models.ImageField(upload_to="payment_proofs/")
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-uploaded_on"]

    def __str__(self):
        return f"{self.name} - {self.uploaded_on:%d %b %Y}"


class WhyChooseUs(models.Model):
    """A single reason/feature shown in the 'Why Choose Us' homepage section."""
    icon = models.CharField(
        max_length=50,
        default="bi-check-circle",
        help_text="Bootstrap Icons class name, e.g. bi-shield-check",
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Why Choose Us items"

    def __str__(self):
        return self.title
