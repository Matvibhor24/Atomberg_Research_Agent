from typing import List, Dict, Any
from googleapiclient.discovery import build
import os


def fetch_youtube(keyword: str, top_n_videos: int = 20) -> List[Dict[str, Any]]:
    """
    Fetch top N YouTube videos + stats for a given keyword.
    Requires YouTube Data API v3 key.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing YOUTUBE_API_KEY in environment")

    youtube = build("youtube", "v3", developerKey=api_key)

    search_response = (
        youtube.search()
        .list(
            q=keyword,
            part="snippet",
            type="video",
            maxResults=min(top_n_videos, 50),  # API limit
        )
        .execute()
    )

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    if not video_ids:
        return []

    stats_response = (
        youtube.videos()
        .list(id=",".join(video_ids), part="snippet,statistics")
        .execute()
    )

    results = []
    for item in stats_response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        results.append(
            {
                "platform": "YouTube",
                "text": f"{snippet.get('title', '')} - {snippet.get('description', '')}",
                "meta": {
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "views": int(stats.get("viewCount", 0)),
                    "shares": 0,  # not exposed by API
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "date": snippet.get("publishedAt"),
                    "id": item["id"],
                    "author": snippet.get("channelTitle", ""),
                },
            }
        )

    return results
