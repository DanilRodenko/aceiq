from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Prediction(models.Model):
    # Match
    match = models.ForeignKey(
        "matches.Match", on_delete=models.CASCADE, related_name="predictions"
    )

    # Players
    player1 = models.ForeignKey(
        "players.Player", on_delete=models.CASCADE, related_name="p1_predictions"
    )
    player2 = models.ForeignKey(
        "players.Player", on_delete=models.CASCADE, related_name="p2_predictions"
    )

    # Probabilities
    win_probability_p1 = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Probability for Player 1 (0.0 - 1.0)",
    )
    win_probability_p2 = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Probability for Player 2 (0.0 - 1.0)",
    )

    # Analytics and metadata
    key_factors = models.JSONField(
        default=dict, help_text="Reasoning behind the prediction"
    )
    model_version = models.CharField(
        max_length=50, help_text="Version of the ML model used"
    )

    # results
    actual_winner = models.ForeignKey(
        "players.Player",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actual_wins_predicted",
    )
    is_correct = models.BooleanField(
        null=True, blank=True, help_text="Was the prediction accurate?"
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for Match {self.match.id} (v{self.model_version})"

    class Meta:
        ordering = ["-created_at"]
