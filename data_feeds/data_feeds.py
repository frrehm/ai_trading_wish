import pandas as pd
import plotly.graph_objs as go
from data_feeds.fred_fetcher import fetch_fred_series

# --- Load ISM PMI from CSV ---
def fetch_ism_data():
    """
    Loads ISM PMI data from your local CSV.
    """
    df = pd.read_csv("data/ISM_PMI_Historical.csv", parse_dates=["Date"])
    df = df.set_index("Date").sort_index()
    return df


# --- Return indicators as separate Series ---
def get_all_indicators():
    # Load ISM PMI
    ism_df = fetch_ism_data()
    ism = ism_df["ISM_PMI"].copy()
    ism.name = "ISM_PMI"
    ism.index = pd.to_datetime(ism.index, errors='coerce')
    ism = ism[~ism.index.isnull()]
    ism = ism.resample("M").mean()

    # Fetch FRED indicators
    umcsent = fetch_fred_series("UMCSENT")
    housing = fetch_fred_series("HOUST")

    # Clean datetime
    umcsent.index = pd.to_datetime(umcsent.index, errors='coerce')
    housing.index = pd.to_datetime(housing.index, errors='coerce')
    umcsent = umcsent[~umcsent.index.isnull()]
    housing = housing[~housing.index.isnull()]

    # Rename and resample
    umcsent.name = "UMCSI"
    housing.name = "HousingStarts"
    umcsent = umcsent.resample("M").mean()
    housing = housing.resample("M").mean()

    return {
        "ISM_PMI": ism,
        "UMCSI": umcsent,
        "HousingStarts": housing
    }


# --- Plot each indicator on a separate Plotly chart ---
def plot_each_indicator(indicators: dict):
    figs = {}
    for name, series in indicators.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=series.index, y=series.values, mode='lines', name=name))
        fig.update_layout(
            title=name,
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_white"
        )
        figs[name] = fig
    return figs


# --- Optional: Original multi-line plot if needed ---
def plot_indicators_combined(indicators: dict):
    fig = go.Figure()
    for name, series in indicators.items():
        fig.add_trace(go.Scatter(x=series.index, y=series.values, mode='lines', name=name))
    fig.update_layout(
        title="Macro Indicators (Combined)",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_white"
    )
    return fig
