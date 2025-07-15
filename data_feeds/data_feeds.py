# data_feeds/data_feeds.py

import pandas as pd
import requests
import plotly.graph_objects as go
from scraper.ism_fetcher import fetch_latest_ism_data

# === FRED API ===
FRED_API_KEY = "eff8f9962e5748f3998c10876408df4a"
BASE_URL_FRED = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_series(series_id):
    url = f"{BASE_URL_FRED}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()
    observations = data.get("observations", [])
    if not observations:
        raise ValueError(f"No data returned for series ID: {series_id}")
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")["value"]

def fetch_ism_data():
    # Load historical CSV
    df = pd.read_csv("data/ISM_PMI_Historical.csv", parse_dates=["Date"])
    df = df.set_index("Date").sort_index()

    # Try appending latest data (in memory only)
    try:
        latest = fetch_latest_ism_data()
        latest_date = pd.to_datetime(latest["date"])
        if latest_date not in df.index:
            df.loc[latest_date] = latest["pmi"]
            df = df.sort_index()
    except Exception as e:
        print("⚠️ Could not fetch latest ISM data:", e)

    return df

def get_all_indicators():
    ism_df = fetch_ism_data()
    ism = ism_df.iloc[:, 0]
    ism.name = "ISM_PMI"

    umcsent = fetch_fred_series("UMCSENT")
    umcsent.name = "UMCSI"

    housing = fetch_fred_series("HOUST")
    housing.name = "HousingStarts"

    df = pd.concat([ism, umcsent, housing], axis=1)
    df = df.dropna().resample("M").mean()
    return df

def plot_indicators(df):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
    fig.update_layout(title="Leading Indicators", xaxis_title="Date", yaxis_title="Value", height=500)
    return fig
