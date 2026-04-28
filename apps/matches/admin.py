from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "tournament_name",
        "tournament_date",
        "winner",
        "loser",
        "surface",
        "round",
        "score",
    ]
    search_fields = ["tournament_name", "winner__name", "loser__name"]
    list_filter = ["surface", "round", "level"]
    ordering = ["-tournament_date"]
