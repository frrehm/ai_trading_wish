def generate_worldview(df):
    latest = df.iloc[-1]
    trend = df.diff().rolling(3).mean().iloc[-1]

    signals = []

    # ISM Logic
    if latest['ISM_PMI'] > 50 and trend['ISM_PMI'] > 0:
        signals.append("ISM rising above 50 (Expansion)")
    else:
        signals.append("ISM weakening or below 50")

    # UMCSI Logic
    if latest['UMCSI'] > 85 and trend['UMCSI'] > 0:
        signals.append("Consumer sentiment strong and improving")
    else:
        signals.append("Weak or falling consumer sentiment")

    # Housing Starts vs. Trendline
    housing_trendline = df["HousingStarts"].rolling(window=12, min_periods=6).mean()
    latest_housing = df["HousingStarts"].iloc[-1]
    housing_trend = housing_trendline.iloc[-1]

    if latest_housing > housing_trend:
        signals.append("Housing starts above 12-month trendline (strength)")
    else:
        signals.append("Housing starts below 12-month trendline (weakness)")

    # Final Summary
    if all("above" in s or "rising" in s or "strong" in s for s in signals):
        summary = "All leading indicators suggest economic expansion. Consider long cyclicals or growth stocks."
    elif all("weak" in s or "below" in s for s in signals):
        summary = "All indicators show weakness. Defensive or hedged positions recommended."
    else:
        summary = "Mixed macro signals. Consider sector rotation or capital preservation."

    return "\n".join(signals) + "\n\n📈 Worldview: " + summary
