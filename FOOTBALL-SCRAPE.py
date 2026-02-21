import cloudscraper
import mysql.connector
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import random

scraper = cloudscraper.create_scraper(browser={"custom": "chrome", "platform": "windows", "mobile": False})

today = datetime.date.today()

urls_and_leagues = [

    ("https://www.whoscored.com/regions/233/tournaments/85/seasons/10957/stages/24960/fixtures/usa-major-league-soccer-2026", "LEAGUE USA 2025"),
   ("https://www.whoscored.com/regions/155/tournaments/66/seasons/10789/stages/24601/fixtures/netherlands-eerste-divisie-2025-2026", "LEAGUE HOLANDIA 2 2025"),
           ("https://www.whoscored.com/regions/15/tournaments/32/seasons/10777/stages/24571/fixtures/austria-bundesliga-2025-2026", "LEAGUE AUSTRIA 2025"),
         ("https://www.whoscored.com/regions/22/tournaments/18/seasons/10759/stages/24549/fixtures/belgium-jupiler-pro-league-2025-2026", "LEAGUE BELGIA 2025"),
     ("https://www.whoscored.com/regions/22/tournaments/137/seasons/10823/stages/24657/fixtures/belgium-second-division-2025-2026", "LEAGUE BELGIA 2 2025"),
    ("https://www.whoscored.com/regions/81/tournaments/3/seasons/10720/stages/24478/fixtures/germany-bundesliga-2025-2026", "LEAGUE NIEMCY 2025"),
("https://www.whoscored.com/regions/81/tournaments/6/seasons/10721/stages/24479/fixtures/germany-2-bundesliga-2025-2026", "LEAGUE NIEMCY 2 2025"),
    ("https://www.whoscored.com/regions/252/tournaments/7/seasons/10784/stages/24580/fixtures/england-championship-2025-2026", "LEAGUE ANGLIA 2 2025"),
         ("https://www.whoscored.com/regions/55/tournaments/82/seasons/10751/stages/24541/fixtures/croatia-prva-hnl-2025-2026", "LEAGUE CHORWACJA 2025"),
        ("https://www.whoscored.com/regions/58/tournaments/78/seasons/10757/stages/24547/fixtures/czech-republic-gambrinus-league-2025-2026", "LEAGUE CZECHY 2025"),
         ("https://www.whoscored.com/regions/59/tournaments/1/seasons/10730/stages/24498/fixtures/denmark-superliga-2025-2026", "LEAGUE DANIA 2025"),
("https://www.whoscored.com/regions/201/tournaments/79/seasons/10796/stages/24614/fixtures/slovenia-prva-liga-2025-2026", "LEAGUE SŁOWENIA 2025"),
         ("https://www.whoscored.com/regions/176/tournaments/76/seasons/10733/stages/24501/fixtures/poland-ekstraklasa-2025-2026", "LEAGUE POLSKA 2025"),
("https://www.whoscored.com/regions/176/tournaments/232/seasons/10756/stages/24546/fixtures/poland-i-liga-2025-2026", "LEAGUE POLSKA 2 2025"),
         ("https://www.whoscored.com/regions/155/tournaments/13/seasons/10752/stages/24542/fixtures/netherlands-eredivisie-2025-2026", "LEAGUE HOLANDIA 2025"),
    ("https://www.whoscored.com/regions/206/tournaments/63/seasons/10804/stages/24623/fixtures/spain-segunda-divisi%C3%B3n-2025-2026", "LEAGUE HISZPANIA 2 2025"),
    ("https://www.whoscored.com/regions/206/tournaments/4/seasons/10803/stages/24622/fixtures/spain-laliga-2025-2026", "LEAGUE HISZPANIA 2025"),
    ("https://www.whoscored.com/regions/74/tournaments/37/seasons/10793/stages/24610/fixtures/france-ligue-2-2025-2026", "LEAGUE FRANCJA 2 2025"),
    ("https://www.whoscored.com/regions/74/tournaments/22/seasons/10792/stages/24609/fixtures/france-ligue-1-2025-2026", "LEAGUE FRANCJA 2025"),
    ("https://www.whoscored.com/regions/108/tournaments/5/seasons/10732/stages/24500/fixtures/italy-serie-a-2025-2026", "LEAGUE WŁOCHY 2025"),
    ("https://www.whoscored.com/regions/108/tournaments/19/seasons/10866/stages/24726/fixtures/italy-serie-b-2025-2026", "LEAGUE WŁOCHY 2 2025"),
    ("https://www.whoscored.com/regions/252/tournaments/2/seasons/10743/stages/24533/fixtures/england-premier-league-2025-2026", "LEAGUE ANGLIA 2025"),
    ("https://www.whoscored.com/regions/177/tournaments/21/seasons/10774/stages/24568/fixtures/portugal-liga-2025-2026", "LEAGUE PORTUGALIA 2025"),
("https://www.whoscored.com/regions/177/tournaments/139/seasons/10775/stages/24569/fixtures/portugal-liga-2-2025-2026", "LEAGUE PORTUGALIA 2 2025"),
     ("https://www.whoscored.com/regions/99/tournaments/75/seasons/10748/stages/24538/fixtures/hungary-nb-i-2025-2026", "LEAGUE WĘGRY 2025"),
     ("https://www.whoscored.com/regions/181/tournaments/121/seasons/10783/stages/24579/fixtures/romania-superliga-2025-2026", "LEAGUE RUMUNIA 2025"),
     ("https://www.whoscored.com/regions/196/tournaments/80/seasons/10742/stages/24531/fixtures/serbia-super-liga-2025-2026", "LEAGUE SERBIA 2025"),
     ("https://www.whoscored.com/regions/230/tournaments/114/seasons/10779/stages/24573/fixtures/ukraine-premier-league-2025-2026", "LEAGUE UKRAINA 2025"),
     ("https://www.whoscored.com/regions/34/tournaments/119/seasons/10724/stages/24484/fixtures/bulgaria-a-pfg-2025-2026",
      "LEAGUE BULGARIA 2025"),
    ("https://www.whoscored.com/regions/14/tournaments/194/seasons/10863/stages/24719/fixtures/australia-a-league-2025-2026", "LEAGUE AUSTRALIA 2025"),
("https://www.whoscored.com/regions/194/tournaments/282/seasons/10887/stages/24760/fixtures/saudi-arabia-pro-league-2025-2026", "LEAGUE ARABIA 2025"),
         ("https://www.whoscored.com/regions/213/tournaments/33/seasons/10766/stages/24557/fixtures/switzerland-super-league-2025-2026","LEAGUE SZWAJCARIA 2025"),
    ("https://www.whoscored.com/regions/253/tournaments/20/seasons/10760/stages/24550/fixtures/scotland-premiership-2025-2026", "LEAGUE SZKOCJA 2025"),
         ("https://www.whoscored.com/regions/225/tournaments/17/seasons/10807/stages/24627/fixtures/turkey-super-lig-2025-2026", "LEAGUE TURCJA 2025"),
("https://www.whoscored.com/regions/260/tournaments/387/seasons/11002/south-korea-k-league-1", "LEAGUE KOREA 2025"),
("https://www.whoscored.com/regions/260/tournaments/418/seasons/11012/south-korea-k-league-2", "LEAGUE KOREA 2 2025"),
       ("https://www.whoscored.com/regions/212/tournaments/40/seasons/10986/stages/25046/fixtures/sweden-allsvenskan-2026", "LEAGUE SZWECJA 2025-2025"),
      ("https://www.whoscored.com/regions/212/tournaments/48/seasons/10998/sweden-superettan", "LEAGUE SZWECJA 2 2025-2025"),
        ("https://www.whoscored.com/regions/110/tournaments/324/seasons/10560/stages/23985/fixtures/japan-j-league-2-2025", "LEAGUE JAPONIA 2 2025"), #POPRAW SEZON BLIZEJ
       ("https://www.whoscored.com/regions/110/tournaments/150/seasons/10997/stages/25067/fixtures/japan-j-league-2026", "LEAGUE JAPONIA 2025"),
       ("https://www.whoscored.com/regions/165/tournaments/41/seasons/10983/stages/25043/fixtures/norway-eliteserien-2026", "LEAGUE NORWEGIA 2025-2025"),
       ("https://www.whoscored.com/regions/165/tournaments/50/seasons/10984/norway-1-division", "LEAGUE NORWEGIA 2 2025-2025"),
       ("https://www.whoscored.com/regions/73/tournaments/43/seasons/11008/stages/25099/fixtures/finland-veikkausliiga-2026", "LEAGUE FINLANDIA 2025-2025"),
    ("https://www.whoscored.com/regions/45/tournaments/162/seasons/10611/stages/24090/fixtures/china-super-league-2025", "LEAGUE CHINY 2025"), #POPRAW SEZON


]

