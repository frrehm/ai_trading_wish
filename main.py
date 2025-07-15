import streamlit as st
from wish_engine import analyzer
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from data_feeds import leading_indicators

from wish_engine import worldview_generator

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# Tabs for navigation
tab1, tab2 = st.tabs(["💹 WISH Assistant", "🧭 Macro Dashboard"])

with tab1:
    st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")
    worldview = st.text_input("🌍 Enter your macro view (e.g. 'Bullish US Growth')")

    if worldview:
        suggestion = analyzer.run_wish_analysis(worldview)
        st.success(suggestion)

with tab2:
    st.title("🧭 Macro Dashboard")
    st.markdown("Uses ISM, UMCSI, and Housing Starts to generate a macro 'Worldview'")

    # Load data
    with st.spinner("Fetching indicator data..."):
        df = leading_indicators.get_all_indicators()

    # Plot chart
    st.plotly_chart(leading_indicators.plot_indicators(df), use_container_width=True)

    # Show latest values
    st.dataframe(df.tail(3).round(2))

    # Generate and display worldview
    st.markdown("### 🧠 Auto-Generated Worldview")
    view = worldview_generator.generate_worldview(df)
    st.code(view)
