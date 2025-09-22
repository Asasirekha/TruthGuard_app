# app.py
import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# Set up the page
st.set_page_config(page_title="TruthGuard Agent", page_icon="🤖")

# Title and description
st.title("🤖 TruthGuard Agent")
st.markdown("### Autonomous AI Fact-Checker")
st.write("Paste a claim below. The AI Agent will search the web, analyze results, and return a verdict.")

# Sidebar for API keys
with st.sidebar:
    st.header("Configuration")
    
    # Gemini Key
    st.markdown("**Google Gemini API Key**")
    gemini_api_key = st.text_input("Enter your Gemini Key:", type="password")
    st.markdown("[Get Gemini Key](https://aistudio.google.com/app/apikey)")
    
    # Tavily Key
    st.markdown("**Tavily AI API Key (for Web Search)**")
    tavily_api_key = st.text_input("Enter your Tavily Key:", type="password")
    st.markdown("[Get Tavily Key](https://tavily.com/)")
    
    st.markdown("---")
    st.caption("Keys are not stored and are only used for this session.")

# User input
user_input = st.text_area(
    "**Claim to Fact-Check:**",
    height=100,
    placeholder="e.g., 'Drinking lemon water causes bone cancer.'"
)

# Function to perform web search using Tavily
def tavily_search(query, api_key):
    """Searches the web using the Tavily API and returns results."""
    tavily = TavilyClient(api_key=tavily_api_key)
    response = tavily.search(query=query, include_answer=True, max_results=5)
    return response

# The core function for the AI Agent
def fact_check_agent(claim, gemini_key, tavily_key):
    """
    This function acts as an AI agent: it plans, uses tools (web search),
    reasons about the evidence, and generates a final verdict.
    """
    # Configure the Gemini API
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Step 1: Agent Plans the Search Query
    prompt_plan = f"""
    You are a fact-checking assistant. Given the user's claim below, generate a simple, effective web search query to find evidence from reputable sources to verify or debunk it. Return only the search query, nothing else.

    Claim: "{claim}"

    Search Query:
    """
    search_query = model.generate_content(prompt_plan).text.strip()
    
    # Step 2: Agent Uses a Tool (Tavily Search API)
    st.info(f"🤖 Agent is searching the web: '{search_query}'")
    search_results = tavily_search(search_query, tavily_key)
    
    # Step 3: Agent Reasons About the Evidence
    prompt_reason = f"""
    ROLE: You are TruthGuard, an autonomous AI fact-checking agent.

    GOAL: Analyze the following user's claim based on the provided web search evidence from Tavily. Generate a final verdict.

    USER'S CLAIM: "{claim}"

    WEB SEARCH EVIDENCE:
    {search_results}

    INSTRUCTIONS:
    1.  **VERDICT:** Start with a clear verdict: **TRUE**, **FALSE**, **MIXTURE**, or **UNPROVEN**.
    2.  **SUMMARY:** Provide a 1-2 sentence summary of your finding.
    3.  **EVIDENCE:** Briefly cite the key evidence from the search results that led to your verdict. Mention source names for credibility (e.g., "According to the WHO...").
    4.  **CONFIDENCE:** State your confidence level (Low/Medium/High).

    Be neutral and objective.
    """
    
    # Step 4: Agent Generates Final Verdict
    with st.spinner("🤖 Agent is analyzing evidence and reasoning..."):
        final_verdict = model.generate_content(prompt_reason).text

    return final_verdict, search_query

# Create the button to run the Agent
if st.button("🔍 Launch TruthGuard Agent", type="primary") and user_input:
    if not gemini_api_key or not tavily_api_key:
        st.error("Please add both API keys in the sidebar to use the Agent.")
    else:
        # Run the Agent
        verdict, search_query_used = fact_check_agent(user_input, gemini_api_key, tavily_api_key)
        
        # Display Results
        st.success("Fact-Check Complete!")
        st.markdown("---")
        st.markdown(f"**Claim:** {user_input}")
        st.markdown(f"**Search Query Used:** `{search_query_used}`")
        st.markdown("---")
        st.markdown(verdict)
        st.markdown("---")
        st.caption("This verdict was generated autonomously by an AI agent using web search.")

elif st.button("🔍 Launch TruthGuard Agent") and not user_input:
    st.warning("Please enter a claim to fact-check.")