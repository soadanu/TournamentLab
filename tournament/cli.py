"""Friendly command-line interface."""
import random
from .teams import register_team
from .fixtures import generate_fixtures, record_result
from .standings import compute_standings, league_complete, champion
from .storage import save_tournament, load_tournament

SAVE_FILE = "tournament.json"


def show_teams(teams):
    if not teams:
        print("No teams registered.")
        return
    for team in teams:
        print(f'{team["id"]}: {team["name"]}')


def show_fixtures(teams, fixtures):
    names = {team["id"]: team["name"] for team in teams}
    if not fixtures:
        print("No fixtures generated.")
        return
    for match in fixtures:
        status = match["status"]
        score = (f'{match["home_score"]}-{match["away_score"]}'
                 if status == "played" else "vs")
        print(f'{match["id"]}: {names[match["home_id"]]} {score} '
              f'{names[match["away_id"]]} [{status}]')


def show_table(teams, fixtures):
    table = compute_standings(teams, fixtures)
    print("\nLEAGUE TABLE — " + ("COMPLETE" if league_complete(fixtures) else "IN PROGRESS"))
    print(f'{"Team":20} {"P":>2} {"W":>2} {"D":>2} {"L":>2} {"GF":>3} {"GA":>3} {"GD":>3} {"Pts":>4}')
    for row in table:
        print(f'{row["team"][:20]:20} {row["played"]:2} {row["won"]:2} {row["drawn"]:2} '
              f'{row["lost"]:2} {row["gf"]:3} {row["ga"]:3} {row["gd"]:3} {row["points"]:4}')
    winner = champion(teams, fixtures)
    if winner:
        print(f'\nCHAMPION: {winner["team"]}')
    else:
        print("\nChampion will be announced when every fixture has a result.")


def simulate_demo(teams, fixtures):
    if not fixtures:
        raise ValueError("Generate fixtures first.")
    if input("This will fill every pending fixture with demo scores. Continue? (yes/no): ").strip().casefold() != "yes":
        print("Demo simulation cancelled.")
        return
    rng = random.Random(2026)
    for match in fixtures:
        if match["status"] == "pending":
            record_result(fixtures, match["id"], rng.randint(0, 4), rng.randint(0, 4))
    print("Demo fixtures simulated with seed 2026.")


def run():
    teams, fixtures = [], []
    while True:
        print("""
========================================
       TOURNAMENTLAB
       ESPORTS LEAGUE MANAGER
========================================
1. Register team
2. List teams
3. Generate fixtures
4. List fixtures
5. Record match result
6. View league table
7. Save tournament
8. Load tournament
9. Show champion
10. Simulate demo fixtures
0. Exit
""")
        choice = input("Select an option: ").strip()
        try:
            if choice == "1":
                team = register_team(teams, input("Team name: "))
                print(f'Registered {team["name"]} ({team["id"]}).')
            elif choice == "2":
                show_teams(teams)
            elif choice == "3":
                if fixtures:
                    raise ValueError("Fixtures have already been generated for this season.")
                fixtures = generate_fixtures(teams)
                print(f"Generated {len(fixtures)} fixtures.")
            elif choice == "4":
                show_fixtures(teams, fixtures)
            elif choice == "5":
                fixture_id = input("Fixture ID: ").strip().upper()
                home = int(input("Home score: ").strip())
                away = int(input("Away score: ").strip())
                record_result(fixtures, fixture_id, home, away)
                print("Result successfully recorded.")
            elif choice == "6":
                show_table(teams, fixtures)
            elif choice == "7":
                save_tournament(SAVE_FILE, teams, fixtures)
                print(f"Saved to {SAVE_FILE}.")
            elif choice == "8":
                loaded = load_tournament(SAVE_FILE)
                teams, fixtures = loaded["teams"], loaded["fixtures"]
                print("Tournament loaded successfully.")
            elif choice == "9":
                winner = champion(teams, fixtures)
                print(f'CHAMPION: {winner["team"]}' if winner else "League is still in progress.")
            elif choice == "10":
                simulate_demo(teams, fixtures)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Choose a number from 0 to 10.")
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}")
        except EOFError:
            print("\nGoodbye!")
            break
