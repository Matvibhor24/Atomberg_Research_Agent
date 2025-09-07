from typing import Dict, Any, List
import os
import argparse

from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from langsmith import traceable

from agent.nodes.keyword_setup import keyword_setup_node
from agent.nodes.data_retrieval import data_retrieval_node
from agent.nodes.noise_filtering import noise_filtering_node
from agent.nodes.brand_tagging import brand_tagging_node
from agent.nodes.engagement_aggregation import engagement_aggregation_node
from agent.nodes.sentiment_analysis import sentiment_analysis_node
from agent.nodes.metric_computation import metric_computation_node
from agent.nodes.insight_generation import insight_generation_node


def build_graph():
    """
    Construct the LangGraph workflow using modular node implementations.
    Returns a compiled graph ready to invoke.
    """
    workflow = StateGraph(Dict[str, Any])

    workflow.add_node("keyword_setup", keyword_setup_node)
    workflow.add_node("data_retrieval", data_retrieval_node)
    workflow.add_node("noise_filtering", noise_filtering_node)
    workflow.add_node("brand_tagging", brand_tagging_node)
    workflow.add_node("engagement_aggregation", engagement_aggregation_node)
    workflow.add_node("sentiment_analysis", sentiment_analysis_node)
    workflow.add_node("metric_computation", metric_computation_node)
    workflow.add_node("insight_generation", insight_generation_node)

    workflow.set_entry_point("keyword_setup")

    workflow.add_edge("keyword_setup", "data_retrieval")
    workflow.add_edge("data_retrieval", "noise_filtering")
    workflow.add_edge("noise_filtering", "brand_tagging")
    workflow.add_edge("brand_tagging", "engagement_aggregation")
    workflow.add_edge("engagement_aggregation", "sentiment_analysis")
    workflow.add_edge("sentiment_analysis", "metric_computation")
    workflow.add_edge("metric_computation", "insight_generation")
    workflow.add_edge("insight_generation", END)

    return workflow.compile()


def _parse_keywords_env(value: str) -> List[str]:
    if not value:
        return []
    if "," in value:
        parts = [p.strip() for p in value.split(",") if p.strip()]
    else:
        parts = [p.strip() for p in value.split() if p.strip()]
    return parts or []


def parse_args() -> argparse.Namespace:
    env_keywords = _parse_keywords_env(os.getenv("KEYWORDS", ""))
    env_topn = os.getenv("TOP_N_PER_PLATFORM")
    try:
        env_topn_int = int(env_topn) if env_topn else None
    except ValueError:
        env_topn_int = None

    parser = argparse.ArgumentParser(description="Run Atomberg research agent")
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=env_keywords or ["smart fan"],
        help="Keywords to track (space-separated). Fallback: KEYWORDS env (comma/space-separated)",
    )
    parser.add_argument(
        "--top_n_per_platform",
        type=int,
        default=env_topn_int or 20,
        help="Items to fetch per platform. Fallback: TOP_N_PER_PLATFORM env",
    )
    return parser.parse_args()


@traceable(run_type="chain", name="atomberg_research_pipeline")
def run_pipeline() -> Dict[str, Any]:
    args = parse_args()

    graph = build_graph()

    initial_state: Dict[str, Any] = {
        "keywords": args.keywords,
        "top_n_per_platform": args.top_n_per_platform,
    }

    serp = os.getenv("SERPAPI_KEY")
    yt = os.getenv("YOUTUBE_API_KEY")
    if serp:
        initial_state["SERPAPI_KEY"] = serp
    if yt:
        initial_state["YOUTUBE_API_KEY"] = yt

    final_state = graph.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    load_dotenv()
    final_state = run_pipeline()

    print("Metrics:")
    print(final_state.get("metrics", {}))
    print("Insights:")
    print(final_state.get("insights", {}))
