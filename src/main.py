import json
from datetime import datetime
from pathlib import Path

from locations import get_daily_location
from weather import get_weather
from sports import get_all_sports

from dashboard import generate_dashboard

BASE_DIR = Path(__file__).resolve().parent.parent

WEATHER_DIR = BASE_DIR / "data" / "weather"
SPORTS_DIR = BASE_DIR / "data" / "sports"


def save_json(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def main():

    now = datetime.now()

    today = now.strftime(
        "%Y-%m-%d"
    )

    timestamp = now.isoformat()

    print()
    print("=" * 60)
    print("DAILYPULSE")
    print("=" * 60)

    print(
        f"Run time: {timestamp}"
    )

    location = get_daily_location()

    print(
        f"Location: "
        f"{location['city']}, "
        f"{location['state']}"
    )

    print()
    print("Getting weather...")

    weather = get_weather(location)

    weather_data = {
        "timestamp": timestamp,
        "location": location,
        "weather": weather
    }

    save_json(
        WEATHER_DIR / f"{today}.json",
        weather_data
    )

    print("✓ Weather saved")

    print()
    print("Getting sports...")

    sports = get_all_sports()

    sports_data = {
        "timestamp": timestamp,
        "location": location,
        "sports": sports
    }

    save_json(
        SPORTS_DIR / f"{today}.json",
        sports_data
    )

    print("✓ Sports saved")

    print()
    print("Updating README...")

    generate_dashboard()

    print("✓ README updated")

    print()
    print("=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()