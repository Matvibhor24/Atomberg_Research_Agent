from typing import Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

BRANDS = ["Atomberg", "Crompton", "Havells", "Orient", "Bajaj", "Polycab", "Usha"]

analyzer = SentimentIntensityAnalyzer()


def _get_sentiment(text: str) -> str:
    """
    Use VADER to classify sentiment.
    """
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"


def sentiment_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 6: Run sentiment analysis and tally results per brand.
    """
    posts = state.get("tagged_data", [])

    sentiment_totals = {
        brand: {"positive": 0, "negative": 0, "neutral": 0} for brand in BRANDS
    }

    for post in posts:
        sentiment = _get_sentiment(post["text"])
        post["sentiment"] = sentiment

        for brand in post.get("brands", []):
            if brand in sentiment_totals:
                sentiment_totals[brand][sentiment] += 1

    state["sentiment_totals"] = sentiment_totals
    state["sentiment_tagged_data"] = posts
    return state
