# Design decisions

1. Team IDs are stable references; names are display labels.
2. Fixtures are the canonical record of match outcomes.
3. Standings are derived on demand to avoid a separately mutable scoreboard drifting out of sync.
4. Scores are validated before fixture mutation; `type(score) is int` excludes booleans.
5. A fixture pair is unordered for duplicate detection.
6. Ranking uses points, goal difference, goals for, then casefolded team name. No head-to-head rule is introduced.
7. JSON is versioned and validated before the loaded data is returned to the CLI.
8. Demo scores use a local `random.Random(2026)` instance and require explicit confirmation.
