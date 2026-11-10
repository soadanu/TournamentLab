"""Versioned JSON persistence with validation before state replacement."""
import json
from pathlib import Path

SCHEMA_VERSION = 1


def validate_data(data):
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported or missing schema_version.")
    teams, fixtures = data.get("teams"), data.get("fixtures")
    if not isinstance(teams, list) or not isinstance(fixtures, list):
        raise ValueError("Teams and fixtures must be lists.")
    team_ids, names = set(), set()
    for team in teams:
        if not isinstance(team, dict) or set(team) != {"id", "name"}:
            raise ValueError("Invalid team record.")
        if not isinstance(team["id"], str) or not team["id"]:
            raise ValueError("Invalid team ID.")
        if team["id"] in team_ids:
            raise ValueError("Duplicate team ID.")
        if not isinstance(team["name"], str) or not 2 <= len(team["name"].strip()) <= 30:
            raise ValueError("Invalid team name.")
        normalized = team["name"].strip().casefold()
        if normalized in names:
            raise ValueError("Duplicate team name.")
        team_ids.add(team["id"])
        names.add(normalized)
    fixture_ids, pairs = set(), set()
    for match in fixtures:
        required = {"id", "home_id", "away_id", "status", "home_score", "away_score"}
        if not isinstance(match, dict) or set(match) != required:
            raise ValueError("Invalid fixture record.")
        if not isinstance(match["id"], str) or not match["id"] or match["id"] in fixture_ids:
            raise ValueError("Invalid or duplicate fixture ID.")
        fixture_ids.add(match["id"])
        home, away = match["home_id"], match["away_id"]
        if home not in team_ids or away not in team_ids or home == away:
            raise ValueError("Fixture references invalid teams.")
        pair = frozenset((home, away))
        if pair in pairs:
            raise ValueError("Duplicate team pairing.")
        pairs.add(pair)
        status = match["status"]
        hs, aws = match["home_score"], match["away_score"]
        if status == "pending":
            if hs is not None or aws is not None:
                raise ValueError("Pending fixtures must not have scores.")
        elif status == "played":
            if type(hs) is not int or hs < 0 or type(aws) is not int or aws < 0:
                raise ValueError("Played fixtures need nonnegative integer scores.")
        else:
            raise ValueError("Unknown fixture status.")
    if fixtures and len(teams) < 4:
        raise ValueError("A season with fixtures needs at least four teams.")
    return {"teams": teams, "fixtures": fixtures}


def save_tournament(path, teams, fixtures):
    data = {"schema_version": SCHEMA_VERSION, "teams": teams, "fixtures": fixtures}
    validate_data(data)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(target)


def load_tournament(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load tournament: {exc}") from exc
    return validate_data(data)
