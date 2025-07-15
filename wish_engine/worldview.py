import pandas as pd

def generate_worldview(df: pd.DataFrame) -> str:
    """
    Generates a simple macroeconomic worldview based on ISM, UMCSI, and Housing Starts.
    """
    latest = df.iloc[-1]

    view = []

    if latest["ISM_PMI"] > 50:
        view.append("Manufacturing expanding (ISM above 50)")
    else:
        view.append("Manufacturing contracting (ISM below 50)")

    if latest["UMCSI"] > 70:
        view.append("Strong consumer sentiment (UMCSI high)")
    elif latest["UMCSI"] < 60:
        view.append("Weak consumer sentiment (UMCSI low)")
    else:
        view.append("Consumer sentiment stable")

    if latest["HousingStarts"] > df["HousingStarts"].mean():
        view.append("Housing starts above average")
    else:
        view.append("Housing starts below average")

    return " | ".join(view)
