# scraper/ism_fetcher.py
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import os

from nlp.comment_interpreter import interpret_ism_comments

PMI_URL = "https://www.ismworld.org/supply-management-news-and-reports/reports/pmi/"
CSV_PATH = "data/ISM_PMI_Historical.csv"


def fetch_latest_ism_data():
    response = requests.get(PMI_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find headline PMI number (look for the pattern like 'PMI® at 49.0%')
    pmi_text = soup.find(text=re.compile(r"PMI.*?\d+\.\d+%"))
    match = re.search(r"(\d+\.\d+)%", pmi_text)
    pmi_value = float(match.group(1)) if match else None

    # Extract the publication date from the page
    date_tag = soup.find("div", class_="article-date")
    if date_tag:
        date_str = date_tag.text.strip()
        try:
            report_date = datetime.strptime(date_str, "%B %d, %Y")
        except:
            report_date = datetime.today()
    else:
        report_date = datetime.today()

    # Extract panelist comments section
    comments_section = soup.find("div", class_="panelist-comments")
    comments_text = comments_section.get_text(strip=True) if comments_section else ""

    return {
        "date": report_date.strftime("%Y-%m-%d"),
        "pmi": pmi_value,
        "comments": comments_text
    }


def update_ism_csv(new_data):
    # Load existing CSV if available
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
        df = df.set_index("Date")
    else:
        df = pd.DataFrame(columns=["Date", "ISM_PMI"])
        df = df.set_index("Date")

    date = pd.to_datetime(new_data["date"])
    if date not in df.index:
        df.loc[date] = new_data["pmi"]
        df = df.sort_index()
        df.to_csv(CSV_PATH)
        print("✅ New PMI data appended to CSV.")
    else:
        print("ℹ️ PMI data for this date already exists.")


def full_ism_pipeline():
    data = fetch_latest_ism_data()
    update_ism_csv(data)

    print("\n📊 ISM PMI Report:")
    print("Date:", data["date"])
    print("PMI:", data["pmi"])
    print("\n🗨️ Comments:")
    print(data["comments"][:500], "...\n")

    print("🤖 AI Interpretation:")
    sentiment = interpret_ism_comments(data["comments"])
    for sector, view in sentiment.items():
        icon = "🔼" if view == "Bullish" else "🔽" if view == "Bearish" else "⚖️"
        print(f"{icon} {sector}: {view}")


if __name__ == "__main__":
    full_ism_pipeline()


# nlp/comment_interpreter.py

def interpret_ism_comments(comments: str) -> dict:
    """
    Simulate AI analysis of ISM panelist comments.
    In production: use OpenAI or local LLM for true NLP.
    """
    sector_sentiment = {}
    
    example_sectors = [
        "Technology", "Construction", "Food & Beverage", "Healthcare",
        "Finance", "Retail", "Transportation", "Automotive"
    ]

    comments_lower = comments.lower()

    for sector in example_sectors:
        if sector.lower() in comments_lower:
            if any(word in comments_lower for word in ["strong", "growth", "expanding", "increasing"]):
                sentiment = "Bullish"
            elif any(word in comments_lower for word in ["decline", "weak", "shrinking", "slow"]):
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            sector_sentiment[sector] = sentiment

    return sector_sentiment


# ✅ Add this to main.py under your leading indicator chart
import scraper.ism_fetcher as ism

if st.button("🔁 Refresh ISM Data"):
    with st.spinner("Fetching latest ISM data..."):
        ism.full_ism_pipeline()
        st.success("✅ ISM data updated!")

