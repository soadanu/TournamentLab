"""Standings are derived from played fixtures; no stored scoreboard."""
def compute_standings(teams, fixtures):
    rows = {
        team["id"]: {
            "team_id": team["id"], "team": team["name"],
            "played": 0, "won": 0, "drawn": 0, "lost": 0,
            "gf": 0, "ga": 0, "gd": 0, "points": 0,
        }
        for team in teams
    }
    for match in fixtures:
        if match["status"] != "played":
            continue
        home = rows[match["home_id"]]
        away = rows[match["away_id"]]
        hs, aws = match["home_score"], match["away_score"]
        home["played"] += 1
        away["played"] += 1
        home["gf"] += hs
        home["ga"] += aws
        away["gf"] += aws
        away["ga"] += hs
        if hs > aws:
            home["won"] += 1
            away["lost"] += 1
            home["points"] += 3
        elif hs < aws:
            away["won"] += 1
            home["lost"] += 1
            away["points"] += 3
        else:
            home["drawn"] += 1
            away["drawn"] += 1
            home["points"] += 1
            away["points"] += 1
    for row in rows.values():
        row["gd"] = row["gf"] - row["ga"]
    return sorted(
        rows.values(),
        key=lambda row: (-row["points"], -row["gd"], -row["gf"], row["team"].casefold())
    )


def league_complete(fixtures):
    return bool(fixtures) and all(match["status"] == "played" for match in fixtures)


def champion(teams, fixtures):
    if not league_complete(fixtures):
        return None
    table = compute_standings(teams, fixtures)
    return table[0] if table else None
