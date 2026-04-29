import os
import sys
import django
import pandas as pd

sys.path.insert(0, "/Users/abcd/aceiq")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.players.models import Player  # type: ignore # noqa: E402


def load_players(filepath):
    atp_players = pd.read_csv(filepath)
    atp_players["dob"] = pd.to_datetime(
        atp_players["dob"], format="%Y%m%d", errors="coerce"
    ).dt.date
    players = []
    for _, row in atp_players.iterrows():
        dob = row["dob"] if pd.notna(row["dob"]) else None
        height = int(row["height"]) if pd.notna(row["height"]) else None
        player_obj = Player(
            atp_id=row["player_id"],
            name=f"{str(row['name_first'] or '')} {str(row['name_last'] or '')}".strip(),
            hand=row["hand"],
            date_of_birth=dob,
            country=row["ioc"],
            height_cm=height,
        )
        players.append(player_obj)

    Player.objects.bulk_create(
        players,
        update_conflicts=True,
        unique_fields=["atp_id"],
        update_fields=["name", "hand", "date_of_birth", "country", "height_cm"],
    )

    print(f"Successfully synced {len(players)} players.")


if __name__ == "__main__":
    filepath = "ml/data/raw/tennis_atp/atp_players.csv"
    load_players(filepath)
