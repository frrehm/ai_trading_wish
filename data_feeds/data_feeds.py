import pandas as pd
import requests
from .fred_fetcher import fetch_fred_series
from scraper.ism_fetcher import fetch_ism_data

def get_all_indicators():
    # Fetch ISM PMI Series
    ism_df = fetch_ism_data()              # returns a DataFrame
    ism = ism_df.iloc[:, 0]                # convert 1-column DataFrame to Series
    ism.name = "ISM_PMI"

    # Fetch other indicators
    umcsent = fetch_fred_series("UMCSENT")
    umcsent.name = "UMCSI"

    housing = fetch_fred_series("HOUST")
    housing.name = "HousingStarts"

    # Combine and clean
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
