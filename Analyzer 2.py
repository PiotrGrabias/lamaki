from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector
import time
import os
import json

def parse_time(time_str):
    if '+' in time_str:
        base_time, extra_time = time_str.split('+')
        return int(base_time) + int(extra_time)
    return int(time_str)

def check_goal_pattern(soup):
    try:
        team_names_divs = soup.find_all("strong")
        if not team_names_divs:
            return False, False, False, None, None, None

        team_names = [strong.find("a").text for strong in team_names_divs if strong.find("a")]
        if len(team_names) < 2:
            return False, False, False, None, None, None

        team_a, team_b = team_names[0], team_names[1]
        goal_details = []

        stats_a = soup.find(id="a")
        stats_b = soup.find(id="b")

        def extract_goal_times(stats_div):
            goal_times = []
            if stats_div:
                for div in stats_div.find_all("div", recursive=False):
                    if (div.find("div", class_="event_icon goal") or
                        div.find("div", class_="event_icon penalty_goal") or
                        div.find("div", class_="event_icon own_goal")):

                        text = div.get_text(strip=True)
                        parts = text.split("·")
                        if len(parts) > 1:
                            time = parts[1].strip().replace("’", "")
                            goal_times.append(time)
            return goal_times

        goals_a = extract_goal_times(stats_a)
        goals_b = extract_goal_times(stats_b)

        for time_ in goals_a:
            t = time_.split("·")[-1].strip().replace("'", "").replace("’", "")
            goal_details.append((parse_time(t), team_a))

        for time_ in goals_b:
            t = time_.split("·")[-1].strip().replace("'", "").replace("’", "")
            goal_details.append((parse_time(t), team_b))

        if not goal_details:
            return False, False, False, team_a, team_b, None

        goal_details.sort(key=lambda x: x[0])

        score_a = score_b = 0
        one_team_leads = second_team_leads = one_team_leads_again = False
        team_a_lead_first = None

        for goal_time, team in goal_details:
            if team == team_a:
                score_a += 1
            else:
                score_b += 1

            if not one_team_leads:
                if score_a > score_b:
                    one_team_leads, team_a_lead_first = True, True
                elif score_b > score_a:
                    one_team_leads, team_a_lead_first = True, False

            if one_team_leads and not second_team_leads:
                if (team_a_lead_first and score_b > score_a) or (not team_a_lead_first and score_a > score_b):
                    second_team_leads = True

            if second_team_leads and not one_team_leads_again:
                if (team_a_lead_first and score_a > score_b) or (not team_a_lead_first and score_b > score_a):
                    one_team_leads_again = True

        return one_team_leads, second_team_leads, one_team_leads_again, team_a, team_b, goal_details

    except Exception as e:
        print("Error in goal pattern check:", e)
        return False, False, False, None, None, None

def create_tables(cursor, match_db):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS past_comebacks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_report_url VARCHAR(255),
            league_name VARCHAR(255),
            team_a VARCHAR(255),
            team_b VARCHAR(255),
            goal_details JSON,
            score VARCHAR(50),
            match_date DATE,
            comeback_type VARCHAR(50)
        )
    """)
    match_db.commit()

def insert_fixed_match(cursor, match_db, url, league_name, team_a, team_b, goal_details, score, date, comeback_type):
    goal_details_json = json.dumps(goal_details)
    sql = """
        INSERT INTO past_comebacks
        (match_report_url, league_name, team_a, team_b, goal_details, score, match_date, comeback_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (url, league_name, team_a, team_b, goal_details_json, score, date, comeback_type)
    cursor.execute(sql, val)
    match_db.commit()

def process_match(driver, url, league_name, cursor, match_db, score, date):
    try:
        driver.get(url)
        time.sleep(3)  # wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        one_team_leads, second_team_leads, one_team_leads_again, team_a, team_b, goal_details = check_goal_pattern(soup)

        if one_team_leads and second_team_leads:
            if one_team_leads_again:
                comeback_type = "three-phase"
                print(f"Three-phase comeback: {team_a} vs {team_b}")
            else:
                comeback_type = "two-phase"
                print(f"Two-phase comeback: {team_a} vs {team_b}")

            insert_fixed_match(cursor, match_db, url, league_name, team_a, team_b, goal_details, score, date, comeback_type)

    except Exception as e:
        print(f"Error processing {url}: {e}")

def get_offset():
    if os.path.exists('offset.txt'):
        with open('offset.txt', 'r') as file:
            return int(file.read().strip())
    return 0

def save_offset(offset):
    with open('offset.txt', 'w') as file:
        file.write(str(offset))

def main():
    # Selenium Chrome setup
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    # DB connection
    match_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="j4pi3rd0l3",
        database="football_scores"
    )
    cursor = match_db.cursor(buffered=True)

    # Ensure target tables exist
    create_tables(cursor, match_db)

    offset = get_offset()
    limit = 50

    while True:
        cursor.execute(f"SELECT match_report_url, league_name, score, match_date FROM past_matches LIMIT {offset}, {limit}")
        matches = cursor.fetchall()
        if not matches:
            print("No more matches.")
            break

        count = 0
        for url, league, score, date in matches:
            process_match(driver, url, league, cursor, match_db, score, date)
            count += 1
            print(f"Processed: {count}")
            time.sleep(5)

        offset += count
        save_offset(offset)

    driver.quit()
    match_db.close()

if __name__ == "__main__":
    main()
