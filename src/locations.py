import json
import random
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

LOCATIONS_FILE = BASE_DIR / "config" / "locations.json"
HISTORY_FILE = BASE_DIR / "data" / "history" / "location_history.json"


def load_locations():
    with open(LOCATIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_history():
    if not HISTORY_FILE.exists():
        return {}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def get_daily_location():
    today = date.today().isoformat()

    history = load_history()
    locations = load_locations()

    if today in history:
        return history[today]

    used_locations = {
        value["city"]
        for value in history.values()
    }

    available_locations = [
        location
        for location in locations
        if location["city"] not in used_locations
    ]

    if not available_locations:
        available_locations = locations

    random.seed(today)

    location = random.choice(available_locations)

    history[today] = location

    save_history(history)

    return location