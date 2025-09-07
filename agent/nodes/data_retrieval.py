import os
from datetime import datetime, timedelta
from typing import Dict, Any

from services.google_fetcher import fetch_google_serpapi
from services.youtube_fetcher import fetch_youtube
from services.x_fetcher import fetch_x_snscrape


def data_retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: fetches data from Google, YouTube, X"""
    keyword = state.get("keywords", ["smart fan"])[0]
    top_n = state.get("top_n_per_platform", 20)

    combined = []

    serpapi_key = os.getenv("SERPAPI_KEY") or state.get("SERPAPI_KEY")
    if serpapi_key:
        try:
            combined.extend(fetch_google_serpapi(keyword, serpapi_key, top_n=top_n))
        except Exception as e:
            print("Google fetch error:", e)

    yt_key = os.getenv("YOUTUBE_API_KEY") or state.get("YOUTUBE_API_KEY")
    if yt_key:
        try:
            combined.extend(fetch_youtube(keyword, yt_key, top_n_videos=top_n))
        except Exception as e:
            print("YouTube fetch error:", e)

    enable_x = str(os.getenv("ENABLE_X") or state.get("ENABLE_X", "")).lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if enable_x:
        try:
            since_date = (datetime.utcnow() - timedelta(days=365)).date().isoformat()
            until_date = datetime.utcnow().date().isoformat()
            combined.extend(
                fetch_x_snscrape(
                    keyword, top_n=top_n, since_iso=since_date, until_iso=until_date
                )
            )
        except Exception as e:
            print("X fetch error:", e)

    state["raw_data"] = combined
    return state
