from typing import Dict, Any, List
from langsmith import traceable

BRANDS = ["Atomberg", "Crompton", "Havells", "Orient", "Bajaj", "Polycab", "Usha"]


def _tag_brands(text: str, brands: List[str]) -> List[str]:
    """
    Check which brands are mentioned in text (case-insensitive).
    """
    text_lower = text.lower()
    matches = []
    for brand in brands:
        if brand.lower() in text_lower:
            matches.append(brand)
    return matches


@traceable(run_type="tool", name="brand_tagging")
def brand_tagging_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 4: Scan posts and tag them with mentioned brands.
    """
    posts = state.get("clean_data", [])
    tagged_posts = []

    mention_counters = {brand: 0 for brand in BRANDS}

    for post in posts:
        mentions = _tag_brands(post["text"], BRANDS)
        if mentions:
            post["brands"] = mentions
            for b in mentions:
                mention_counters[b] += 1
        else:
            post["brands"] = ["none"]

        tagged_posts.append(post)

    state["tagged_data"] = tagged_posts
    state["mention_counters"] = mention_counters

    return state
