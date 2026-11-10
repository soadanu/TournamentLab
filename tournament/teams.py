"""Team registration and validation."""
def validate_team_name(name):
    if not isinstance(name, str):
        raise ValueError("Team name must be text.")
    cleaned = name.strip()
    if not 2 <= len(cleaned) <= 30:
        raise ValueError("Team name must contain 2–30 characters.")
    return cleaned


def register_team(teams, name):
    """Register a team; mutate teams only after all validation succeeds."""
    cleaned = validate_team_name(name)
    normalized = cleaned.casefold()
    if any(team["name"].casefold() == normalized for team in teams):
        raise ValueError("A team with that name already exists.")
    team = {"id": f"TM{len(teams) + 1:03d}", "name": cleaned}
    teams.append(team)
    return team


def list_teams(teams):
    return sorted(teams, key=lambda team: team["id"])
