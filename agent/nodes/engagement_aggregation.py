from typing import Dict, Any, DefaultDict
from collections import defaultdict
from langsmith import traceable

BRANDS = ["Atomberg", "Crompton", "Havells", "Orient", "Bajaj", "Polycab", "Usha"]


@traceable(run_type="tool", name="engagement_aggregation")
def engagement_aggregation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 5: Aggregate engagement metrics for each brand.
    """
    tagged_posts = state.get("tagged_data", [])

    engagement_totals = {
        brand: {"likes": 0, "comments": 0, "views": 0, "shares": 0} for brand in BRANDS
    }

    for post in tagged_posts:
        brands = post.get("brands", [])
        meta = post.get("meta", {})

        likes = meta.get("likes", 0)
        comments = meta.get("comments", 0)
        views = meta.get("views", 0)
        shares = meta.get("shares", 0)

        for brand in brands:
            if brand in engagement_totals:
                engagement_totals[brand]["likes"] += likes
                engagement_totals[brand]["comments"] += comments
                engagement_totals[brand]["views"] += views
                engagement_totals[brand]["shares"] += shares

    state["engagement_totals"] = engagement_totals
    return state
