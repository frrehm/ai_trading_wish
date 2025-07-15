import pandas as pd
import requests
import plotly.graph_objects as go
import os

from scraper.ism_fetcher import fetch_latest_ism_data

# === Constants ===
FRED_API_KEY = "eff8f9962e5748f3998c10876408df4a"
BASE_URL_FRED = "https://api.stlouisfed.org/fred/series/observations"
CSV_PATH = "data/ISM_PMI_Historical.csv"

# === Load Historical ISM CSV ===
def fetch_ism_historical():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, parse_dates=["Date"]).set_index("Date").sort_index()
        return df
    else:
        raise FileNotFoundError("ISM historical CSV not found at: data/ISM_PMI_Historical.csv")

# === Live + Historical ISM Merge ===
def fetch_combined_ism():
    df_hist = fetch_ism_historical()

    try:
        latest = fetch_latest_ism_data()
        latest_date = pd.to_datetime(latest["date"])
        if latest_date not in df_hist.index:
            df_hist.loc[latest_date] = latest["pmi"]
    except Exception as e:
        print("⚠️ Could not fetch latest ISM data:", e)

    return df_hist.sort_index()

# === FRED Series Pull ===
def fetch_fred_series(series_id):
    url = f"{BASE_URL_FRED}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)

    if "application/json" not in response.headers.get("Content-Type", ""):
        raise ValueError("❌ FRED returned non-JSON response:\n" + response.text[:300])

    data = response.json()
    observations = data.get("observations", [])
    if not observations:
        raise ValueError(f"No data returned for series ID: {series_id}")

    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")["value"]

# === Final Combined Indicator DataFrame ===
def get_all_indicators():
    ism = fetch_combined_ism()
    umcsent = fetch_fred_series("UMCSENT")
    housing = fetch_fred_series("HOUST")

    df = pd.concat([
        ism.rename("ISM_PMI"),
        umcsent.rename("UMCSI"),
        housing.rename("HousingStarts")
    ], axis=1)

    df = df.dropna().resample("M").mean()
    return df

# === Plotting ===
def plot_indicators(df):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
    fig.update_layout(title="Leading Indicators", xaxis_title="Date", yaxis_title="Value", height=500)
    return fig

