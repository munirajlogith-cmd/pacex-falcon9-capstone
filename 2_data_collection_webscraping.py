"""Lab 2: scrape Falcon 9 launch records from Wikipedia with BeautifulSoup."""
import requests
import pandas as pd
from bs4 import BeautifulSoup
from config import WIKI_URL

soup = BeautifulSoup(requests.get(WIKI_URL, timeout=30).text, "html.parser")
tables = soup.find_all("table", "wikitable plainrowheaders collapsible")

rows = []
for table in tables:
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        if len(cells) >= 8 and cells[0].isdigit():  # launch rows start with a flight number
            rows.append(cells[:9])

cols = ["Flight No.", "Date and time", "Version Booster", "Launch site",
        "Payload", "Payload mass", "Orbit", "Customer", "Launch outcome"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("spacex_web_scraped_mine.csv", index=False)
print(df.shape)
print(df.head())
