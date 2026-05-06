from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from .models import Player
from apps.matches.models import Match
from datetime import date
import plotly.graph_objects as go


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
        avg_svpt=Avg("w_svpt"),
        avg_1stIn=Avg("w_1stIn"),
        avg_1stWon=Avg("w_1stWon"),
        avg_2ndWon=Avg("w_2ndWon"),
        avg_bpSaved=Avg("w_bpSaved"),
        avg_bpFaced=Avg("w_bpFaced"),
    )

    # Radar chart
    radar_chart = None
    if avg_stats["avg_aces"] and avg_stats["avg_bpSaved"]:
        # Calculate percentages properly
        avg_1stIn_pct = (
            (avg_stats["avg_1stIn"] or 0) / max((avg_stats["avg_svpt"] or 1), 1) * 100
        )
        avg_1stWon_pct = (
            (avg_stats["avg_1stWon"] or 0) / max((avg_stats["avg_1stIn"] or 1), 1) * 100
        )
        avg_2ndWon_pct = (
            (avg_stats["avg_2ndWon"] or 0)
            / max(((avg_stats["avg_svpt"] or 1) - (avg_stats["avg_1stIn"] or 0)), 1)
            * 100
        )
        avg_bpSaved_pct = (
            (avg_stats["avg_bpSaved"] or 0)
            / max((avg_stats["avg_bpFaced"] or 1), 1)
            * 100
        )

        categories = [
            "First Serve %",
            "1st Serve Won",
            "BP Saved",
            "2nd Serve Won",
            "Aces",
        ]
        values = [
            min(avg_1stIn_pct, 100),
            min(avg_1stWon_pct, 100),
            min(avg_bpSaved_pct, 100),
            min(avg_2ndWon_pct, 100),
            min((avg_stats["avg_aces"] or 0) * 5, 100),
        ]

        fig = go.Figure(
            data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                fillcolor="rgba(200, 255, 0, 0.15)",
                line=dict(color="#c8ff00", width=2),
            )
        )

        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    color="#6b7280",
                    gridcolor="rgba(0,0,0,0.1)",
                ),
                angularaxis=dict(color="#1a1a1a"),
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=100, r=100, t=100, b=100),
            width=600,
            height=600,
        )

        radar_chart = fig.to_json()

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
        .annotate(wins=Count("id"), avg_aces=Avg("w_aces"))
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
        "radar_chart": radar_chart,
    }

    return render(request, "players/player_detail.html", context)
