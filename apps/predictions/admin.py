from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        "match",
        "player1",
        "player2",
        "win_probability_p1",
        "win_probability_p2",
        "is_correct",
        "created_at",
    ]
    list_filter = ["is_correct", "model_version"]
    ordering = ["-created_at"]
