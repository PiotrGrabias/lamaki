from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper(browser={"custom": "chrome", "platform": "windows", "mobile": False})
url = "https://www.whoscored.com/matches/1910678/live/germany-bundesliga-2025-2026-eintracht-frankfurt-borussia-dortmun'"
response = scraper.get(url)
soup = BeautifulSoup(response.text, "html.parser")
events = soup.select("div.match-centre-header-team-key-incident")
print(events)
