import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from data_feeds import data_feeds
import wish_engine
from wish_engine import analyzer

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

view = wish_engine.generate_worldview(df)

# Tabs for navigation
tab1, tab2 = st.tabs(["💹 WISH Assistant", "🧭 Macro Dashboard"])

with tab1:
    st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")

    # Load and process macro data
    with st.spinner("Fetching indicator data..."):
        df = data_feeds.get_all_indicators()

    # Create a simple worldview string from your data (example: use the last row)
    worldview_str = df.tail(1).to_string()

    # Generate and show the W.I.S.H. recommendation
    suggestion = analyzer.run_wish_analysis(worldview_str)
    st.markdown("### 🧠 AI-Generated WISH Strategy")
    st.success(suggestion)

with tab2:
    st.title("🧭 Macro Dashboard")
    st.markdown("Uses ISM, UMCSI, and Housing Starts to generate a macro 'Worldview'")

    with st.spinner("Fetching indicator data..."):
        df = data_feeds.get_all_indicators()

    # Plot indicators (see next section)
    chart = data_feeds.plot_indicators(df)
    st.plotly_chart(chart, use_container_width=True)

    st.dataframe(df.tail(3).round(2))

    st.markdown("### 🧠 Auto-Generated Worldview")
    view = wish_engine.generate_worldview(df)
    st.code(view)
