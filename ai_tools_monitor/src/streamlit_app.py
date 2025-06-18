import streamlit as st
import asyncio
from datetime import datetime
from agents.mcp_agent import EnhancedFetcherAgent
from dotenv import load_dotenv
import os

# Page config
st.set_page_config(
    page_title="AI Tools Monitor",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'fetched_tools' not in st.session_state:
    st.session_state.fetched_tools = []
if 'analysis' not in st.session_state:
    st.session_state.analysis = {}

# Title and description
st.title("🤖 AI Tools Monitor")
st.markdown("""
This dashboard monitors AI tools from multiple sources including Twitter, TopAI.tools, and Archon.
Use the sidebar to configure and run fetches.
""")

# Sidebar configuration
st.sidebar.title("Configuration")

# Twitter API credentials
st.sidebar.subheader("Twitter API Credentials")
twitter_api_key = st.sidebar.text_input("API Key", value=os.getenv('TWITTER_API_KEY', ''))
twitter_api_secret = st.sidebar.text_input("API Secret", value=os.getenv('TWITTER_API_SECRET', ''), type='password')
twitter_access_token = st.sidebar.text_input("Access Token", value=os.getenv('TWITTER_ACCESS_TOKEN', ''))
twitter_access_token_secret = st.sidebar.text_input("Access Token Secret", value=os.getenv('TWITTER_ACCESS_TOKEN_SECRET', ''), type='password')

# Archon configuration
st.sidebar.subheader("Archon Configuration")
archon_api_key = st.sidebar.text_input("Archon API Key", value=os.getenv('ARCHON_API_KEY', ''), type='password')
archon_endpoint = st.sidebar.text_input("Archon Endpoint", value=os.getenv('ARCHON_ENDPOINT', 'http://localhost:8000'))

# Fetch button
if st.sidebar.button("Fetch Tools"):
    config = {
        'TWITTER_API_KEY': twitter_api_key,
        'TWITTER_API_SECRET': twitter_api_secret,
        'TWITTER_ACCESS_TOKEN': twitter_access_token,
        'TWITTER_ACCESS_TOKEN_SECRET': twitter_access_token_secret,
        'ARCHON_API_KEY': archon_api_key,
        'ARCHON_ENDPOINT': archon_endpoint
    }
    
    with st.spinner("Fetching tools..."):
        agent = EnhancedFetcherAgent(config)
        try:
            tools = asyncio.run(agent.fetch_all())
            st.session_state.fetched_tools = tools
            
            analysis = asyncio.run(agent.analyze_tools(tools))
            st.session_state.analysis = analysis
            
            st.success(f"Successfully fetched {len(tools)} tools!")
        except Exception as e:
            st.error(f"Error fetching tools: {str(e)}")
        finally:
            asyncio.run(agent.close())

# Display results
if st.session_state.fetched_tools:
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tools", st.session_state.analysis.get('total_tools', 0))
    with col2:
        st.metric("Sources", len(st.session_state.analysis.get('sources', {})))
    with col3:
        st.metric("Categories", len(st.session_state.analysis.get('categories', {})))

    # Source distribution
    st.subheader("Tools by Source")
    sources = st.session_state.analysis.get('sources', {})
    st.bar_chart(sources)

    # Top categories
    st.subheader("Top Categories")
    for trend in st.session_state.analysis.get('trends', []):
        st.write(f"- {trend}")

    # Pricing distribution
    st.subheader("Pricing Distribution")
    pricing = st.session_state.analysis.get('pricing_distribution', {})
    st.bar_chart(pricing)

    # Tool list
    st.subheader("Recent Tools")
    for tool in st.session_state.fetched_tools[:10]:
        with st.expander(f"{tool['name']} ({tool['raw_data'].get('source', 'Unknown')})"):
            st.write(f"**Description:** {tool['description']}")
            st.write(f"**URL:** {tool['url']}")
            
            if tool['raw_data'].get('source') == 'Twitter':
                author = tool['raw_data'].get('author', {})
                if author:
                    st.write(f"**Author:** @{author.get('username')} ({author.get('name')})")
                    st.write(f"**Followers:** {author.get('followers', 0):,}")
                metrics = tool['raw_data'].get('metrics', {})
                st.write(f"**Likes:** {metrics.get('like_count', 0):,}")
                st.write(f"**Retweets:** {metrics.get('retweet_count', 0):,}")
            
            elif tool['raw_data'].get('source') == 'TopAI.tools':
                st.write(f"**Categories:** {', '.join(tool['raw_data'].get('categories', []))}")
                st.write(f"**Pricing:** {tool['raw_data'].get('pricing', 'Unknown')}")
                metrics = tool['raw_data'].get('metrics', {})
                st.write(f"**Views:** {metrics.get('views', 0):,}")

else:
    st.info("Use the sidebar to configure and fetch tools.") 