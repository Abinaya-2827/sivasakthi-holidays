from django.db import models


class GalleryImage(models.Model):
    caption = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_on"]

    def __str__(self):
        return self.caption or f"Gallery photo #{self.pk}"
