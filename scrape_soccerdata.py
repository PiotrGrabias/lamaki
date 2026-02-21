import cloudscraper
import mysql.connector
from bs4 import BeautifulSoup
import datetime
import time
from datetime import datetime

scraper = cloudscraper.create_scraper(browser={"custom": "chrome", "platform": "windows", "mobile": False})


urls_and_leagues = [
    ("https://www.whoscored.com/regions/81/tournaments/3/seasons/10720/stages/24478/fixtures/germany-bundesliga-2025-2026",
     "LEAGUE NIEMCY 2025"),
]

desired_scores = [
    "1-2", "2-1", "3-1", "1-3", "2-3", "3-2", "3-3", "4-3", "3-4", "4-4",
    "4-5", "5-4", "5-2", "2-5", "5-3", "3-5", "2-4", "4-2", "5-5"
]

# --- Konfiguracja bazy ---
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
               CREATE TABLE IF NOT EXISTS nm_fixed_fresh
               (
                   id
                   INT
                   AUTO_INCREMENT
                   PRIMARY
                   KEY,
                   match_date
                   DATE,
                   league_name
                   VARCHAR
               (
                   255
               ),
                   home_team VARCHAR
               (
                   255
               ),
                   away_team VARCHAR
               (
                   255
               ),
                   score VARCHAR
               (
                   10
               ),
                   match_result VARCHAR
               (
                   255
               ),
                   match_report_url VARCHAR
               (
                   255
               )
                   )
               ''')

for url, league_name in urls_and_leagues:
    print(f"\n[INFO] Przetwarzanie ligi: {league_name}")
    try:
        response = scraper.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Nie udało się pobrać {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Wszystkie accordiony (grupy meczów wg daty)
    accordions = soup.find_all("div", class_=lambda c: c and c.startswith("Accordion-module_accordion__"))

    for accordion in accordions:
        header = accordion.find("div", class_=lambda c: c and c.startswith("Accordion-module_header__"))
        if header and header.span:
            date_text = header.span.text.strip()
            try:
                match_date_obj = datetime.strptime(date_text, "%A, %b %d %Y")
                match_date = match_date_obj.strftime("%Y-%m-%d")
            except Exception as e:
                print(f"[ERROR] Nie udało się sparsować daty '{date_text}': {e}")
                match_date = None
        else:
            match_date = None
        matches = accordion.find_all("div", class_=lambda c: c and c.startswith("Match-module_match__"))
        for match in matches:
            try:
                teams = match.find_all("div", class_=lambda c: c and c.startswith("Match-module_teamName__"))
                home_team = teams[0].get_text(strip=True) if len(teams) > 0 else None
                away_team = teams[1].get_text(strip=True) if len(teams) > 1 else None

                score_div = match.find("div", class_=lambda c: c and c.startswith("Match-module_scores__"))
                score_spans = score_div.find_all("span") if score_div else []
                score = "-".join([s.text.strip() for s in score_spans]) if score_spans else None

                match_report_a = match.find("a", class_=lambda c: c and c.startswith("Match-module_score__"))
                match_report_url = f"https://www.whoscored.com{match_report_a['href']}" if match_report_a else None

                match_result = f"{home_team} {score} : {away_team}"

                if score in desired_scores and match_report_url and match_date >= '2026-01-05':
                    print(f"[INFO] Zapis do bazy: {match_result} | URL: {match_report_url}")
                    cursor.execute('''
                                   INSERT INTO nm_fixed_fresh (match_date, league_name, home_team, away_team, score,
                                                               match_result, match_report_url)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                                   ''', (match_date, league_name, home_team, away_team, score, match_result,
                                         match_report_url))
                    conn.commit()

            except Exception as e:
                print(f"[ERROR] Błąd przy przetwarzaniu meczu: {e}")
                continue

    time.sleep(5)

cursor.close()
conn.close()
print("[INFO] Zakończono działanie skryptu.")
