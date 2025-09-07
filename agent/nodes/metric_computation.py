from typing import Dict, Any
from langsmith import traceable
from config import get_brands


@traceable(run_type="chain", name="metric_computation")
def metric_computation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 7: Compute SoV, SPV, Engagement Share for each brand.
    """
    mention_counters = state.get("mention_counters", {})
    sentiment_totals = state.get("sentiment_totals", {})
    engagement_totals = state.get("engagement_totals", {})

    results = {}

    total_mentions = sum(mention_counters.values())
    brands = get_brands()
    total_positive = sum(sentiment_totals[b]["positive"] for b in brands)
    total_engagement = sum(sum(engagement_totals[b].values()) for b in brands)

    for brand in brands:
        mentions = mention_counters.get(brand, 0)
        sentiments = sentiment_totals.get(
            brand, {"positive": 0, "negative": 0, "neutral": 0}
        )
        engagement = engagement_totals.get(
            brand, {"likes": 0, "comments": 0, "views": 0, "shares": 0}
        )

        brand_engagement = sum(engagement.values())

        sov = (mentions / total_mentions * 100) if total_mentions > 0 else 0
        spv = (
            (sentiments["positive"] / total_positive * 100) if total_positive > 0 else 0
        )
        eng_share = (
            (brand_engagement / total_engagement * 100) if total_engagement > 0 else 0
        )

        results[brand] = {
            "mentions": mentions,
            "sov_percent": round(sov, 2),
            "sentiment": sentiments,
            "spv_percent": round(spv, 2),
            "engagement": engagement,
            "engagement_share_percent": round(eng_share, 2),
        }

    state["metrics"] = results
    return state
