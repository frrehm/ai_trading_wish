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
       
