from typing import Dict, Any
from langsmith import traceable


@traceable(run_type="chain", name="keyword_setup")
def keyword_setup_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 1: Initialize brands, mentions, engagement, and sentiment counters.
    """
    brands = ["Atomberg", "Crompton", "Havells", "Orient", "Bajaj", "Polycab", "Usha"]

    state["brands"] = brands
    state["mentions"] = {b: 0 for b in brands}
    state["engagement"] = {
        b: {"likes": 0, "comments": 0, "shares": 0, "views": 0} for b in brands
    }
    state["sentiments"] = {
        b: {"positive": 0, "negative": 0, "neutral": 0} for b in brands
    }

    return state
