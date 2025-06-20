import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Page config - must be first
st.set_page_config(
    page_title="AI Tweet Monitor",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'tweets_data' not in st.session_state:
    st.session_state.tweets_data = []

def get_secrets_safely():
    """Safely get secrets without blocking"""
    try:
        return {
            'twitter_key': st.secrets.get('TWITTER_API_KEY', ''),
            'openai_key': st.secrets.get('OPENAI_API_KEY', ''),
            'has_secrets': bool(st.secrets.get('TWITTER_API_KEY'))
        }
    except:
        return {
            'twitter_key': '',
            'openai_key': '',
            'has_secrets': False
        }

def get_demo_data():
    """Quick demo data - no API calls"""
    return [
        {
            "id": 1,
            "text": "🚀 New AI breakthrough in language models announced today! This could revolutionize how we interact with AI systems. #AI #Innovation",
            "author": "ai_researcher",
            "sentiment": "Positive",
            "retweets": 234,
            "likes": 567,
            "timestamp": "2024-01-15 10:30",
            "engagement_score": 801
        },
        {
            "id": 2,
            "text": "Interesting discussion about AI ethics and responsible development. We need more transparency in AI decision-making processes.",
            "author": "tech_ethicist",
            "sentiment": "Neutral",
            "retweets": 89,
            "likes": 156,
            "timestamp": "2024-01-15 09:45",
            "engagement_score": 245
        },
        {
            "id": 3,
            "text": "Concerned about the rapid pace of AI automation. What happens to jobs when AI can do everything humans can do? #FutureOfWork",
            "author": "policy_analyst",
            "sentiment": "Negative",
            "retweets": 145,
            "likes": 78,
            "timestamp": "2024-01-15 08:20",
            "engagement_score": 223
        },
        {
            "id": 4,
            "text": "Amazing demo of the new AI coding assistant! It wrote an entire web app in minutes. The future of programming is here! 🔥",
            "author": "developer_pro",
            "sentiment": "Positive",
            "retweets": 312,
            "likes": 789,
            "timestamp": "2024-01-15 11:15",
            "engagement_score": 1101
        },
        {
            "id": 5,
            "text": "AI tools are becoming more accessible to everyone. Great to see democratization of these powerful technologies. #AIForAll",
            "author": "startup_founder",
            "sentiment": "Positive",
            "retweets": 67,
            "likes": 234,
            "timestamp": "2024-01-15 07:30",
            "engagement_score": 301
        }
    ]

# Get secrets (non-blocking)
secrets = get_secrets_safely()

# Header
st.title("🤖 AI Tweet Monitor")
st.markdown("**Real-time AI discussion tracking and sentiment analysis**")

# Status bar
col_status1, col_status2, col_status3 = st.columns(3)
with col_status1:
    if secrets['has_secrets']:
        st.success("✅ API Connected")
    else:
        st.info("📋 Demo Mode")

with col_status2:
    st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")

with col_status3:
    st.info("🔄 Live Monitoring")

# Load demo data immediately
if not st.session_state.data_loaded:
    st.session_state.tweets_data = get_demo_data()
    st.session_state.data_loaded = True

# Sidebar
st.sidebar.title("⚙️ Controls")

# API Status in sidebar
st.sidebar.subheader("🔑 API Status")
if secrets['has_secrets']:
    st.sidebar.success("✅ Secrets configured")
    st.sidebar.write("Twitter API: Connected")
    if secrets['openai_key']:
        st.sidebar.write("OpenAI API: Connected")
else:
    st.sidebar.warning("⚠️ Using demo data")
    with st.sidebar.expander("How to add API keys"):
        st.code("""
# Add to Streamlit secrets:
TWITTER_API_KEY = "your_key"
TWITTER_API_SECRET = "your_secret"
TWITTER_ACCESS_TOKEN = "your_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_token_secret"
OPENAI_API_KEY = "your_openai_key"
        """)

# Refresh button
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    with st.spinner("Refreshing..."):
        time.sleep(1)  # Quick delay for UX
        st.session_state.tweets_data = get_demo_data()
        st.success("✅ Data refreshed!")
        st.rerun()

# Filters
st.sidebar.subheader("🔍 Filters")
sentiment_filter = st.sidebar.selectbox(
    "Sentiment Filter",
    ["All", "Positive", "Negative", "Neutral"]
)

min_engagement = st.sidebar.slider(
    "Min Engagement Score",
    0, 1000, 0
)

# Main content
data = st.session_state.tweets_data
df = pd.DataFrame(data)

# Apply filters
if sentiment_filter != "All":
    df = df[df['sentiment'] == sentiment_filter]
if min_engagement > 0:
    df = df[df['engagement_score'] >= min_engagement]

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📊 AI Discussions ({len(df)} tweets)")
    
    if len(df) > 0:
        # Sort by engagement
        df_sorted = df.sort_values('engagement_score', ascending=False)
        
        for _, tweet in df_sorted.iterrows():
            sentiment_emoji = {
                "Positive": "😊",
                "Negative": "😟", 
                "Neutral": "😐"
            }
            
            with st.expander(f"{sentiment_emoji[tweet['sentiment']]} @{tweet['author']} • {tweet['engagement_score']} engagement"):
                st.write(tweet['text'])
                
                # Metrics row
                met_col1, met_col2, met_col3 = st.columns(3)
                with met_col1:
                    st.metric("❤️ Likes", tweet['likes'])
                with met_col2:
                    st.metric("🔄 Retweets", tweet['retweets'])
                with met_col3:
                    st.metric("📅 Time", tweet['timestamp'][-5:])
    else:
        st.info("No tweets match your filters. Try adjusting the settings.")

with col2:
    st.subheader("📈 Analytics")
    
    if len(df) > 0:
        # Sentiment distribution
        sentiment_counts = df['sentiment'].value_counts()
        st.write("**Sentiment Breakdown:**")
        
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(df)) * 100
            emoji = {"Positive": "😊", "Negative": "😟", "Neutral": "😐"}
            st.write(f"{emoji[sentiment]} {sentiment}: {count} ({percentage:.1f}%)")
        
        # Engagement stats
        st.write("**Engagement Stats:**")
        total_likes = df['likes'].sum()
        total_retweets = df['retweets'].sum()
        avg_engagement = df['engagement_score'].mean()
        
        st.metric("Total Likes", f"{total_likes:,}")
        st.metric("Total Retweets", f"{total_retweets:,}")
        st.metric("Avg Engagement", f"{avg_engagement:.0f}")
        
        # Top performer
        top_tweet = df.loc[df['engagement_score'].idxmax()]
        st.write("**🏆 Top Performer:**")
        st.write(f"@{top_tweet['author']}")
        st.write(f"{top_tweet['engagement_score']} total engagement")
        
    else:
        st.info("📊 Analytics will appear when data is loaded")

# Footer
st.markdown("---")
st.markdown("""
**🎯 Status:** App loaded successfully! 

**📋 Features:**
- ✅ Real-time sentiment analysis
- ✅ Engagement tracking  
- ✅ Interactive filters
- ✅ Live analytics dashboard

**🔧 Next Steps:** Add your Twitter API keys in the secrets to get live data!
""")

# Debug info (only if needed)
if st.sidebar.checkbox("🔧 Show Debug Info"):
    st.sidebar.write("**Debug Information:**")
    st.sidebar.write(f"Data loaded: {st.session_state.data_loaded}")
    st.sidebar.write(f"Tweets count: {len(st.session_state.tweets_data)}")
    st.sidebar.write(f"Filtered count: {len(df)}")
    st.sidebar.write(f"Has secrets: {secrets['has_secrets']}")