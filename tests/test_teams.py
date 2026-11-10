import unittest
from tournament.teams import register_team, validate_team_name

class TeamTests(unittest.TestCase):
    def test_register_team(self):
        teams = []
        self.assertEqual(register_team(teams, " Red ")["name"], "Red")
        self.assertEqual(teams[0]["id"], "TM001")
    def test_duplicate_casefolded_name(self):
        teams = []
        register_team(teams, "Red Comets")
        with self.assertRaises(ValueError):
            register_team(teams, " red comets ")
    def test_blank_name(self):
        with self.assertRaises(ValueError):
            validate_team_name("  ")
    def test_too_long_name(self):
        with self.assertRaises(ValueError):
            validate_team_name("x" * 31)
