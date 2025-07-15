import pandas as pd
import requests
import plotly.graph_objects as go

FRED_API_KEY = "eff8f9962e5748f3998c10876408df4a"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_series(series_id):
    url = f"{BASE_URL}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()
    observations = data.get("observations", [])
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")["value"]

def get_all_indicators():
    ism = fetch_fred_series("ISM/MAN_PMI")
    umcsent = fetch_fred_series("UMCSENT")
    housing = fetch_fred_series("HOUST")
    df = pd.concat([
        ism.rename("ISM_PMI"),
        umcsent.rename("UMCSI"),
        housing.rename("HousingStarts")
    ], axis=1)
    df = df.dropna().resample("M").mean()
    return df

def plot_indicators(df):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
    fig.update_layout(title="Leading Indicators", xaxis_title="Date", yaxis_title="Value", height=500)
    return fig
