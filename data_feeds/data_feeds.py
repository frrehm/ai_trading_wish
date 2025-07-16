import pandas as pd
from data_feeds.fred_fetcher import fetch_fred_series

def fetch_ism_data():
    """
    Loads ISM PMI data from your local CSV.
    """
    df = pd.read_csv("data/ISM_PMI_Historical.csv", parse_dates=["Date"])
    df = df.set_index("Date").sort_index()
    return df

def get_all_indicators():
    # Load ISM PMI
    ism_df = fetch_ism_data()
    ism = ism_df["ISM_PMI"].copy()
    ism.name = "ISM_PMI"
    ism.index = pd.to_datetime(ism.index)

    # Fetch FRED indicators
    umcsent = fetch_fred_series("UMCSENT")
    housing = fetch_fred_series("HOUST")

    # Ensure all have datetime index
    umcsent.index = pd.to_datetime(umcsent.index)
    housing.index = pd.to_datetime(housing.index)

    # Rename
    umcsent.name = "UMCSI"
    housing.name = "HousingStarts"

    # Combine
    df = pd.concat([ism, umcsent, housing], axis=1)

    # Make sure index is datetime and sorted
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Monthly average
    df = df.dropna().resample("M").mean()
    return df
