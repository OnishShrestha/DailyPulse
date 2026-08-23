import requests
from datetime import datetime


SPORTS = {
    "MLB": {
        "sport": "baseball",
        "league": "mlb"
    },
    "NBA": {
        "sport": "basketball",
        "league": "nba"
    },
    "NFL": {
        "sport": "football",
        "league": "nfl"
    }
}


def get_scoreboard(sport_name):
    config = SPORTS[sport_name]

    url = (
        f"https://site.api.espn.com/apis/site/v2/"
        f"sports/{config['sport']}/{config['league']}/scoreboard"
    )

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def parse_games(data):
    games = []

    for event in data.get("events", []):

        competition = event.get(
            "competitions",
            [{}]
        )[0]

        competitors = competition.get(
            "competitors",
            []
        )

        home = None
        away = None

        for team in competitors:

            if team.get("homeAway") == "home":
                home = team

            elif team.get("homeAway") == "away":
                away = team

        status = (
            competition
            .get("status", {})
            .get("type", {})
        )

        venue = competition.get(
            "venue",
            {}
        )

        address = venue.get(
            "address",
            {}
        )

        game = {
            "id": event.get("id"),
            "name": event.get("name"),
            "short_name": event.get("shortName"),

            "date": event.get("date"),

            "status": status.get(
                "description",
                "Unknown"
            ),

            "state": status.get(
                "state",
                "unknown"
            ),

            "detail": status.get(
                "detail",
                ""
            ),

            "home_team": (
                home.get("team", {}).get("displayName")
                if home else None
            ),

            "home_abbreviation": (
                home.get("team", {}).get("abbreviation")
                if home else None
            ),

            "home_score": (
                home.get("score")
                if home else None
            ),

            "away_team": (
                away.get("team", {}).get("displayName")
                if away else None
            ),

            "away_abbreviation": (
                away.get("team", {}).get("abbreviation")
                if away else None
            ),

            "away_score": (
                away.get("score")
                if away else None
            ),

            "venue": venue.get(
                "fullName",
                "Unknown"
            ),

            "city": address.get(
                "city",
                "Unknown"
            ),

            "state": address.get(
                "state",
                ""
            )
        }

        games.append(game)

    return games


def get_all_sports():
    result = {}

    for sport in SPORTS:

        try:
            data = get_scoreboard(sport)

            result[sport] = parse_games(data)

        except Exception as error:

            result[sport] = {
                "error": str(error),
                "games": []
            }

    return result