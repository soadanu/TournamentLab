"""Round-robin fixture generation and safe score recording."""
def generate_fixtures(teams):
    if not 4 <= len(teams) <= 8:
        raise ValueError("Register between 4 and 8 teams before generating fixtures.")
    if len({team["id"] for team in teams}) != len(teams):
        raise ValueError("Team IDs must be unique.")
    fixtures = []
    number = 1
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            fixtures.append({
                "id": f"M{number:03d}",
                "home_id": teams[i]["id"],
                "away_id": teams[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None,
            })
            number += 1
    return fixtures


def record_result(fixtures, fixture_id, home_score, away_score):
    for score in (home_score, away_score):
        if type(score) is not int or score < 0:
            raise ValueError("Scores must be nonnegative integers (not decimals or booleans).")
    fixture = next((item for item in fixtures if item["id"] == fixture_id), None)
    if fixture is None:
        raise ValueError("Fixture ID not found.")
    if fixture["status"] != "pending":
        raise ValueError("This fixture already has a result.")
    # Validate fully before changing any field.
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"
    return fixture
