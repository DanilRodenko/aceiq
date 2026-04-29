import os
import sys
import glob
import django
import pandas as pd

sys.path.insert(0, "/Users/abcd/aceiq")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.matches.models import Match  # type: ignore # noqa: E402
from apps.players.models import Player  # type: ignore # noqa: E402


SURFACE_MAP = {
    "Hard": "HR",
    "Clay": "CL",
    "Grass": "GR",
    "Carpet": "CP",
}


def safe_int(val):
    return int(val) if pd.notna(val) else None


def load_matches(data_dir_pattern):
    files = glob.glob(data_dir_pattern)
    players_dict = {str(p.atp_id): p for p in Player.objects.all()}
    total = 0

    for file in sorted(files):
        df = pd.read_csv(file, low_memory=False)
        df["tourney_date"] = pd.to_datetime(
            df["tourney_date"], format="%Y%m%d", errors="coerce"
        ).dt.date

        matches_to_create = []

        for _, row in df.iterrows():
            winner = players_dict.get(str(row["winner_id"]))
            loser = players_dict.get(str(row["loser_id"]))

            if not winner or not loser:
                continue

            match_obj = Match(
                atp_match_id=f"{row['tourney_id']}_{row['match_num']}",
                tournament_name=row["tourney_name"],
                tournament_date=row["tourney_date"]
                if pd.notna(row["tourney_date"])
                else None,
                surface=SURFACE_MAP.get(row["surface"], "UN"),
                level=row["tourney_level"],
                round=row["round"],
                score=row["score"] if pd.notna(row["score"]) else "",
                minutes=safe_int(row["minutes"]),
                winner=winner,
                loser=loser,
                winner_rank=safe_int(row["winner_rank"]),
                loser_rank=safe_int(row["loser_rank"]),
                w_aces=safe_int(row["w_ace"]),
                w_df=safe_int(row["w_df"]),
                w_svpt=safe_int(row["w_svpt"]),
                w_1stIn=safe_int(row["w_1stIn"]),
                w_1stWon=safe_int(row["w_1stWon"]),
                w_2ndWon=safe_int(row["w_2ndWon"]),
                w_bpSaved=safe_int(row["w_bpSaved"]),
                w_bpFaced=safe_int(row["w_bpFaced"]),
                l_aces=safe_int(row["l_ace"]),
                l_df=safe_int(row["l_df"]),
                l_svpt=safe_int(row["l_svpt"]),
                l_1stIn=safe_int(row["l_1stIn"]),
                l_1stWon=safe_int(row["l_1stWon"]),
                l_2ndWon=safe_int(row["l_2ndWon"]),
                l_bpSaved=safe_int(row["l_bpSaved"]),
                l_bpFaced=safe_int(row["l_bpFaced"]),
            )
            matches_to_create.append(match_obj)

        if matches_to_create:
            Match.objects.bulk_create(
                matches_to_create,
                update_conflicts=True,
                unique_fields=["atp_match_id"],
                update_fields=[
                    "score",
                    "minutes",
                    "winner_rank",
                    "loser_rank",
                    "w_aces",
                    "w_df",
                    "w_svpt",
                    "w_1stIn",
                    "w_1stWon",
                    "w_2ndWon",
                    "w_bpSaved",
                    "w_bpFaced",
                    "l_aces",
                    "l_df",
                    "l_svpt",
                    "l_1stIn",
                    "l_1stWon",
                    "l_2ndWon",
                    "l_bpSaved",
                    "l_bpFaced",
                ],
            )
            total += len(matches_to_create)
            print(f"Loaded {len(matches_to_create)} matches from {file}")

    print("--- Finished ---")
    print(f"Total matches synced: {total}")


if __name__ == "__main__":
    load_matches("ml/data/raw/tennis_atp/atp_matches_[0-9]*.csv")
