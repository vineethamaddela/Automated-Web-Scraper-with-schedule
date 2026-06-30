import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import schedule
import time

def scrape():
    url = "https://quotes.toscrape.com"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    # SQLite Database
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT,
        author TEXT
    )
    """)

    # CSV File
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author"])

        for q in quotes:
            quote = q.find("span", class_="text").text
            author = q.find("small", class_="author").text

            print("Quote:", quote)
            print("Author:", author)
            print("-" * 40)

            # Save to CSV
            writer.writerow([quote, author])

            # Save to SQLite
            cursor.execute(
                "INSERT INTO quotes (quote, author) VALUES (?, ?)",
                (quote, author)
            )

    conn.commit()
    conn.close()

    print("Data saved to quotes.csv")
    print("Data saved to quotes.db")
    print("Waiting for next schedule...\n")


# Run every 1 minute
schedule.every(1).minutes.do(scrape)

print("Automated Web Scraper Started...")
print("Press Stop button to exit.\n")

# First run immediately
scrape()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(1)
