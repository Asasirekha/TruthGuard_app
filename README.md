# TruthGuard Agent - Autonomous AI Fact-Checker

An advanced AI agit add .gitignoregent that autonomously fact-checks claims by searching the web, analyzing evidence, and providing verdicts.

## Features

- **Autonomous AI Agent**: Plans, executes web searches, and reasons about evidence
- **Real-Time Web Search**: Uses Tavily API to gather current information
- **Clear Verdict System**: TRUE, FALSE, MIXTURE, or UNPROVEN with confidence levels
- **Evidence-Based**: Cites sources and provides reasoning for each verdict

## Tech Stack

- **AI Agent Framework**: Custom agent architecture with planning + execution
- **Language Model**: Google Gemini 1.5 Flash
- **Web Search**: Tavily AI Search API
- **Frontend**: Streamlit
- **Backend**: Python

## Prerequisites

You need two API keys:
1. **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Tavily API Key** from [Tavily AI](https://tavily.com/)

## How to Run

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Enter both API keys in the sidebar
5. Paste a claim and click "Launch TruthGuard Agent"

## How It Works

1. **Planning**: The AI generates an optimal search query for the claim
2. **Execution**: Searches the web using Tavily API
3. **Reasoning**: Analyzes search results to form evidence-based conclusion
4. **Verdict**: Returns final verdict with confidence level and sources

## Use Cases

- Fact-checking news headlines
- Verifying health claims
- Checking viral social media posts
- Research assistance for students/journalists

Built as a demonstration of autonomous AI agent capabilities.