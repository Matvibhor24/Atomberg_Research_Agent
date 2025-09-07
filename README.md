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

The agent requires API keys for Google Search and YouTube.

- **Google Search / SerpAPI** → Obtain an API key from SerpAPI or Google Custom Search.
- **YouTube Data API v3** → Enable the API in Google Cloud Console and generate your key.
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

- Retrieve data from Google and YouTube
- Clean and deduplicate content
- Tag brand mentions and calculate engagement metrics
- Perform sentiment analysis
- Compute SoV and related KPIs
- Output results and insights

**Outputs include JSON files and text summaries**

---

## Example Outputs

- `outputs/results.json` → Processed raw + structured data
- `outputs/insights.txt` → Narrative insights (if OpenAI integrated)

---
