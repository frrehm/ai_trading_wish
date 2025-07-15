import streamlit as st
from data_feeds.data_feeds import get_all_indicators, plot_indicators
from wish_engine import analyzer
import scraper.ism_fetcher as ism
from wish_engine.worldview import generate_worldview

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# Tabs for navigation
tab1, tab2 = st.tabs(["💹 WISH Assistant", "🧭 Macro Dashboard"])

# --- WISH Tab ---
with tab1:
    st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")

    worldview = st.text_input("🌍 Enter your macro view (e.g. 'Bullish US Growth')")

    if worldview:
        suggestion = analyzer.run_wish_analysis(worldview)
        st.success(suggestion)

# --- Macro Dashboard ---
with tab2:
    st.title("🧭 Macro Dashboard")
    st.markdown("Uses ISM, UMCSI, and Housing Starts to generate a macro 'Worldview'")

    # Load and process macro data
    with st.spinner("📊 Fetching indicator data..."):
        df = get_all_indicators()

    # Show chart
    chart = plot_indicators(df)
    st.plotly_chart(chart, use_container_width=True)

    # Show latest values
    st.dataframe(df.tail(3).round(2))

    # Auto-generated macro view
    st.markdown("### 🧠 Auto-Generated Worldview")
    view = generate_worldview(df)
    st.code(view)

# --- Button to refresh ISM data ---
if st.button("🔁 Refresh ISM Data"):
    with st.spinner("Fetching latest ISM data..."):
        ism.full_ism_pipeline()
        st.success("✅ ISM data updated!")

if st.button("🔁 Refresh ISM Data"):
    with st.spinner("Fetching latest ISM data..."):
        ism.full_ism_pipeline()
        st.success("✅ ISM data updated!")
