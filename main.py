import streamlit as st
import data_feeds
import wish_engine
from wish_engine import analyzer
from data_feeds import data_feeds

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

    # Load and process macro data
    with st.spinner("Fetching indicator data..."):
        df = data_feeds.get_all_indicators()

    # Show chart
    chart = data_feeds.plot_indicators(df)
    st.plotly_chart(chart, use_container_width=True)

    # Show latest values
    st.dataframe(df.tail(3).round(2))

    # Generate and display Worldview
    st.markdown("### 🧠 Auto-Generated Worldview")
    view = wish_engine.generate_worldview(df)
    st.code(view)



import requests

API_KEY = "eff8f9962e5748f3998c10876408df4a"
SERIES_ID = "UMCSENT"  # Michigan Consumer Sentiment

url = f"https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={API_KEY}&file_type=json"

response = requests.get(url)

if response.status_code != 200:
    print("❌ Error:", response.status_code)
    print("Message:", response.text)
else:
    print("✅ Success! Sample observation:")
    print(response.json()["observations"][:2])

import scraper.ism_fetcher as ism

if st.button("🔁 Refresh ISM Data"):
    with st.spinner("Fetching latest ISM data..."):
        ism.full_ism_pipeline()
        st.success("✅ ISM data updated!")

