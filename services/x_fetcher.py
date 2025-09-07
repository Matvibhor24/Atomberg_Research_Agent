import snscrape.modules.twitter as sntwitter
from typing import List, Dict, Any
from datetime import datetime
from langsmith import traceable


@traceable(run_type="tool", name="fetch_x_snscrape")
def fetch_x_snscrape(
    keyword: str, top_n: int = 100, since_iso: str = None, until_iso: str = None
) -> List[Dict[str, Any]]:
    """
    Fetch tweets using snscrape. No API key required.
    since_iso, until_iso should be 'YYYY-MM-DD' strings.
    """
    query = f"{keyword}"
    if since_iso:
        query += f" since:{since_iso}"
    if until_iso:
        query += f" until:{until_iso}"

    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= top_n:
            break
        tweets.append(
            {
                "platform": "X",
                "text": tweet.content,
                "meta": {
                    "likes": tweet.likeCount,
                    "comments": tweet.replyCount,
                    "shares": tweet.retweetCount,
                    "views": getattr(tweet, "viewCount", 0) or 0,  # sometimes missing
                    "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",
                    "date": tweet.date.isoformat(),
                    "id": str(tweet.id),
                    "author": tweet.user.username,
                },
            }
        )
    return tweets
