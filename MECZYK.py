import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()  # imitacja przeglądarki
url = "https://fbref.com/en/comps/51/2025-2025/schedule/2025-2025-Eerste-Divisie-Scores-and-Fixtures"
html = scraper.get(url).text

soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
print(f"Liczba tabel: {len(tables)}")
