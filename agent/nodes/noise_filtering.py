import os
from typing import Dict, Any, List
from langsmith import traceable
from dotenv import load_dotenv
from openai import OpenAI

import json
import re

def safe_json_parse(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Remove code fences like ```json ... ```
        cleaned = re.sub(r"^```(json)?|```$", "", response.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise


load_dotenv()

@traceable(run_type="llm", name="gemini_relevance_filter")
def llm_classify(posts: List[str], keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Use Gemini to classify multiple posts as relevant and/or spam.
    Returns a list of dicts: [{"post": str, "relevant": bool, "spam": bool}, ...]
    """
    posts_formatted = "\n".join([f"{i+1}. \"{p}\"" for i, p in enumerate(posts)])

    prompt = f"""
    You are filtering posts for market research on {keywords}.
    - Relevant if the post is about {keywords}.
    - Irrelevant if it's about unrelated topics or homonyms.
    - Spam if it's very short, only a link, or promotional junk like just a 'buy now'.

    Keywords to consider: {", ".join(keywords)}

    Posts:
    {posts_formatted}

    Return JSON array ONLY, in this format:
    [
      {{"post": "...", "relevant": true/false, "spam": true/false}},
      ...
    ]
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a strict JSON classifier. Reply only with JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content
    return safe_json_parse(response)


@traceable(run_type="chain", name="noise_filtering")
def noise_filtering_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 3: Deduplicate, then batch classify posts with LLM relevance + spam filter.
    """
    keywords = state.get("keywords", [])
    raw_posts = state.get("raw_data", [])

    deduped = []
    seen = set()
    for post in raw_posts:
        identifier = post.get("meta", {}).get("url") or post["text"].strip().lower()
        if identifier not in seen:
            seen.add(identifier)
            deduped.append(post)

    clean = []
    batch_size = 5
    for i in range(0, len(deduped), batch_size):
        batch = deduped[i:i+batch_size]
        texts = [p["text"] for p in batch]
        
        try:
            results = llm_classify(texts, keywords)
        except Exception as e:
            print(f"Batch classification failed: {e}")
            continue

        for post, result in zip(batch, results):
            post["meta"]["classification"] = result
            if result.get("relevant") and not result.get("spam"):
                clean.append(post)

    state["clean_data"] = clean
    return state
