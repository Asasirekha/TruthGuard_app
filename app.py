# app.py
import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# Set up the page
st.set_page_config(page_title="TruthGuard Agent", page_icon="🤖", layout="centered")

# Title and description
st.title("🤖 TruthGuard Agent")
st.markdown("### Autonomous AI Fact-Checker")
st.write("Paste a claim below. The AI Agent will search the web, analyze results, and return a verdict.")

# Initialize API keys variables
gemini_api_key = ""
tavily_api_key = ""

# Try to load API keys from Streamlit secrets (for deployment)
try:
    if "GEMINI_API_KEY" in st.secrets:
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
    if "TAVILY_API_KEY" in st.secrets:
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
except Exception as e:
    # This is normal for local development - silently ignore
    pass

# Sidebar for API keys configuration
with st.sidebar:
    st.header("🔑 Configuration")
    
    # Display status
    if gemini_api_key and tavily_api_key:
        st.success("API keys loaded from secure secrets!")
    else:
        st.info("Enter your API keys below:")
    
    st.markdown("---")
    
    # Gemini API Key Input (only show if not already loaded from secrets)
    if not gemini_api_key:
        gemini_api_key = st.text_input("Google Gemini API Key:", type="password", key="gemini_key")
        st.markdown("[Get Gemini Key](https://aistudio.google.com/app/apikey)")
    else:
        st.markdown("**Google Gemini API Key** ✅ Loaded from secrets")
    
    st.markdown("---")
    
    # Tavily API Key Input (only show if not already loaded from secrets)
    if not tavily_api_key:
        tavily_api_key = st.text_input("Tavily AI API Key:", type="password", key="tavily_key")
        st.markdown("[Get Tavily Key](https://tavily.com/)")
    else:
        st.markdown("**Tavily AI API Key** ✅ Loaded from secrets")
    
    st.markdown("---")
    st.caption("🔒 Keys are handled securely and never stored in the app.")

# User input
user_input = st.text_area(
    "**Claim to Fact-Check:**",
    height=100,
    placeholder="e.g., 'Drinking lemon water causes bone cancer.'"
)

# Function to perform web search using Tavily
def tavily_search(query, api_key):
    """Searches the web using the Tavily API and returns results."""
    try:
        tavily = TavilyClient(api_key=api_key)
        response = tavily.search(query=query, include_answer=True, max_results=5)
        return response
    except Exception as e:
        st.error(f"Search API error: {e}")
        return None

# The core function for the AI Agent
# The core function for the AI Agent (FIXED VERSION)
def fact_check_agent(claim, gemini_key, tavily_key):
    """AI Agent that fact-checks claims using web search and reasoning."""
    if not gemini_key or not tavily_key:
        return "Error: Please enter both API keys in the sidebar.", ""
    
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return f"Error: Failed to configure AI model. {e}", ""
    
    # Step 1: Agent Plans the Search Query (SIMPLIFIED PROMPT)
    prompt_plan = f"""
    Create a short, simple search query to fact-check this claim. Return ONLY the search query, nothing else.
    
    Claim: "{claim}"
    
    Search Query:
    """
    
    try:
        search_query_response = model.generate_content(prompt_plan)
        search_query = search_query_response.text.strip()
        
        # Clean up the query - remove any explanations, keep it under 100 chars
        if len(search_query) > 100:
            # Take only the first part that looks like a search query
            search_query = search_query.split('"')[1] if '"' in search_query else search_query[:100]
        
    except Exception as e:
        return f"Error: Failed to generate search query. {e}", ""
    
    # Step 2: Web Search
    if search_query and len(search_query) <= 400:
        with st.status("🤖 Agent is working...", expanded=True) as status:
            st.write(f"**Planning:** Searching for: '{search_query}'")
            
            search_results = tavily_search(search_query, tavily_key)
            if not search_results:
                return "Error: Web search failed. Check your Tavily API key.", search_query
            
            # Step 3: Analysis and Verdict
            prompt_reason = f"""
            Analyze this claim based on the search evidence and provide a fact-check verdict.
            
            CLAIM: "{claim}"
            
            EVIDENCE FOUND: {search_results}
            
            Provide a clear verdict: TRUE, FALSE, MIXTURE, or UNPROVEN.
            Include a brief summary and cite the most relevant evidence.
            """
            
            try:
                final_verdict_response = model.generate_content(prompt_reason)
                final_verdict = final_verdict_response.text
                status.update(label="✅ Analysis complete!", state="complete")
            except Exception as e:
                return f"Error: AI analysis failed. {e}", search_query
        
        return final_verdict, search_query
    else:
        return f"Error: Generated search query is too long ({len(search_query)} characters).", ""


# Run the Agent
if st.button("🔍 Launch TruthGuard Agent", type="primary", use_container_width=True):
    if not user_input:
        st.warning("Please enter a claim to fact-check.")
    elif not gemini_api_key or not tavily_api_key:
        st.error("Please add both API keys in the sidebar.")
    else:
        verdict, search_query = fact_check_agent(user_input, gemini_api_key, tavily_api_key)
        
        if verdict.startswith("Error:"):
            st.error(verdict)
        else:
            st.success("🎉 Fact-Check Complete!")
            st.markdown("---")
            st.markdown(f"**Claim:** {user_input}")
            st.markdown(f"**Search:** `{search_query}`")
            st.markdown("---")
            st.markdown(verdict)
            st.markdown("---")
            st.caption("🤖 Autonomous AI agent analysis")

# Ignore the secrets error - it's normal for local development
import warnings
warnings.filterwarnings('ignore', message='No secrets found')