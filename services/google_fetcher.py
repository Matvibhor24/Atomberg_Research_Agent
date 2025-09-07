import requests
from typing import List, Dict, Any
import os
from langsmith import traceable


@traceable(run_type="tool", name="fetch_google_serpapi")
def fetch_google_serpapi(keyword: str, top_n: int = 20) -> List[Dict[str, Any]]:
    url = "https://serpapi.com/search"
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        raise RuntimeError("Missing SERPAPI_KEY in environment")
    params = {"engine": "google", "q": keyword, "api_key": serpapi_key}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    results = []
    for item in data.get("organic_results", []) + data.get("news_results", []):
        title = item.get("title", "")
        snippet = item.get("snippet") or item.get("description", "")
        link = item.get("link") or item.get("source")
        results.append(
            {
                "platform": "Google",
                "text": f"{title} - {snippet}",
                "meta": {
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "views": 0,
                    "url": link,
                    "date": item.get("date"),
                    "id": item.get("position") or item.get("cacheId") or link,
                    "author": item.get("source") or item.get("displayed_link"),
                },
            }
        )
        if len(results) >= top_n:
            break
    return results
