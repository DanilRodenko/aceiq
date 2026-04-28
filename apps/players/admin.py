from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "hand", "current_rank", "atp_id"]
    search_fields = ["name", "country", "atp_id"]
    ordering = ["current_rank"]
