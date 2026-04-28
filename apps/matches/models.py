from django.db import models


class Match(models.Model):
    SURFACE = [
        ("HR", "Hard"),
        ("CL", "Clay"),
        ("GR", "Grass"),
        ("CP", "Carpet"),
        ("UN", "Unknown"),
    ]
    ROUND = [
        ("R128", "Top 128"),
        ("R64", "Top 64"),
        ("R32", "Top 32"),
        ("R16", "Top 16"),
        ("QF", "Quater-Final"),
        ("SF", "Semi-Final"),
        ("F", "Final"),
    ]

    LEVEL = [("G", "Grand Slam"), ("M", "Masters"), ("A", "ATP"), ("C", "Challenger")]

    # Players
    winner = models.ForeignKey(
        "players.Player",
        on_delete=models.SET_NULL,
        null=True,
        related_name="won_matches",
    )
    loser = models.ForeignKey(
        "players.Player",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lose_matches",
    )

    # Tournament
    tournament_name = models.CharField(max_length=200)
    tournament_date = models.DateField(null=True, blank=True)
    surface = models.CharField(max_length=2, choices=SURFACE)
    round = models.CharField(max_length=4, choices=ROUND)
    level = models.CharField(max_length=1, choices=LEVEL)

    score = models.CharField(max_length=25)
    minutes = models.IntegerField(null=True, blank=True)

    # Winner stats
    w_aces = models.IntegerField(null=True, blank=True)
    w_df = models.IntegerField(null=True, blank=True)
    w_svpt = models.IntegerField(null=True, blank=True)
    w_1stIn = models.IntegerField(null=True, blank=True)
    w_1stWon = models.IntegerField(null=True, blank=True)
    w_2ndWon = models.IntegerField(null=True, blank=True)
    w_bpSaved = models.IntegerField(null=True, blank=True)
    w_bpFaced = models.IntegerField(null=True, blank=True)

    # Loser stats
    l_aces = models.IntegerField(null=True, blank=True)
    l_df = models.IntegerField(null=True, blank=True)
    l_svpt = models.IntegerField(null=True, blank=True)
    l_1stIn = models.IntegerField(null=True, blank=True)
    l_1stWon = models.IntegerField(null=True, blank=True)
    l_2ndWon = models.IntegerField(null=True, blank=True)
    l_bpSaved = models.IntegerField(null=True, blank=True)
    l_bpFaced = models.IntegerField(null=True, blank=True)

    # Rank at match time
    winner_rank = models.IntegerField(null=True, blank=True)
    loser_rank = models.IntegerField(null=True, blank=True)

    # Meta
    atp_match_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tournament_date"]
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.winner} vs {self.loser} — {self.tournament_name} ({self.tournament_date})"
