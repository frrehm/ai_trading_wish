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
    ism_df = fetch_ism_data()
    ism = ism_df["ISM_PMI"]
    ism.name = "ISM_PMI"

    umcsent = fetch_fred_series("UMCSENT")
    umcsent.name = "UMCSI"

    housing = fetch_fred_series("HOUST")
    housing.name = "HousingStarts"

    df = pd.concat([ism, umcsent, housing], axis=1)
    df = df.dropna().resample("M").mean()
    return df
