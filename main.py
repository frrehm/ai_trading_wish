import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import scraper.ism_fetcher as ism
import streamlit as st
from data_feeds import data_feeds
import wish_engine
from wish_engine import analyzer
import pandas as pd

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# Tabs for navigation
tab1, tab2 = st.tabs(["💹 WISH Assistant", "🧭 Macro Dashboard"])

with tab1:
    st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")

    # Load and process macro data
    with st.spinner("Fetching indicator data..."):
        ism.full_ism_pipeline()  # 🔄 Update the CSV with the latest ISM data
        indicators = data_feeds.get_all_indicators()

    # Combine all indicators into a DataFrame
    df = pd.concat(indicators.values(), axis=1)
    df.columns = indicators.keys()
    df = df.dropna()

    # Create worldview string from last row
    worldview_str = df.tail(1).to_string()

    # Generate and show the W.I.S.H. recommendation
    suggestion = analyzer.run_wish_analysis(worldview_str)
    st.markdown("### 🧠 AI-Generated WISH Strategy")
    st.success(suggestion)

with tab2:
    st.title("🧭 Macro Dashboard")
    st.markdown("Uses ISM, UMCSI, and Housing Starts to generate a macro 'Worldview'")

    with st.spinner("Fetching indicator data..."):
        indicators = data_feeds.get_all_indicators()

    # Plot each indicator separately
    charts = data_feeds.plot_each_indicator(indicators)
    for name, fig in charts.items():
        st.subheader(name)
        st.plotly_chart(fig, use_container_width=True)

    # Show the latest values
    latest = {name: series.dropna().iloc[-1] for name, series in indicators.items()}
    latest_df = pd.DataFrame(latest, index=["Latest"]).T.round(2)
    st.dataframe(latest_df)

    # Generate and show Worldview from full combined DataFrame
    full_df = pd.concat(indicators.values(), axis=1)
    full_df.columns = indicators.keys()
    full_df = full_df.dropna()

    st.markdown("### 🧠 Auto-Generated Worldview")
    view = wish_engine.generate_worldview(full_df)
    st.code(view)

st.write("✅ ISM_PMI Preview:")
st.write(indicators["ISM_PMI"].dropna().tail())

