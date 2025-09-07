<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# can you give me entire of this in a singke file

Here is the entire Atomberg Share of Voice AI Agent README content, cleaned and formatted as a single Markdown file you can save as `README.md`:

```markdown
# Atomberg Share of Voice AI Agent

## Overview
This project implements an AI agent that analyzes Atomberg’s online presence for "smart fans" across **Google** and **YouTube**. The agent quantifies **Share of Voice (SoV)**, **Share of Positive Voice (SPV)**, engagement metrics, and generates actionable marketing insights.  
Built with **Python**, **LangGraph nodes**, **VADER sentiment analysis**, and **LLM integration** for narrative insights.

---

## Features
- Fetch top N search results/posts from multiple platforms for Atomberg and competitors (Crompton, Havells, Orient, Bajaj, Polycab, Usha)  
- Clean and deduplicate posts to remove noise  
- Tag posts with mentioned brands  
- Aggregate engagement metrics (likes, comments, shares, views) per brand  
- Perform sentiment analysis (positive/negative/neutral)  
- Compute SoV, SPV, and engagement share  
- Generate human-readable insights and recommendations for marketing  

---

## Technology Stack
- **Python** – Data processing, cleaning, and workflow orchestration  
- **Google Search API / SerpAPI** – Fetch search results  
- **YouTube Data API v3** – Fetch YouTube posts  
- **VADER (NLTK)** – Sentiment analysis  
- **LangGraph** – AI agent orchestration  
- **LangChain / LLMs** – Narrative insight generation  

---

## Workflow Steps
1. Keyword & Brand Setup  
2. Data Retrieval  
3. Noise Filtering  
4. Brand Tagging  
5. Engagement Aggregation  
6. Sentiment Analysis  
7. Metric Computation (SoV, SPV, Engagement Share)  
8. Insight Generation  

---

## Setup Instructions

### 1. Clone the Repository
```

git clone <repo_url>
cd atomberg-sov-agent

```

### 2. Create a Virtual Environment (Recommended)
```

python -m venv venv
source venv/bin/activate       \# Linux/macOS
venv\Scripts\activate          \# Windows

```

### 3. Install Dependencies
```

pip install -r requirements.txt

```

### 4. Configure API Keys  
The agent requires API keys for Google Search and YouTube. X scraping uses **snscrape**, which does not require keys.

- **Google Search / SerpAPI** → Obtain an API key from SerpAPI or Google Custom Search.  
- **YouTube Data API v3** → Enable the API in Google Cloud Console and generate your key.  
- **X (Twitter)** → Works via `snscrape`, no keys needed.  
- **Optional: OpenAI** → For narrative summaries, get an OpenAI API key.

Create a `.env` file in the project root and add your credentials:
```

GOOGLE_API_KEY=your_google_api_key
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key   \# Optional

```

### 5. Verify Setup
```

python main.py --test

```
This will fetch dummy posts and confirm connectivity.

### 6. Run the Agent
```

python main.py

```

The agent will:
- Retrieve data from Google, YouTube, and X  
- Clean and deduplicate content  
- Tag brand mentions and calculate engagement metrics  
- Perform sentiment analysis  
- Compute SoV and related KPIs  
- Output results and insights  

**Outputs include JSON files, text summaries, and optional graphs.**

---

## Example Outputs
- `outputs/results.json` → Processed raw + structured data  
- `outputs/insights.txt` → Narrative insights (if OpenAI integrated)  
- `outputs/charts/` → Engagement trend graphs, SoV breakdown  

---
```

You can save the above content directly as a single `README.md` file in your project root.
If you want, I can also help generate badges or add visuals next.
<span style="display:none">[^1][^10][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://stackoverflow.com/questions/4779582/markdown-and-including-multiple-files

[^2]: https://www.reddit.com/r/ObsidianMD/comments/103qrts/is_there_any_way_to_merge_multiple_md_note_files/

[^3]: https://forums.getdrafts.com/t/combine-sections-of-multiple-md-files-by-heading/7362

[^4]: https://www.markdowntoolbox.com/tools/combine-files/

[^5]: https://www.npmjs.com/package/@knennigtri/merge-markdown

[^6]: https://indigo.re/mdsaw/

[^7]: https://github.com/abhinav/stitchmd

[^8]: https://github.com/orgs/unifiedjs/discussions/124

[^9]: https://discourse.gohugo.io/t/multiple-content-parts-within-the-same-page/8337

[^10]: https://www.markdownguide.org/basic-syntax/

