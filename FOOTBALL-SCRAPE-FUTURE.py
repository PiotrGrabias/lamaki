
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector
import time

urls_and_leagues = [
    ("https://fbref.com/en/comps/51/2025-2026/schedule/2025-2026-Eerste-Divisie-Scores-and-Fixtures",
     "LEAGUE HOLANDIA 2 2026"),
    # ("https://fbref.com/en/comps/56/schedule/Austrian-Bundesliga-Scores-and-Fixtures", "LEAGUE AUSTRIA 2025"),
    # ("https://fbref.com/en/comps/37/schedule/Belgian-Pro-League-Scores-and-Fixtures", "LEAGUE BELGIA 2025"),
    ("https://fbref.com/en/comps/69/2025-2026/schedule/2025-2026-Challenger-Pro-League-Scores-and-Fixtures",
     "LEAGUE BELGIA 2 2026"),
    ("https://fbref.com/en/comps/20/2025-2026/schedule/2025-2026-Bundesliga-Scores-and-Fixtures", "LEAGUE NIEMCY 2026"),
    # ("https://fbref.com/en/comps/33/schedule/2-Bundesliga-Scores-and-Fixtures", "LEAGUE NIEMCY 2 2025"),
    ("https://fbref.com/en/comps/10/2025-2026/schedule/2025-2026-Championship-Scores-and-Fixtures",
     "LEAGUE ANGLIA 2 2026"),
    # ("https://fbref.com/en/comps/63/schedule/Hrvatska-NL-Scores-and-Fixtures", "LEAGUE CHORWACJA 2025"),
    # ("https://fbref.com/en/comps/66/schedule/Czech-First-League-Scores-and-Fixtures", "LEAGUE CZECHY 2025"),
    # ("https://fbref.com/en/comps/50/schedule/Danish-Superliga-Scores-and-Fixtures", "LEAGUE DANIA 2025"),
    # ("https://fbref.com/en/comps/36/schedule/Ekstraklasa-Scores-and-Fixtures", "LEAGUE POLSKA 2025"),
    ("https://fbref.com/en/comps/9/2025-2026/schedule/2025-2026-Eredivisie-Scores-and-Fixtures",
     "LEAGUE HOLANDIA 2026"),
    ("https://fbref.com/en/comps/17/2025-2026/schedule/2025-2026-Segunda-Division-Scores-and-Fixtures",
     "LEAGUE HISZPANIA 2 2026"),
    ("https://fbref.com/en/comps/12/2025-2026/schedule/2025-2026-La-Liga-Scores-and-Fixtures", "LEAGUE HISZPANIA 2026"),
    ("https://fbref.com/en/comps/60/2025-2026/schedule/2025-2026-Ligue-2-Scores-and-Fixtures", "LEAGUE FRANCJA 2 2026"),
    ("https://fbref.com/en/comps/13/2025-2026/schedule/2025-2026-Ligue-1-Scores-and-Fixtures", "LEAGUE FRANCJA 2026"),
    ("https://fbref.com/en/comps/11/2025-2026/schedule/2025-2026-Serie-A-Scores-and-Fixtures", "LEAGUE WŁOCHY 2026"),
    ("https://fbref.com/en/comps/18/2025-2026/schedule/2025-2026-Serie-B-Scores-and-Fixtures", "LEAGUE WŁOCHY 2 2026"),
    ("https://fbref.com/en/comps/9/2025-2026/schedule/2025-2026-Premier-League-Scores-and-Fixtures",
     "LEAGUE ANGLIA 2026"),
    ("https://fbref.com/en/comps/70/2025-2026/schedule/2025-2026-Saudi-Professional-League-Scores-and-Fixtures",
     "LEAGUE ARABIA 2026")
]



db_config = {
    'user': 'root',
    'password': 'j4pi3rd0l3',
    'host': 'localhost',
    'port': 3306,
    'database': 'football_scores'
}

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches_future (
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

def main():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    create_table(cursor)
    conn.commit()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    for url, league_name in urls_and_leagues:
        print(f"\n- {league_name}\n")

        driver.get(url)
        time.sleep(3)  # Wait for page to fully load

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Loop through rows in the schedule table
        rows = soup.find_all('tr')[1:]  # skip header row
        for row in rows:
            date_cell = row.find('td', {'data-stat': 'date'})
            if not date_cell:
                continue

            # Get date text from link if available, else skip
            date_link = date_cell.find('a')
            if date_link:
                match_date_str = date_link.text.strip()
                try:
                    match_date = datetime.strptime(match_date_str, "%Y-%m-%d").date()
                except ValueError:
                    # Date format not as expected, skip row
                    continue
            else:
                continue

            # Skip matches in the past
            if match_date < datetime.now().date():
                continue

            home_team_cell = row.find('td', {'data-stat': 'home_team'})
            away_team_cell = row.find('td', {'data-stat': 'away_team'})
            match_report_cell = row.find('td', {'data-stat': 'match_report'})

            if not (home_team_cell and away_team_cell and match_report_cell):
                continue

            home_team = home_team_cell.text.strip()
            away_team = away_team_cell.text.strip()
            match_report_link = match_report_cell.find('a')

            if match_report_link:
                match_report_url = f"https://fbref.com{match_report_link['href']}"
            else:
                match_report_url = None

            match_result = f"{home_team} : {away_team}"

            if match_report_url:
                cursor.execute('''
                    INSERT INTO matches_future (match_date, league_name, home_team, away_team, match_result, match_report_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (match_date, league_name, home_team, away_team, match_result, match_report_url))
                conn.commit()

                print(match_result)
                print(f"Match Report URL: {match_report_url}")

    driver.quit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
