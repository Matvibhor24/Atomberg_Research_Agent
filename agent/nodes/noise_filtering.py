from typing import Dict, Any, List
import re
from langsmith import traceable


def _deduplicate(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique = []
    for post in posts:
        identifier = post.get("meta", {}).get("url") or post["text"].strip().lower()
        if identifier not in seen:
            seen.add(identifier)
            unique.append(post)
    return unique


def _is_relevant(text: str, keywords: List[str]) -> bool:
    """
    Check if text contains at least one keyword (with word boundary).
    Avoids matching 'fan' in 'fan club' unless 'smart fan' is present.
    """
    text = text.lower()
    for kw in keywords:
        if re.search(rf"\b{kw.lower()}\b", text):
            return True
    return False


def _is_spam(text: str) -> bool:
    if len(text.split()) <= 3:
        return True
    if text.lower().startswith("http") or "buy now" in text.lower():
        return True
    return False


@traceable(run_type="tool", name="noise_filtering")
def noise_filtering_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 3: Deduplicate, filter irrelevant, drop spam.
    """
    keywords = state.get("keywords", [])
    raw_posts = state.get("raw_data", [])

    deduped = _deduplicate(raw_posts)

    relevant = [p for p in deduped if _is_relevant(p["text"], keywords)]

    clean = [p for p in relevant if not _is_spam(p["text"])]

    state["clean_data"] = clean
    return state
