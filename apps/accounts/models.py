from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    # Константы для удобного обращения в коде
    FREE = "F"
    TRIAL = "T"
    PRO = "P"
    ENTERPRISE = "E"

    SUBSCRIPTION_CHOICE = [
        (FREE, "Free"),
        (TRIAL, "Trial"),
        (PRO, "Pro"),
        (ENTERPRISE, "Enterprise"),
    ]

    subscription_plan = models.CharField(
        max_length=1, choices=SUBSCRIPTION_CHOICE, default=FREE
    )

    subscription_end = models.DateTimeField(
        null=True, blank=True, help_text="When the subscription expires"
    )

    @property
    def is_pro(self):
        """
        Calculates if the user has active paid/trial features.
        """
        # If free plan = False
        if self.subscription_plan == self.FREE:
            return False

        # Check end date
        if self.subscription_end:
            return self.subscription_end > timezone.now()

        return True

    def __str__(self):
        return f"{self.username} ({self.get_subscription_plan_display()})"  # type: ignore
