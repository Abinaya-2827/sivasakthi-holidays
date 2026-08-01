from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    short_description = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="destinations/")
    is_popular = models.BooleanField(default=False, help_text="Show in the Home page 'Popular Destinations' section")
    is_local_tamilnadu = models.BooleanField(default=False, help_text="Tag as part of 'All Local Tamil Nadu Tours'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def whatsapp_message(self):
        return f"Hello Sivasakthi Holidays, I would like to book this trip to {self.name}."
