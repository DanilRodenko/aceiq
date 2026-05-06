from django.db import models
from django.utils.text import slugify

import country_converter as coco


class Player(models.Model):
    HAND_CHOICES = [("R", "Right"), ("L", "Left"), ("U", "Unknown")]

    # Main information
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=3)  # IOC Code
    hand = models.CharField(max_length=1, choices=HAND_CHOICES, default="R")
    date_of_birth = models.DateField(null=True, blank=True)
    turned_pro = models.IntegerField(null=True, blank=True)  # year

    # Rating
    current_rank = models.IntegerField(null=True, blank=True)
    best_rank = models.IntegerField(null=True, blank=True)

    # Height
    height_cm = models.IntegerField(null=True, blank=True)

    # Photo
    photo = models.ImageField(upload_to="players/photos", null=True, blank=True)

    # ID for API
    atp_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Is Active
    is_active = models.BooleanField(default=False)

    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    class Meta:
        ordering = ["current_rank"]

    def __str__(self):
        return f"{self.name} ({self.country})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            if Player.objects.filter(slug=base_slug).exists():
                # Add birth year if duplicate
                year = self.date_of_birth.year if self.date_of_birth else "unknown"
                base_slug = f"{base_slug}-{year}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_flag(self):
        try:
            iso2 = coco.convert(self.country, to="ISO2", src="IOC")
            # Convert ISO2 to flag emoji
            flag = "".join(chr(ord(c) + 127397) for c in iso2.upper())
            return flag
        except:
            return "🌍"
