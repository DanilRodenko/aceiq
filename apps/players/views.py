from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from .models import Player
from apps.matches.models import Match
from datetime import date


def player_list(request):
    players_qs = Player.objects.all()
    paginator = Paginator(players_qs, 50)
    page = request.GET.get("page", 1)
    players = paginator.get_page(page)
    return render(request, "players/player_list.html", {"players": players})


def player_detail(request, slug):
    player = get_object_or_404(Player, slug=slug)

    # All matches
    matches = Match.objects.filter(Q(winner=player) | Q(loser=player)).order_by(
        "-tournament_date"
    )

    # Career stats
    won = matches.filter(winner=player)
    lost = matches.filter(loser=player)

    # Average stats as winner
    avg_stats = won.aggregate(
        avg_aces=Avg("w_aces"),
        avg_df=Avg("w_df"),
        avg_1stIn=Avg("w_1stIn"),
        avg_1stWon=Avg("w_1stWon"),
        avg_bpSaved=Avg("w_bpSaved"),
        avg_bpFaced=Avg("w_bpFaced"),
    )

    # Age
    age = None
    if player.date_of_birth:
        today = date.today()
        age = (
            today.year
            - player.date_of_birth.year
            - (
                (today.month, today.day)
                < (player.date_of_birth.month, player.date_of_birth.day)
            )
        )

    # Stats by season
    season_stats = (
        won.values("tournament_date__year")
        .annotate(
            wins=Count("id"),
            avg_aces=Avg("w_aces"),
        )
        .order_by("-tournament_date__year")
    )

    context = {
        "player": player,
        "age": age,
        "total_matches": matches.count(),
        "total_wins": won.count(),
        "total_losses": lost.count(),
        "win_rate": round(won.count() / matches.count() * 100, 1)
        if matches.count() > 0
        else 0,
        "avg_stats": avg_stats,
        "recent_matches": matches[:10],
        "season_stats": season_stats,
    }

    return render(request, "players/player_detail.html", context)
