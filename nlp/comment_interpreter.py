def interpret_ism_comments(comments: str) -> dict:
    """
    Simulate AI analysis of ISM panelist comments.
    In production: use OpenAI or local LLM for true NLP.
    """
    sector_sentiment = {}

    example_sectors = [
        "Technology", "Construction", "Food & Beverage", "Healthcare",
        "Finance", "Retail", "Transportation", "Automotive"
    ]

    comments_lower = comments.lower()

    for sector in example_sectors:
        if sector.lower() in comments_lower:
            if any(word in comments_lower for word in ["strong", "growth", "expanding", "increasing"]):
                sentiment = "Bullish"
            elif any(word in comments_lower for word in ["decline", "weak", "shrinking", "slow"]):
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            sector_sentiment[sector] = sentiment

    return sector_sentiment

