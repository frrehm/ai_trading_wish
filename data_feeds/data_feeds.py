# data_feeds/data_feeds.py
import pandas as pd
from scraper.ism_fetcher import fetch_ism_data
from data_feeds.fred_fetcher import fetch_fred_series  # make sure this exists

def get_all_indicators():
    # Load ISM PMI from CSV
    ism_df = fetch_ism_data()
    ism = ism_df["ISM_PMI"]
    ism.name = "ISM_PMI"

    # Fetch FRED indicators
    umcsent = fetch_fred_series("UMCSENT")
    umcsent.name = "UMCSI"

    housing = fetch_fred_series("HOUST")
    housing.name = "HousingStarts"

    # Combine
    df = pd.concat([ism, umcsent, housing], axis=1)
    df = df.dropna().resample("M").mean()
    return df

def plot_indicators(df):
    import plotly.graph_objects as go
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode="lines", name=col))
    fig.update_layout(title="Leading Indicators", xaxis_title="Date", yaxis_title="Value")
    return fig

