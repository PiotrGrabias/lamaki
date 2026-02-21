from datetime import date, datetime
import time
import mysql.connector
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from variables import seasons, leagues

# --- Setup Selenium ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # no browser window
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

today = date.today()
print(f"Today's date: {today}")

# --- Przygotowanie URL ---
urls_and_leagues = []
for comp_id, league in leagues:
    for season in seasons:
        url = f"https://fbref.com/en/comps/{comp_id}/{season}/schedule/{season}-{league}-Scores-and-Fixtures"
        urls_and_leagues.append((url, league))
        print(f"Added URL for league {league}, season {season}: {url}")

# --- Połączenie z bazą ---
db_config = {
    'user': 'root',
    'password': 'j4pi3rd0l3',
    'host': 'localhost',
    'port': 3306,
    'database': 'football_scores'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

desired_scores = [
    "1-2", "2-1", "3-1", "1-3", "2-3", "3-2", "3-3", "4-3", "3-4", "4-4",
    "4-5", "5-4", "5-2", "2-5", "5-3", "3-5", "2-4", "4-2", "5-5"
]

cursor.execute('''
CREATE TABLE IF NOT EXISTS past_matches (
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

# --- Główna pętla ---
for url, league_name in urls_and_leagues:
    print(f"\nOpening URL: {url} for league {league_name}")
    driver.get(url)
    time.sleep(2)  # give JS time to render
    soup = BeautifulSoup(driver.page_source, "html.parser")

    print(f"Page loaded, parsing rows for {league_name}...")

    # FBref często ukrywa tabele w komentarzach HTML
    rows = []
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment, 'html.parser')
        table = comment_soup.find('table')
        if table:
            rows.extend(table.find_all('tr')[1:])  # pomijamy nagłówek

    print(f"Found {len(rows)} rows in table.")

    for i, row in enumerate(rows, start=1):
        date_cell = row.find('td', {'data-stat': 'date'})
        if not date_cell:
            continue

        date_link = date_cell.find('a')
        if date_link:
            try:
                match_date = datetime.strptime(date_link.text.strip(), "%b %d, %Y").date()
            except ValueError:
                continue
        else:
            continue

        if match_date > today:
            continue  # pomijamy przyszłe mecze

        home_team_cell = row.find('td', {'data-stat': 'home_team'})
        away_team_cell = row.find('td', {'data-stat': 'away_team'})
        score_cell = row.find('td', {'data-stat': 'score'})
        match_report_cell = row.find('td', {'data-stat': 'match_report'})

        if not all([home_team_cell, away_team_cell, score_cell, match_report_cell]):
            continue

        home_team = home_team_cell.text.strip()
        away_team = away_team_cell.text.strip()
        score = score_cell.find('a').text.strip() if score_cell.find('a') else score_cell.text.strip()
        score = score.replace('–', '-').strip()
        match_report_url = match_report_cell.find('a')['href'] if match_report_cell.find('a') else None
        match_result = f"{home_team} {score} : {away_team}"

        if score in desired_scores and match_report_url:
            match_report_url = f"https://fbref.com{match_report_url}"
            cursor.execute('''
                INSERT INTO past_matches (match_date, league_name, home_team, away_team, score, match_result, match_report_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (match_date, league_name, home_team, away_team, score, match_result, match_report_url))
            conn.commit()
            print(f"Inserted: {match_result}")
        else:
            print(f"Skipped: {match_result} (score not desired or no report URL)")

cursor.close()
conn.close()
driver.quit()
print("\nAll done.")