# --- Wyniki, które nas interesują ---
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
CREATE TABLE IF NOT EXISTS nm_fixed_fresh (
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
    print(f"\n[INFO] Przetwarzanie ligi: {league_name}")
    try:
        response = scraper.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Nie udało się pobrać {url}: {e}")
        continue

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")
    print(f"[DEBUG] Liczba tabel: {len(tables)}")

    if not tables:
        print(f"[SKIP] Brak tabeli na stronie {url}")
        continue

    table = tables[0]
    rows = table.find_all('tr')
    print(f"[DEBUG] Liczba znalezionych wierszy w tabeli: {len(rows)}")

    for idx, row in enumerate(rows[1:], start=1):
        date_time = row.find('td', {'data-stat': 'date'})
        if not date_time or not date_time.find('a'):
            continue

        date = date_time.find('a').text.strip()

        home_team_cell = row.find('td', {'data-stat': 'home_team'})
        score_cell = row.find('td', {'data-stat': 'score'})
        away_team_cell = row.find('td', {'data-stat': 'away_team'})
        match_report_cell = row.find('td', {'data-stat': 'match_report'})

        if not (home_team_cell and score_cell and away_team_cell and match_report_cell):
            continue

        home_team = home_team_cell.text.strip()
        score = score_cell.find('a').text.strip() if score_cell.find('a') else score_cell.text.strip()
        score = score.replace('–', '-').strip()
        away_team = away_team_cell.text.strip()
        match_report_url = match_report_cell.find('a')['href'] if match_report_cell.find('a') else None
        match_result = f"{home_team} {score} : {away_team}"

        if score in desired_scores and match_report_url and date >= '2026-01-05':
            match_report_url = f"https://fbref.com{match_report_url}"
            print(f"[INFO] Zapis do bazy: {match_result} | URL: {match_report_url}")
            cursor.execute('''
                INSERT INTO nm_fixed_fresh (match_date, league_name, home_team, away_team, score, match_result, match_report_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (date, league_name, home_team, away_team, score, match_result, match_report_url))
            conn.commit()

    time.sleep(6)

cursor.close()
conn.close()
print("[INFO] Zakończono działanie skryptu.")