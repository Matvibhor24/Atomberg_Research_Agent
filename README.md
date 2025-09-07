# Atomberg Share of Voice AI Agent

## Overview
This project implements an AI agent that analyzes Atomberg’s online presence for "smart fans" across **Google**, **YouTube**, and **X (Twitter)**. The agent quantifies **Share of Voice (SoV)**, **Share of Positive Voice (SPV)**, engagement metrics, and generates actionable marketing insights.

Built with **Python**, **LangGraph nodes**, **VADER sentiment analysis**, and optional **LLM integration** for narrative insights.

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
- **snscrape** – Fetch X (Twitter) posts  
- **VADER (NLTK)** – Sentiment analysis  
- **LangGraph** – AI agent orchestration  
- **Matplotlib / Seaborn** – Visualization (optional)  
- **LangChain / LLMs** – Optional narrative insight generation  

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
1. Clone the repository:  
```bash
git clone <repo_url>
cd atomberg-sov-agent
