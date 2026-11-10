import json
import tempfile
import unittest
from pathlib import Path
from tournament.fixtures import generate_fixtures, record_result
from tournament.storage import save_tournament, load_tournament, validate_data

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.teams = [{"id":f"TM{i:03d}","name":f"Team {i}"} for i in range(1,5)]
        self.fixtures = generate_fixtures(self.teams)
    def test_save_reload_preserves_ids_and_scores(self):
        record_result(self.fixtures, "M001", 2, 1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "league.json"
            save_tournament(path, self.teams, self.fixtures)
            loaded = load_tournament(path)
            self.assertEqual(loaded["teams"], self.teams)
            self.assertEqual(loaded["fixtures"], self.fixtures)
    def test_bad_team_reference_rejected(self):
        data = {"schema_version":1, "teams":self.teams, "fixtures":[dict(self.fixtures[0])]}
        data["fixtures"][0]["home_id"] = "PHANTOM"
        with self.assertRaises(ValueError):
            validate_data(data)
    def test_duplicate_pair_rejected(self):
        duplicate = dict(self.fixtures[0])
        duplicate["id"] = "M999"
        data = {"schema_version":1, "teams":self.teams, "fixtures":self.fixtures + [duplicate]}
        with self.assertRaises(ValueError):
            validate_data(data)
