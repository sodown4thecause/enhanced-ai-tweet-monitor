import streamlit as st
import json
import os
from datetime import datetime
import asyncio
import sys
import subprocess

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_tweet_monitor import AITweetMonitor
except ImportError:
    st.error("Could not import AITweetMonitor. Please check the installation.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🐦 Enhanced AI Tweet Monitor",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1DA1F2 0%, #14171A 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1DA1F2;
        margin: 0.5rem 0;
    }
    .tweet-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e1e8ed;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .rewrite-card {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #1DA1F2;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🐦 Enhanced AI Tweet Monitor</h1>
    <p>Real-time monitoring of 100+ AI Twitter accounts with intelligent tweet rewriting</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 Control Panel")

# Load existing data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    data = {}
    files = {
        'tweets': 'ai_tweets_data.json',
        'analysis': 'ai_trends_analysis.json',
        'rewrites': 'ai_tweet_rewrites.json',
        'top_tweets': 'ai_top_tweets.json'
    }
    
    for key, filename in files.items():
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data[key] = json.load(f)
            except Exception as e:
                st.sidebar.error(f"Error loading {filename}: {str(e)}")
                data[key] = None
        else:
            data[key] = None
    
    return data

# Monitor controls
if st.sidebar.button("🔄 Run Monitoring Cycle", type="primary"):
    with st.spinner("Running monitoring cycle..."):
        try:
            # Run the monitoring script
            result = subprocess.run([
                sys.executable, "ai_tweet_monitor.py"
            ], input="1\n", text=True, capture_output=True, timeout=300)
            
            if result.returncode == 0:
                st.sidebar.success("✅ Monitoring cycle completed!")
                st.rerun()
            else:
                st.sidebar.error(f"❌ Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            st.sidebar.warning("⏰ Monitoring cycle timed out")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")

if st.sidebar.button("📊 Generate Dashboard"):
    try:
        subprocess.run([sys.executable, "create_dashboard.py"], check=True)
        st.sidebar.success("✅ Dashboard generated!")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")

# Load data
data = load_data()

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

# Key metrics
if data['analysis']:
    analysis = data['analysis']
    
    with col1:
        st.metric(
            "📊 Total Tweets",
            analysis.get('total_tweets', 0),
            delta=None
        )
    
    with col2:
        st.metric(
            "🏢 AI Accounts",
            analysis.get('total_accounts', 0),
            delta=None
        )
    
    with col3:
        st.metric(
            "💬 Total Engagement",
            f"{analysis.get('total_engagement', 0):,}",
            delta=None
        )
    
    with col4:
        rewrites_count = len(data['rewrites']) if data['rewrites'] else 0
        st.metric(
            "✍️ Tweet Rewrites",
            rewrites_count,
            delta=None
        )

# Status indicators
st.subheader("🔍 System Status")
col1, col2 = st.columns(2)

with col1:
    if data['analysis']:
        twitter_status = data['analysis'].get('twitter_api_status', 'Unknown')
        if 'Connected' in twitter_status:
            st.success(f"🐦 Twitter API: {twitter_status}")
        else:
            st.warning(f"🐦 Twitter API: {twitter_status}")
    else:
        st.info("🐦 Twitter API: No data available")

with col2:
    if data['analysis']:
        openai_status = data['analysis'].get('openai_status', 'Unknown')
        if 'Available' in openai_status:
            st.success(f"🤖 AI Rewriting: {openai_status}")
        else:
            st.info(f"🤖 AI Rewriting: {openai_status}")
    else:
        st.info("🤖 AI Rewriting: No data available")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🏆 Top Tweets", "✍️ Rewrites", "📈 Trends"])

with tab1:
    st.subheader("📊 Analytics Overview")
    
    if data['analysis']:
        analysis = data['analysis']
        
        # Engagement distribution
        if 'engagement_distribution' in analysis:
            dist = analysis['engagement_distribution']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 Max Engagement", f"{dist.get('max', 0):,.0f}")
            with col2:
                st.metric("📊 Median Engagement", f"{dist.get('median', 0):,.0f}")
            with col3:
                st.metric("📉 Min Engagement", f"{dist.get('min', 0):,.0f}")
        
        # Top accounts
        if 'top_performing_accounts' in analysis:
            st.subheader("🏆 Top Performing Accounts")
            for i, account in enumerate(analysis['top_performing_accounts'][:10], 1):
                st.markdown(f"""
                <div class="metric-card">
                    <strong>#{i} @{account['account']}</strong><br>
                    Average Score: {account['avg_score']:.1f} | Tweets: {account['tweets']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📊 No analytics data available. Run a monitoring cycle to generate data.")

with tab2:
    st.subheader("🏆 Top Performing Tweets")
    
    if data['top_tweets']:
        for i, tweet in enumerate(data['top_tweets'][:10], 1):
            engagement_score = tweet.get('engagement_score', 0)
            likes = tweet.get('likes', 0)
            retweets = tweet.get('retweets', 0)
            replies = tweet.get('replies', 0)
            
            st.markdown(f"""
            <div class="tweet-card">
                <h4>#{i} @{tweet['account']}</h4>
                <p>{tweet['content'][:200]}{'...' if len(tweet['content']) > 200 else ''}</p>
                <div style="display: flex; gap: 20px; margin-top: 10px;">
                    <span>🔥 Score: {engagement_score:.1f}</span>
                    <span>❤️ {likes:,}</span>
                    <span>🔄 {retweets:,}</span>
                    <span>💬 {replies:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🏆 No top tweets data available. Run a monitoring cycle to generate data.")

with tab3:
    st.subheader("✍️ Tweet Rewrites")
    
    if data['rewrites']:
        # Rewrite statistics
        total_rewrites = len(data['rewrites'])
        ai_rewrites = sum(1 for r in data['rewrites'] if 'AI-powered' in r.get('rewrite_method', ''))
        rule_rewrites = total_rewrites - ai_rewrites
        high_potential = sum(1 for r in data['rewrites'] if r.get('improvement_potential') == 'High')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤖 AI-Powered", ai_rewrites)
        with col2:
            st.metric("📝 Rule-Based", rule_rewrites)
        with col3:
            st.metric("🚀 High Potential", high_potential)
        
        # Show rewrites
        for i, rewrite in enumerate(data['rewrites'][:10], 1):
            method_color = "#4CAF50" if "AI-powered" in rewrite.get('rewrite_method', '') else "#2196F3"
            potential_emoji = {"High": "🚀", "Medium": "📈", "Low": "📊"}.get(rewrite.get('improvement_potential', 'Medium'), "📊")
            
            st.markdown(f"""
            <div class="rewrite-card">
                <h4>#{i} @{rewrite.get('original_account', 'Unknown')} → @{rewrite.get('reference_account', 'Unknown')}</h4>
                <div style="margin: 10px 0;">
                    <strong>Original:</strong><br>
                    <em>{rewrite['original'][:150]}{'...' if len(rewrite['original']) > 150 else ''}</em>
                </div>
                <div style="margin: 10px 0;">
                    <strong>Rewritten:</strong><br>
                    <strong>{rewrite['rewritten'][:150]}{'...' if len(rewrite['rewritten']) > 150 else ''}</strong>
                </div>
                <div style="display: flex; gap: 15px; margin-top: 10px;">
                    <span style="color: {method_color};">🔧 {rewrite.get('rewrite_method', 'Unknown')}</span>
                    <span>{potential_emoji} {rewrite.get('improvement_potential', 'Medium')} Potential</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✍️ No rewrite data available. Run a monitoring cycle with rewrites enabled.")

with tab4:
    st.subheader("📈 Trending Keywords")
    
    if data['analysis'] and 'trending_keywords' in data['analysis']:
        keywords = data['analysis']['trending_keywords']
        
        # Create two columns for keywords
        col1, col2 = st.columns(2)
        keyword_items = list(keywords.items())
        
        for i, (keyword, count) in enumerate(keyword_items[:20]):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{keyword}</strong>: {count} mentions
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📈 No trending data available. Run a monitoring cycle to generate data.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    🐦 Enhanced AI Tweet Monitor | Real-time monitoring of 100+ AI Twitter accounts<br>
    Last updated: {timestamp}
</div>
""".format(
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
), unsafe_allow_html=True)

# Auto-refresh option
if st.sidebar.checkbox("🔄 Auto-refresh (30s)"):
    import time
    time.sleep(30)
    st.rerun()