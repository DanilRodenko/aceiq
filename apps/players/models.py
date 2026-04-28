from django.db import models


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
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["current_rank"]

    def __str__(self):
        return f"{self.name} ({self.country})"
