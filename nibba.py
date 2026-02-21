import datetime

import mysql.connector
from requests import get
from bs4 import BeautifulSoup

urls_and_leagues = [
    ("https://fbref.com/en/comps/29/schedule/Allsvenskan-Scores-and-Fixtures", "LEAGUE SZWECJA 2024-2025"),
     ("https://fbref.com/en/comps/48/schedule/Superettan-Scores-and-Fixtures", "LEAGUE SZWECJA 2 2024-2025"),
    ("https://fbref.com/en/comps/49/schedule/J2-League-Scores-and-Fixtures", "LEAGUE JAPONIA 2 2024"),
    ("https://fbref.com/en/comps/25/schedule/J1-League-Scores-and-Fixtures", "LEAGUE JAPONIA 2024"),
    ("https://fbref.com/en/comps/55/schedule/K-League-1-Scores-and-Fixtures", "LEAGUE KOREA 2024-2025"),
    ("https://fbref.com/en/comps/28/schedule/Eliteserien-Scores-and-Fixtures", "LEAGUE NORWEGIA 2024-2025"),
    ("https://fbref.com/en/comps/185/schedule/Toppserien-Scores-and-Fixtures", "LEAGUE NORWEGIA 2 2024-2025"),
     ("https://fbref.com/en/comps/43/schedule/Veikkausliiga-Scores-and-Fixtures", "LEAGUE FINLANDIA 2024-2025"),
]

desired_scores = ["1-2", "2-1", "1-3", "3-1", "1-4", "4-1", "2-3", "3-2", "3-3", "4-3", "3-4", "4-4", "4-5", "5-4",
                  "5-2", "2-5", "5-3", "3-5",
                  "2-4", "4-2", "5-5"]

db_config = {
    'user': 'root',
    'password': 'j4pi3rd0l3',
    'host': 'localhost',
    'port': 3306,
    'database': 'football_scores'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS matches_date_wszystko (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_date DATE,
    league_name VARCHAR(255),
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    score VARCHAR(10),
    match_result VARCHAR(255),
    match_report_url VARCHAR(255)
)
''')

for url, league_name in urls_and_leagues:
    page = get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    print(f"\n- {league_name}\n")

    for row in soup.find_all('tr')[1:]:
        date_time = row.find('td', {'data-stat': 'date'})
        if date_time and date_time.find('a'):
            date = date_time.find('a').text
        else:
            continue
        home_team_cell = row.find('td', {'data-stat': 'home_team'})
        score_cell = row.find('td', {'data-stat': 'score'})
        away_team_cell = row.find('td', {'data-stat': 'away_team'})
        match_report_cell = row.find('td', {'data-stat': 'match_report'})

        if home_team_cell and score_cell and away_team_cell and match_report_cell:
            home_team = home_team_cell.text.strip()
            score = score_cell.find('a').text.strip() if score_cell.find('a') else score_cell.text.strip()
            score = score.replace('–', '-').strip()
            away_team = away_team_cell.text.strip()
            match_report_url = match_report_cell.find('a')['href'] if match_report_cell.find('a') else None
            match_result = f"{home_team} {score} : {away_team}"

            if score in desired_scores and match_report_url:
                match_report_url = f"https://fbref.com{match_report_url}"
                cursor.execute('''
                INSERT INTO matches_date_wszystko (match_date, league_name, home_team, away_team, score, match_result, match_report_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (date, league_name, home_team, away_team, score, match_result, match_report_url))
                conn.commit()

                print(match_result)
                print(f"Match Report URL: {match_report_url}")

# Close the database connection
cursor.close()
conn.close()