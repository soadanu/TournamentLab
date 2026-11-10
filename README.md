# TournamentLab — Esports League Manager

A Python command-line tournament manager. Register 4–8 teams, generate a single round-robin season, record scores, calculate standings, persist JSON, and announce a champion when every fixture is played.

## Requirements
- Python 3.10+ (standard library only)
- No external packages

## Run
```bash
python3 main.py
```

## Run tests
```bash
python3 -m unittest discover -s tests -v
```

## Rules
- Team names are trimmed, 2–30 characters, and unique case-insensitively.
- Each unordered pair plays once. A season can have 4–8 teams.
- Win = 3 points; draw = 1 point each; loss = 0.
- Ranking: points descending, goal difference descending, goals for descending, normalized team name ascending.
- Standings are calculated from played fixtures, not stored independently.
- A fixture accepts one result only. Scores must be nonnegative integers; booleans and decimals are rejected.
- JSON uses `schema_version: 1`; loaded data is validated before it replaces current in-memory state.
- Demo simulation requires an explicit `yes` and uses a reproducible random seed (2026).

## Example
Register Thunder, Comets, Phoenix and Rockets, generate six fixtures, enter some results, and view the table. The table remains marked IN PROGRESS until every fixture is played.

## Project layout
- `tournament/teams.py`: team validation and registration
- `tournament/fixtures.py`: round-robin schedule and result entry
- `tournament/standings.py`: derived league table and champion
- `tournament/storage.py`: validated JSON persistence
- `tournament/cli.py`: interactive menu
- `tests/`: automated unit tests

## Notes
The application intentionally does not provide an edit-result operation. To correct a completed result, start a fresh season or add a separately documented edit feature with tests.
