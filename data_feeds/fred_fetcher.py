import pandas as pd
import requests
from datetime import datetime

FRED_API_KEY = "f4534c7eff90496:rvvfsfhx2op7027"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_series(series_id: str) -> pd.Series:
    url = f"{BASE_URL}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch {series_id}: {response.status_code}")

    data = response.json()["observations"]

    # Build Series
    series = {
        datetime.strptime(obs["date"], "%Y-%m-%d"): float(obs["value"])
        for obs in data if obs["value"] not in ("", ".")
    }

    return pd.Series(series, name=series_id).sort_index()
