import streamlit as st
from wish_engine import analyzer

st.set_page_config(page_title="AI Trading Assistant", layout="wide")

st.title("💹 AI Trading Assistant using the W.I.S.H. Framework")
st.markdown("**W**orldview → **I**ndustry → **S**tock → **H**ow to Trade It")

worldview = st.text_input("🌍 Enter your macro view (e.g. 'Bullish US Growth')")

if worldview:
    suggestion = analyzer.run_wish_analysis(worldview)
    st.success(suggestion)
