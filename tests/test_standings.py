import unittest
from tournament.fixtures import generate_fixtures, record_result
from tournament.standings import compute_standings, champion

class StandingsTests(unittest.TestCase):
    def setUp(self):
        self.teams = [{"id": f"TM{i:03d}", "name": n} for i, n in enumerate(
            ["Thunder", "Comets", "Phoenix", "Rockets"], 1)]
        self.fixtures = generate_fixtures(self.teams)
    def test_win_draw_loss_points(self):
        record_result(self.fixtures, "M001", 2, 0)
        record_result(self.fixtures, "M004", 1, 1)
        table = {r["team"]: r for r in compute_standings(self.teams, self.fixtures)}
        self.assertEqual(table["Thunder"]["points"], 3)
        self.assertEqual(table["Comets"]["points"], 1)
        self.assertEqual(table["Phoenix"]["points"], 1)
    def test_tiebreak_goal_difference_then_goals_then_name(self):
        teams = [{"id":"1","name":"Zulu"},{"id":"2","name":"Alpha"}]
        fixtures = [{"id":"M1","home_id":"1","away_id":"2","status":"played",
                     "home_score":2,"away_score":1}]
        result = compute_standings(teams, fixtures)
        self.assertEqual(result[0]["team"], "Zulu")
    def test_standings_recomputed_from_matches(self):
        first = compute_standings(self.teams, self.fixtures)
        record_result(self.fixtures, "M001", 3, 0)
        second = compute_standings(self.teams, self.fixtures)
        self.assertNotEqual(first, second)
    def test_champion_only_when_complete(self):
        self.assertIsNone(champion(self.teams, self.fixtures))
        for match in self.fixtures:
            if match["status"] == "pending":
                record_result(self.fixtures, match["id"], 1, 0)
        self.assertIsNotNone(champion(self.teams, self.fixtures))
