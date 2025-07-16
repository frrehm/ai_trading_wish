# data_feeds/fred_fetcher.py
import pandas as pd
import requests

API_KEY = "eff8f9962e5748f3998c10876408df4a"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_series(series_id):
    url = f"{BASE_URL}?series_id={series_id}&api_key={API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()

    observations = data.get("observations", [])
    if not observations:
        raise ValueError(f"No data returned for series ID: {series_id}")
    
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")["value"]
