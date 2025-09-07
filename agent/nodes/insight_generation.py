from typing import Dict, Any
import statistics
import os
from langsmith import traceable
from langchain_google_genai import ChatGoogleGenerativeAI

BRANDS = ["Atomberg", "Crompton", "Havells", "Orient", "Bajaj", "Polycab", "Usha"]


def _rule_based_insights(metrics: Dict[str, Any]) -> Dict[str, str]:
    insights = {}

    top_brand = max(metrics.items(), key=lambda x: x[1]["sov_percent"])[0]
    top_sov = metrics[top_brand]["sov_percent"]

    insights["sov"] = (
        f"{top_brand} leads with {top_sov:.1f}% Share of Voice among smart fans."
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


def _call_gemini(summary_prompt: str, api_key: str) -> str:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        max_output_tokens=250,
        google_api_key=api_key,
    )
    return (llm.invoke(summary_prompt).content or "").strip()


@traceable(run_type="chain", name="insight_generation")
def insight_generation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    metrics = state.get("metrics", {})
    try:
        if not metrics:
            raise ValueError("No metrics available")
        rule_based = _rule_based_insights(metrics)
        narrative = (
            f"Based on the data, {rule_based['sov']} "
            f"Additionally, {rule_based['spv']} "
            f"Finally, {rule_based['engagement']}"
        )
    except Exception:
        rule_based = {}
        narrative = (
            "Not enough data to compute comparative brand insights yet. "
            "Please try with broader keywords or a longer time window."
        )

    # Prefer Google Gemini (via GOOGLE_API_KEY) for generating narrative
    gemini_key = os.getenv("GOOGLE_API_KEY") or state.get("GOOGLE_API_KEY")
    if gemini_key:
        try:
            summary_prompt = (
                "You are a marketing analyst. Summarize these brand metrics into a concise, insightful paragraph "
                "with one key takeaway and one recommendation. Avoid repeating numbers verbatim; focus on narrative.\n\n"
                f"Metrics JSON:\n{metrics}\n\n"
                f"Rule-based insights:\n{rule_based}\n\n"
            )
            llm_text = _call_gemini(summary_prompt, gemini_key)
        except Exception:
            llm_text = narrative
    else:
        llm_text = narrative

    if not llm_text:
        llm_text = narrative

    # OpenAI-based summarization is temporarily disabled in favor of Gemini.
    # If needed later, re-enable this block and ensure OPENAI_API_KEY is set.
    # api_key = os.getenv("OPENAI_API_KEY") or state.get("OPENAI_API_KEY")
    # if api_key:
    #     try:
    #         from openai import OpenAI
    #
    #         client = OpenAI(api_key=api_key)
    #         summary_prompt = (
    #             "You are a marketing analyst. Summarize these brand metrics into a concise, insightful paragraph "
    #             "with one key takeaway and one recommendation. Avoid repeating numbers verbatim; focus on narrative.\n\n"
    #             f"Metrics JSON:\n{metrics}\n\n"
    #             f"Rule-based insights:\n{rule_based}\n\n"
    #         )
    #         completion = client.chat.completions.create(
    #             model="gpt-4o-mini",
    #             messages=[
    #                 {
    #                     "role": "system",
    #                     "content": "You generate crisp marketing insights.",
    #                 },
    #                 {"role": "user", "content": summary_prompt},
    #             ],
    #             temperature=0.4,
    #             max_tokens=250,
    #         )
    #         llm_text = completion.choices[0].message.content.strip()
    #     except Exception:
    #         llm_text = narrative

    state["insights"] = {
        "rule_based": rule_based,
        "narrative": llm_text,
    }
    return state
