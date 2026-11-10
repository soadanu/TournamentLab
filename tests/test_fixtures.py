import unittest
from tournament.fixtures import generate_fixtures, record_result

def teams(n):
    return [{"id": f"TM{i:03d}", "name": f"Team {i}"} for i in range(1, n + 1)]

class FixtureTests(unittest.TestCase):
    def test_reject_fewer_than_four(self):
        with self.assertRaises(ValueError):
            generate_fixtures(teams(3))
    def test_four_teams_six_fixtures(self):
        self.assertEqual(len(generate_fixtures(teams(4))), 6)
    def test_six_teams_fifteen_fixtures(self):
        self.assertEqual(len(generate_fixtures(teams(6))), 15)
    def test_no_self_or_duplicate_pairs(self):
        fixtures = generate_fixtures(teams(5))
        pairs = [frozenset((m["home_id"], m["away_id"])) for m in fixtures]
        self.assertTrue(all(m["home_id"] != m["away_id"] for m in fixtures))
        self.assertEqual(len(pairs), len(set(pairs)))
    def test_negative_float_and_bool_rejected_without_mutation(self):
        fixtures = generate_fixtures(teams(4))
        before = [dict(m) for m in fixtures]
        for bad in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                record_result(fixtures, "M001", bad, 0)
            self.assertEqual(fixtures, before)
    def test_unknown_fixture(self):
        with self.assertRaises(ValueError):
            record_result(generate_fixtures(teams(4)), "M999", 1, 0)
    def test_duplicate_result(self):
        fixtures = generate_fixtures(teams(4))
        record_result(fixtures, "M001", 1, 0)
        with self.assertRaises(ValueError):
            record_result(fixtures, "M001", 2, 0)
