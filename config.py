"""
Configuration file for the Market Research Agent
"""

# Default brands to track
DEFAULT_BRANDS = [
    "Atomberg", 
    "Crompton", 
    "Havells", 
    "Orient", 
    "Bajaj", 
    "SuperFan",
    "Hunter",
    "Polycab", 
    "Midea",
    "Kichler",
    "V-Guard",
    "Usha"
]

# Default keywords
DEFAULT_KEYWORDS = ["smart fan"]

PROJECT_NAME = "Market Research Agent"
API_TITLE = "Market Research Agent API"
LANGCHAIN_PROJECT = "Market-Research-Agent"

def get_brands():
    """Get the list of brands to track"""
    import os
    brands_env = os.getenv("BRANDS", "")
    if brands_env:
        # Support comma-separated or space-separated brands
        if "," in brands_env:
            return [brand.strip() for brand in brands_env.split(",") if brand.strip()]
        else:
            return [brand.strip() for brand in brands_env.split() if brand.strip()]
    return DEFAULT_BRANDS

def get_keywords():
    """Get the default keywords"""
    import os
    keywords_env = os.getenv("KEYWORDS", "")
    if keywords_env:
        # Support comma-separated or space-separated keywords
        if "," in keywords_env:
            return [keyword.strip() for keyword in keywords_env.split(",") if keyword.strip()]
        else:
            return [keyword.strip() for keyword in keywords_env.split() if keyword.strip()]
    return DEFAULT_KEYWORDS
