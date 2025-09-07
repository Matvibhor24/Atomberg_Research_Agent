from typing import Dict, Any, List
import os
import argparse
import asyncio

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
from config import get_keywords, PROJECT_NAME


def build_graph():
    """
    Construct the LangGraph workflow using modular node implementations.
    Return a compiled graph ready to invoke.
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

    parser = argparse.ArgumentParser(description=f"Run {PROJECT_NAME}")
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=env_keywords or get_keywords(),
        help="Keywords to track (space-separated). Fallback: KEYWORDS env (comma/space-separated)",
    )
    parser.add_argument(
        "--top_n_per_platform",
        type=int,
        default=env_topn_int or 20,
        help="Items to fetch per platform. Fallback: TOP_N_PER_PLATFORM env",
    )
    return parser.parse_args()



@traceable(run_type="chain", name="atomberg_market_research_agent")
def run_pipeline_server(initial_state=None):
    if initial_state is None:
        initial_state = {
            "keywords": get_keywords(),
            "top_n_per_platform": 20,
        }
    graph = build_graph()
    final_state = graph.invoke(initial_state)
    return final_state

@traceable(run_type="chain", name="atomberg_market_research_pipeline")
def run_pipeline() -> Dict[str, Any]:
    args = parse_args()

    graph = build_graph()

    initial_state: Dict[str, Any] = {
        "keywords": args.keywords,
        "top_n_per_platform": args.top_n_per_platform,
    }

    final_state = graph.invoke(initial_state)
    return final_state

@traceable(run_type="chain", name="atomberg_market_research_agent_with_progress")
async def run_pipeline_server_with_progress(initial_state=None):
    """Run pipeline with progress updates for SSE streaming"""
    if initial_state is None:
        initial_state = {
            "keywords": get_keywords(),
            "top_n_per_platform": 20,
        }
    
    # Step names mapping
    step_names = [
        "Keyword & Brand Setup",
        "Data Retrieval", 
        "Noise Filtering",
        "Brand Tagging",
        "Engagement Aggregation",
        "Sentiment Analysis",
        "Metric Computation",
        "Insight Generation"
    ]
    
    try:
        from agent.nodes.keyword_setup import keyword_setup_node
        from agent.nodes.data_retrieval import data_retrieval_node
        from agent.nodes.noise_filtering import noise_filtering_node
        from agent.nodes.brand_tagging import brand_tagging_node
        from agent.nodes.engagement_aggregation import engagement_aggregation_node
        from agent.nodes.sentiment_analysis import sentiment_analysis_node
        from agent.nodes.metric_computation import metric_computation_node
        from agent.nodes.insight_generation import insight_generation_node
        
        node_functions = [
            keyword_setup_node,
            data_retrieval_node,
            noise_filtering_node,
            brand_tagging_node,
            engagement_aggregation_node,
            sentiment_analysis_node,
            metric_computation_node,
            insight_generation_node
        ]
        
        state = initial_state.copy()
        current_step = 1
        
        for step_name, node_func in zip(step_names, node_functions):
            # Mark step as in progress
            yield {"type": "progress", "currentStep": current_step, "stepName": step_name, "status": "in_progress"}
            
            try:
                state = node_func(state)
                
                # Mark step as completed
                yield {"type": "progress", "currentStep": current_step, "stepName": step_name, "status": "completed"}
                current_step += 1
                
            except Exception as e:
                yield {"type": "progress", "currentStep": current_step, "stepName": step_name, "status": "error", "error": str(e)}
                raise e
        
        yield {
            "type": "complete",
            "sources": state.get("raw_data", []),
            "metrics": state.get("metrics", {}),
            "insights": state.get("insights", {}),
        }
        
    except Exception as e:
        yield {"type": "error", "message": str(e)}

if __name__ == "__main__":
    load_dotenv()
    final_state = run_pipeline()

    print("Metrics:")
    print(final_state.get("metrics", {}))
    print("Insights:")
    print(final_state.get("insights", {}))
