# ai_trading_wish/wish_engine/analyzer.py

def run_wish_analysis(worldview: str) -> str:
    """Very simple WISH logic example."""
    vw = worldview.lower()
    
    if "growth" in vw:
        return "📊 Suggestion: Long Semiconductors (SMH), Long NVDA"
    elif "china" in vw:
        return "📊 Suggestion: Long Commodities, Short Luxury"
    elif "recession" in vw or "slowdown" in vw:
        return "📊 Suggestion: Long Utilities, Short Travel & Leisure"
    else:
        return "❓ No strong trade idea detected yet. Try a different view."
        
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
