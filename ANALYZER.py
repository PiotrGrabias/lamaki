import cloudscraper
from bs4 import BeautifulSoup
import mysql.connector
import time
import os
import json
import traceback


# --- Funkcje pomocnicze ---

def parse_time(time_str):
    if '+' in time_str:
        base_time, extra_time = time_str.split('+')
        return int(base_time) + int(extra_time)
    return int(time_str)


def check_goal_pattern(soup, home_team_from_db, away_team_from_db):
    try:
        team_a = home_team_from_db
        team_b = away_team_from_db
        print(f"[DEBUG] Drużyny z bazy: {team_a} vs {team_b}")

        print("[DEBUG] Szukam div#live-incidents")
        incidents_div = soup.find("div", id="live-incidents")

        if not incidents_div:
            print("[DEBUG] Nie znaleziono live-incidents")
            return False, False, False, team_a, team_b, None

        goal_details = []

        print("[DEBUG] Iteruję po wszystkich wierszach tr w incidents")
        for tr in incidents_div.find_all("tr"):
            for side in ["home", "away"]:
                td = tr.find("td", class_=f"key-incident {side}-incident")
                if not td:
                    continue

                # Znajdź wszystkie wydarzenia GOL (data-type="16")
                goal_events = td.find_all("div", class_="match-centre-header-team-key-incident",
                                          attrs={"data-type": "16"})

                for event in goal_events:
                    # Pobierz minutę
                    icon_div = event.find("div", class_="incident-icon")
                    if icon_div and "data-minute" in icon_div.attrs:
                        goal_minute = int(icon_div["data-minute"])
                        goal_second = int(icon_div.get("data-second", 0))
                    else:
                        continue  # Pomijamy jeśli nie ma minuty

                    # Pobierz wynik po golu
                    current_score = None
                    current_score_span = event.find("span", class_="current-score")
                    if current_score_span:
                        current_score = current_score_span.text.strip("() \n\t")

                    # Zapisujemy tylko niezbędne informacje
                    goal_event = {
                        "minute": goal_minute,
                        "second": goal_second,
                        "team": side,  # "home" lub "away"
                        "score_after_goal": current_score
                    }
                    print(f"[DEBUG] Znaleziono gol: {side} w {goal_minute}' (wynik: {current_score})")
                    goal_details.append(goal_event)

        # Sortowanie goli po czasie
        goal_details.sort(key=lambda x: (x["minute"], x["second"]))

        # DEBUG: Wypisz wszystkie znalezione gole
        print(f"[DEBUG] Znaleziono {len(goal_details)} goli:")
        for idx, goal in enumerate(goal_details):
            team_name = team_a if goal["team"] == "home" else team_b
            print(f"  Gol {idx + 1}: {goal['minute']}' dla {team_name} (wynik: {goal['score_after_goal']})")

        # Sprawdź wzorce prowadzenia
        if not goal_details:
            print("[DEBUG] Nie znaleziono żadnych goli")
            return False, False, False, team_a, team_b, None

        score_a = score_b = 0
        one_team_leads = second_team_leads = one_team_leads_again = False
        team_a_lead_first = None

        print("[DEBUG] Obliczam leady:")
        for g in goal_details:
            if g["team"] == "home":
                score_a += 1
            else:
                score_b += 1

            current_score_display = g.get("score_after_goal", f"{score_a}-{score_b}")
            print(f"[DEBUG] {g['minute']}' - wynik: {current_score_display}")

            # Analiza prowadzenia
            if not one_team_leads:
                if score_a > score_b:
                    one_team_leads, team_a_lead_first = True, True
                    print(f"  → PIERWSZY LEAD: {team_a} prowadzi")
                elif score_b > score_a:
                    one_team_leads, team_a_lead_first = True, False
                    print(f"  → PIERWSZY LEAD: {team_b} prowadzi")

            elif one_team_leads and not second_team_leads:
                if (team_a_lead_first and score_b > score_a) or (not team_a_lead_first and score_a > score_b):
                    second_team_leads = True
                    leading_team = team_b if team_a_lead_first else team_a
                    print(f"  → DRUGI LEAD! {leading_team} przejmuje prowadzenie")

            elif second_team_leads and not one_team_leads_again:
                if (team_a_lead_first and score_a > score_b) or (not team_a_lead_first and score_b > score_a):
                    one_team_leads_again = True
                    leading_team = team_a if team_a_lead_first else team_b
                    print(f"  → TRZECI LEAD! {leading_team} odzyskuje prowadzenie")

        print(f"[DEBUG] Podsumowanie: "
              f"one_team_leads={one_team_leads}, "
              f"second_team_leads={second_team_leads}, "
              f"one_team_leads_again={one_team_leads_again}")

        return one_team_leads, second_team_leads, one_team_leads_again, team_a, team_b, goal_details

    except Exception as e:
        print(f"Error in goal pattern check: {e}")
        traceback.print_exc()
        return False, False, False, home_team_from_db, away_team_from_db, None


