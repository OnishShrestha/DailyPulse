import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

README_FILE = BASE_DIR / "README.md"

WEATHER_DIR = BASE_DIR / "data" / "weather"
SPORTS_DIR = BASE_DIR / "data" / "sports"


def load_json(path):

    if not path.exists():
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def format_game(game):

    if not isinstance(game, dict):
        return "Data unavailable."

    return (
        f"**{game.get('away_team', 'Unknown')}** "
        f"vs "
        f"**{game.get('home_team', 'Unknown')}**  \n"
        f"Status: {game.get('status', 'Unknown')}  \n"
        f"Time: {game.get('date', 'Unknown')}  \n"
        f"Venue: {game.get('venue', 'Unknown')}  \n"
        f"Location: {game.get('city', 'Unknown')}, "
        f"{game.get('state', '')}  \n"
    )


def format_sport(name, games):

    lines = []

    lines.append(
        f"## {name}"
    )

    if isinstance(games, dict):
        lines.append(
            f"> ⚠️ Unable to retrieve {name} data."
        )

        lines.append("")

        return "\n".join(lines)

    if not games:

        lines.append(
            "No games scheduled or available."
        )

        lines.append("")

        return "\n".join(lines)

    for game in games:

        lines.append(
            format_game(game)
        )

        lines.append("---")

    return "\n".join(lines)


def generate_dashboard():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    weather_file = (
        WEATHER_DIR / f"{today}.json"
    )

    sports_file = (
        SPORTS_DIR / f"{today}.json"
    )

    weather_data = load_json(
        weather_file
    )

    sports_data = load_json(
        sports_file
    )

    location = weather_data.get(
        "location",
        {}
    )

    weather = weather_data.get(
        "weather",
        {}
    )

    current = weather.get(
        "current",
        {}
    )

    temperature = current.get(
        "temperature_2m",
        "N/A"
    )

    feels_like = current.get(
        "apparent_temperature",
        "N/A"
    )

    humidity = current.get(
        "relative_humidity_2m",
        "N/A"
    )

    wind = current.get(
        "wind_speed_10m",
        "N/A"
    )

    precipitation = current.get(
        "precipitation",
        "N/A"
    )

    generated = datetime.now().strftime(
        "%B %d, %Y at %I:%M %p"
    )

    sports = sports_data.get(
        "sports",
        {}
    )

    readme = f"""# 🌎 DailyPulse

> Automated weather + MLB + NBA + NFL dashboard powered by GitHub Actions.

---

## 📍 Location of the Day

### {location.get('city', 'Unknown')}, {location.get('state', '')}

🇺🇸 {location.get('country', '')}

---

## 🌦️ Current Weather

| Metric | Value |
|---|---:|
| Temperature | {temperature} °F |
| Feels Like | {feels_like} °F |
| Humidity | {humidity}% |
| Wind | {wind} mph |
| Precipitation | {precipitation} in |

---

## 🏟️ Sports Dashboard

{format_sport("⚾ MLB", sports.get("MLB", []))}

{format_sport("🏀 NBA", sports.get("NBA", []))}

{format_sport("🏈 NFL", sports.get("NFL", []))}

---

## 🤖 Automation

| Item | Value |
|---|---|
| Last update | {generated} |
| Daily location | {location.get('city', 'Unknown')} |
| Weather source | Open-Meteo |
| Sports source | ESPN public scoreboard |
| Updates per day | 3 |

---

## 📁 Historical Data

Weather:

`data/weather/`

Sports:

`data/sports/`

Locations:

`data/history/location_history.json`

---

## ℹ️ About

DailyPulse automatically collects weather and sports information throughout the day and stores historical snapshots in this repository.

Weather data is provided by Open-Meteo.

Sports data is retrieved from ESPN's public scoreboard endpoints.

"""

    with open(
        README_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(readme)


if __name__ == "__main__":
    generate_dashboard()