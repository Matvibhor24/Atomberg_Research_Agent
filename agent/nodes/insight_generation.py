from typing import Dict, Any
import os
from dotenv import load_dotenv
from langsmith import traceable
from config import get_brands
from openai import OpenAI

load_dotenv()

@traceable(run_type="tool", name="rule_based_insights")
def _rule_based_insights(metrics: Dict[str, Any], keywords: list = None) -> Dict[str, str]:
    """Generate basic rule-based insights from metrics"""
    insights = {}
    
    if keywords and len(keywords) > 0:
        product_term = keywords[0]
    else:
        product_term = "products"

    top_brand = max(metrics.items(), key=lambda x: x[1]["sov_percent"])[0]
    top_sov = metrics[top_brand]["sov_percent"]

    insights["sov"] = (
        f"{top_brand} leads with {top_sov:.1f}% Share of Voice among {product_term}."
    )

    top_spv_brand = max(metrics.items(), key=lambda x: x[1]["spv_percent"])[0]
    top_spv = metrics[top_spv_brand]["spv_percent"]

    insights["spv"] = (
        f"{top_spv_brand} has the highest Share of Positive Voice at {top_spv:.1f}%."
    )

    top_eng_brand = max(
        metrics.items(), key=lambda x: x[1]["engagement_share_percent"]
    )[0]
    top_eng = metrics[top_eng_brand]["engagement_share_percent"]

    insights["engagement"] = (
        f"{top_eng_brand} drives the most engagement with {top_eng:.1f}% share."
    )

    return insights


@traceable(run_type="llm", name="call_openai")
def _call_openai(prompt: str, api_key: str) -> str:
    """Call OpenAI GPT-4o-mini"""
    
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a marketing analyst. Generate concise, actionable insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return completion.choices[0].message.content.strip()


@traceable(run_type="llm", name="call_gemini")
def _call_gemini(prompt: str, api_key: str) -> str:
    """Call OpenAI Gemini-1.5-flash"""
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    completion = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a marketing analyst. Generate concise, actionable insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return completion.choices[0].message.content.strip()


@traceable(run_type="chain", name="generate_llm_insights")
def _generate_llm_insights(metrics: Dict[str, Any], rule_based: Dict[str, str], keywords: list = None) -> str:
    """Generate insights using either OpenAI or Gemini based on available API keys"""
    
    prompt = (
        f"You are a marketing analyst for 'Atomberg' brand. For these keywords {keywords} searched on the internet, we have got the following - \n\n"
        f"Metrics JSON:\n{metrics}\n\n"
        f"Rule-based insights:\n{rule_based}\n\n"
        "Summarize these brand metrics into a concise, insightful paragraph "
        "with one key takeaway and one recommendation. Avoid repeating numbers verbatim; focus on narrative.\n\n"
        
    )

    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    if gemini_key:
        try:
            print("Using Gemini 2.5 Flash for insights")
            return _call_gemini(prompt, gemini_key)
        except Exception as e:
            print(f"Gemini failed: {e}")

    elif openai_key:
        try:
            print("Using OpenAI GPT-4o-mini for insights")
            return _call_openai(prompt, openai_key)
        except Exception as e:
            print(f"OpenAI failed: {e}")
    
    
    
    print("No LLM available, using rule-based insights")
    return None


@traceable(run_type="chain", name="insight_generation")
def insight_generation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate marketing insights from brand metrics"""
    metrics = state.get("metrics", {})
    keywords = state.get("keywords", [])
    
    try:
        if not metrics:
            raise ValueError("No metrics available")
        
        rule_based = _rule_based_insights(metrics, keywords)
        fallback_narrative = (
            f"Based on the data, {rule_based['sov']} "
            f"Additionally, {rule_based['spv']} "
            f"Finally, {rule_based['engagement']}"
        )
        
    except Exception as e:
        print(f"Error generating rule-based insights: {e}")
        rule_based = {}
        fallback_narrative = (
            "Not enough data to compute comparative brand insights yet. "
            "Please try with broader keywords or a longer time window."
        )
    
    llm_narrative = _generate_llm_insights(metrics, rule_based, keywords)
    
    final_narrative = llm_narrative if llm_narrative else fallback_narrative
    
    state["insights"] = {
        "rule_based": rule_based,
        "narrative": final_narrative,
    }
    
    return state
