import streamlit as st
import data_feeds.data_feeds as data_feeds
import wish_engine
from wish_engine import analyzer
import scraper.ism_fetcher as ism

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# Tabs for navigation
tab1, tab2 = st.tabs(["💹 WISH Assistant", "🧭 Macro Dashboard"])

# --- Tab 1: W.I.S.H. Assistant ---
with tab1:
    st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")
    worldview = st.text_input("🌍 Enter your macro view (e.g. 'Bullish US Growth')")

    if worldview:
        suggestion = analyzer.run_wish_analysis(worldview)
        st.success(suggestion)

# --- Tab 2: Macro Dashboard ---
with tab2:
    st.title("🧭 Macro Dashboard")
    st.markdown("Uses ISM, UMCSI, and Housing Starts to generate a macro 'Worldview'")

    with st.spinner("Fetching indicator data..."):
        df = data_feeds.get_all_indicators()

    st.plotly_chart(data_feeds.plot_indicators(df), use_container_width=True)
    st.dataframe(df.tail(3).round(2))

    st.markdown("### 🧠 Auto-Generated Worldview")
    view = wish_engine.generate_worldview(df)
    st.code(view)

    if st.button("🔁 Refresh ISM Data"):
        with st.spinner("Fetching latest ISM data..."):
            ism.full_ism_pipeline()
            st.success("✅ ISM data updated!")

