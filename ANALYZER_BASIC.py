import mysql.connector
from itertools import combinations
from collections import defaultdict

# Connect to DB
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='j4pi3rd0l3',
    database='football_scores'
)
cursor = db.cursor()

# Create the missing_matches_2024 table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS missing_matches_2024 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team1 VARCHAR(255) NOT NULL,
    team2 VARCHAR(255) NOT NULL,
    triplet_teamA VARCHAR(255) NOT NULL,
    triplet_teamB VARCHAR(255) NOT NULL,
    triplet_teamC VARCHAR(255) NOT NULL,
    league_name VARCHAR(255) NOT NULL
)
""")

# 1. Get all unique teams per league
cursor.execute("""
    SELECT DISTINCT league_name, team_a AS team FROM lamaczki_2024
    UNION
    SELECT DISTINCT league_name, team_b AS team FROM lamaczki_2024
""")
league_team_rows = cursor.fetchall()

league_teams = defaultdict(set)
for league_name, team in league_team_rows:
    league_teams[league_name].add(team)

# 2. Get all existing matches as canonical pairs, per league
cursor.execute("""
    SELECT league_name, LEAST(team_a, team_b), GREATEST(team_a, team_b) FROM lamaczki_2024
""")
matches_rows = cursor.fetchall()

league_existing_matches = defaultdict(set)
for league_name, team1, team2 in matches_rows:
    league_existing_matches[league_name].add((team1, team2))

# 3. Process each league
missing_matches = []

for league_name, teams in league_teams.items():
    sorted_teams = sorted(teams)
    triplets = combinations(sorted_teams, 3)
    existing_matches = league_existing_matches[league_name]

    for teamA, teamB, teamC in triplets:
        # Define the 3 possible matches
        pairs = [
            (min(teamA, teamB), max(teamA, teamB)),
            (min(teamA, teamC), max(teamA, teamC)),
            (min(teamB, teamC), max(teamB, teamC))
        ]

        # Check which exist
        exist_flags = [pair in existing_matches for pair in pairs]

        if sum(exist_flags) == 2:
            # One missing, identify it
            missing_index = exist_flags.index(False)
            missing_pair = pairs[missing_index]
            team1, team2 = missing_pair
            missing_matches.append((team1, team2, teamA, teamB, teamC, league_name))

print(f"Found {len(missing_matches)} missing matches to insert")

# 4. Insert into DB
insert_query = """
    INSERT INTO missing_matches_2024 (team1, team2, triplet_teamA, triplet_teamB, triplet_teamC, league_name)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, missing_matches)
db.commit()

print("Inserted missing matches into missing_matches_2024")

cursor.close()
db.close()