def insert_fixed_match(cursor, table_name, match_db, date, url, league_name, team_a, team_b, goal_details, score):
    try:
        goal_details_json = json.dumps(goal_details)
        print(f"[DEBUG] Wstawiam mecz do {table_name}: {team_a} vs {team_b}")
        sql = f"""
            INSERT INTO {table_name}
            (match_date, match_report_url, league_name, team_a, team_b, goal_details, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (date, url, league_name, team_a, team_b, goal_details_json, score)
        cursor.execute(sql, val)
        match_db.commit()
        print(f"[SUCCESS] Mecz dodany do {table_name}")
    except Exception as e:
        print(f"[ERROR] Błąd przy wstawianiu do {table_name}: {e}")
        match_db.rollback()


def process_match(date, url, league_name, cursor, match_db, score, scraper, home_team, away_team):
    print(f"[DEBUG] Przetwarzam mecz: {url} ({date}) - {home_team} vs {away_team}")
    try:
        html = scraper.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        # Przekazujemy drużyny z bazy danych do funkcji check_goal_pattern
        one_team_leads, second_team_leads, one_team_leads_again, team_a, team_b, goal_details = check_goal_pattern(soup,
                                                                                                                   home_team,
                                                                                                                   away_team)

        if one_team_leads and second_team_leads:
            table_name = "na_calego_2025" if one_team_leads_again else "lamaczki_2025"
            phase = "Three-phase comeback" if one_team_leads_again else "Two-phase comeback"
            print(f"[INFO] {phase}: {team_a} vs {team_b}")
            insert_fixed_match(cursor, table_name, match_db, date, url, league_name, team_a, team_b, goal_details,
                               score)
        else:
            print(f"[DEBUG] Mecz nie spełnia kryteriów comeback: {home_team} vs {away_team}")
    except Exception as e:
        print(f"[ERROR] Błąd przy przetwarzaniu meczu {url}: {e}")
        traceback.print_exc()


def get_offset():
    if os.path.exists('offset.txt'):
        with open('offset.txt', 'r') as file:
            return int(file.read().strip())
    return 0


def save_offset(offset):
    with open('offset.txt', 'w') as file:
        file.write(str(offset))


def create_tables(cursor):
    print("[DEBUG] Tworzenie tabel jeśli nie istnieją")
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS na_calego_2025
                   (
                       id
                       INT
                       AUTO_INCREMENT
                       PRIMARY
                       KEY,
                       match_date
                       DATE,
                       match_report_url
                       VARCHAR
                   (
                       255
                   ),
                       league_name VARCHAR
                   (
                       255
                   ),
                       team_a VARCHAR
                   (
                       255
                   ),
                       team_b VARCHAR
                   (
                       255
                   ),
                       goal_details JSON,
                       score VARCHAR
                   (
                       10
                   )
                       )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS lamaczki_2025
                   (
                       id
                       INT
                       AUTO_INCREMENT
                       PRIMARY
                       KEY,
                       match_date
                       DATE,
                       match_report_url
                       VARCHAR
                   (
                       255
                   ),
                       league_name VARCHAR
                   (
                       255
                   ),
                       team_a VARCHAR
                   (
                       255
                   ),
                       team_b VARCHAR
                   (
                       255
                   ),
                       goal_details JSON,
                       score VARCHAR
                   (
                       10
                   )
                       )
                   """)


# --- Główny skrypt ---
def main():
    print("[DEBUG] Łączenie z bazą")
    match_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="j4pi3rd0l3",
        database="football_scores"
    )

    cursor = match_db.cursor(buffered=True)
    create_tables(cursor)
    match_db.commit()

    scraper = cloudscraper.create_scraper()

    offset = get_offset()
    limit = 50

    while True:
        print(f"[DEBUG] Pobieram mecze z offset={offset}, limit={limit}")
        cursor.execute(f"""
            SELECT match_date, match_report_url, league_name, score, home_team, away_team 
            FROM nm_fixed_fresh 
            LIMIT {offset}, {limit}
        """)
        matches = cursor.fetchall()

        if not matches:
            print("[INFO] Brak więcej meczów do przetworzenia")
            break

        count = 0
        for date, url, league_name, score, home_team, away_team in matches:
            try:
                process_match(date, url, league_name, cursor, match_db, score, scraper, home_team, away_team)
                count += 1
                print(f"[DEBUG] Przetworzono {count} meczów w tej partii")
                time.sleep(3)  # Mniejsze opóźnienie dla testów
            except Exception as e:
                print(f"[ERROR] Błąd przy przetwarzaniu {url}: {e}")
                traceback.print_exc()
                continue

        offset += count
        save_offset(offset)
        print(f"[DEBUG] Nowy offset zapisany: {offset}")

        # Przerwa między partiami
        if count > 0:
            print("[DEBUG] Przerwa między partiami...")
            time.sleep(10)

    match_db.close()
    print("[INFO] Skrypt zakończył działanie")


if __name__ == "__main__":
    main()