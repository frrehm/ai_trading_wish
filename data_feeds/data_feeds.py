import pandas as pd
import requests
import plotly.graph_objects as go
import os

# === API Keys ===
TRADING_ECON_API_KEY = "f4534c7eff90496:rvvfsfhx2op7027"
FRED_API_KEY = "eff8f9962e5748f3998c10876408df4a"
BASE_URL_FRED = "https://api.stlouisfed.org/fred/series/observations"

# === ISM PMI from CSV + Trading Economics ===
def fetch_ism_historical():
    df = pd.read_csv("data/ISM_PMI_Historical.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    return df

def fetch_te_ism_pmi():
    url = f"https://api.tradingeconomics.com/historical/country/united states/indicator/ISM Manufacturing PMI?c={TRADING_ECON_API_KEY}&f=json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[["Date", "Value"]].rename(columns={"Value": "ISM_PMI"})
    df.set_index("Date", inplace=True)
    return df.sort_index()

def fetch_combined_ism():
    df_hist = fetch_ism_historical()
    df_live = fetch_te_ism_pmi()
    df_combined = pd.concat([df_hist, df_live[~df_live.index.isin(df_hist.index)]])
    return df_combined.sort_index()

# === FRED Series ===
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

# === Main DataFrame Builder ===
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
