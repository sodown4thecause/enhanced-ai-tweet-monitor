import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

def check_ai_tweet_monitor_status():
    """Check the status of the Enhanced AI Tweet Monitor system."""
    print("🐦 Enhanced AI Tweet Monitor - System Status Check")
    print("="*60)
    
    # Load environment variables
    load_dotenv()
    
    # Check API configuration
    twitter_configured = bool(os.getenv('TWITTER_API_KEY'))
    openai_configured = bool(os.getenv('OPENAI_API_KEY'))
    
    print(f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # API Configuration Status
    print("🔑 API Configuration:")
    print(f"   Twitter API: {'✅ Configured' if twitter_configured else '❌ Missing'}")
    print(f"   OpenAI API:  {'✅ Configured' if openai_configured else '❌ Missing'}")
    print(f"   Rewrite Mode: {'🤖 AI-Powered' if openai_configured else '📝 Rule-Based'}")
    print()
    
    # Check for data files
    print("📊 Data Files:")
    files_status = {
        "Tweet Data": "ai_tweets_data.json",
        "Analysis Data": "ai_trends_analysis.json",
        "Tweet Rewrites": "ai_tweet_rewrites.json",
        "Top Tweets": "ai_top_tweets.json",
        "Dashboard": "dashboard.html"
    }
    
    for name, filename in files_status.items():
        if os.path.exists(filename):
            file_time = datetime.fromtimestamp(os.path.getmtime(filename))
            age = datetime.now() - file_time
            age_str = f"{age.seconds//60} minutes ago" if age.seconds < 3600 else f"{age.seconds//3600} hours ago"
            print(f"   {name}: ✅ Available (Updated {age_str})")
        else:
            print(f"   {name}: ❌ Not found")
    
    print()
    
    # Check recent activity
    if os.path.exists("ai_trends_analysis.json"):
        try:
            with open("ai_trends_analysis.json", 'r', encoding='utf-8') as f:
                analysis = json.load(f)
            
            print("📈 Latest Analysis Summary:")
            print(f"   Total Tweets: {analysis.get('total_tweets', 0)}")
            print(f"   AI Accounts: {analysis.get('total_accounts', 0)}")
            print(f"   Total Engagement: {analysis.get('total_engagement', 0):,}")
            print(f"   Average Engagement: {analysis.get('avg_engagement', 0)}")
            
            trending = analysis.get('trending_keywords', {})
            if trending:
                top_keyword = max(trending.items(), key=lambda x: x[1])
                print(f"   Top Trending: '{top_keyword[0]}' ({top_keyword[1]} mentions)")
            
            top_accounts = analysis.get('top_performing_accounts', [])
            if top_accounts:
                print(f"   Best Account: @{top_accounts[0]['account']} (Score: {top_accounts[0]['avg_score']:.1f})")
            
            print(f"   Last Updated: {analysis.get('analysis_timestamp', 'Unknown')}")
            
        except Exception as e:
            print(f"   ❌ Error reading analysis: {str(e)}")
    
    # Check rewrite data
    if os.path.exists("ai_tweet_rewrites.json"):
        try:
            with open("ai_tweet_rewrites.json", 'r', encoding='utf-8') as f:
                rewrites = json.load(f)
            
            print(f"\n✍️ Tweet Rewrite Summary:")
            print(f"   Total Rewrites: {len(rewrites)}")
            
            ai_powered = sum(1 for r in rewrites if r.get('rewrite_method') == 'AI-powered')
            rule_based = len(rewrites) - ai_powered
            
            print(f"   AI-Powered: {ai_powered}")
            print(f"   Rule-Based: {rule_based}")
            
            if rewrites:
                high_potential = sum(1 for r in rewrites if r.get('improvement_potential') == 'High')
                print(f"   High Improvement Potential: {high_potential}")
                
        except Exception as e:
            print(f"   ❌ Error reading rewrites: {str(e)}")
    
    print()
    
    # System recommendations
    print("💡 Recommendations:")
    if not twitter_configured:
        print("   • Add TWITTER_API_KEY to .env file for real Twitter monitoring")
    if not openai_configured:
        print("   • Add OPENAI_API_KEY to .env file for AI-powered tweet rewriting")
        print("   • Currently using rule-based rewriting (still effective!)")
    
    if twitter_configured and openai_configured:
        print("   • ✅ All APIs configured - full AI-powered functionality enabled!")
    
    print("   • Run 'python ai_tweet_monitor.py' to start monitoring 100+ accounts")
    print("   • Choose option 1 for single cycle with tweet rewriting")
    print("   • Choose option 3 for continuous monitoring with rewrites")
    print("   • Open 'dashboard.html' in browser to view web interface")
    
    print()
    print("🚀 Enhanced AI Tweet Monitor Status: READY FOR 100+ ACCOUNTS")
    print("="*60)

def show_rewrite_examples():
    """Show examples of tweet rewrites if available."""
    if not os.path.exists("ai_tweet_rewrites.json"):
        print("✍️ No rewrite data available yet.")
        print("   Run monitoring with rewrites to see examples.")
        return
    
    try:
        with open("ai_tweet_rewrites.json", 'r', encoding='utf-8') as f:
            rewrites = json.load(f)
        
        if not rewrites:
            print("✍️ No rewrites in data file.")
            return
        
        print("\n✍️ Tweet Rewrite Examples:")
        print("-" * 50)
        
        for i, rewrite in enumerate(rewrites[:3], 1):  # Show first 3 examples
            print(f"\n📝 Example {i}:")
            print(f"   Account: @{rewrite.get('original_account', 'Unknown')}")
            print(f"   Method: {rewrite.get('rewrite_method', 'Unknown')}")
            print(f"   Potential: {rewrite.get('improvement_potential', 'Unknown')}")
            print(f"   \n   Original:  {rewrite.get('original', 'N/A')[:100]}...")
            print(f"   Rewritten: {rewrite.get('rewritten', 'N/A')[:100]}...")
            print(f"   Reference: @{rewrite.get('reference_account', 'Unknown')}")
        
        print(f"\n📊 Rewrite Statistics:")
        ai_count = sum(1 for r in rewrites if r.get('rewrite_method') == 'AI-powered')
        high_potential = sum(1 for r in rewrites if r.get('improvement_potential') == 'High')
        
        print(f"   Total Rewrites: {len(rewrites)}")
        print(f"   AI-Powered: {ai_count} ({ai_count/len(rewrites)*100:.1f}%)")
        print(f"   High Potential: {high_potential} ({high_potential/len(rewrites)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error reading rewrite data: {str(e)}")

def show_top_performers():
    """Show top performing tweets and accounts."""
    if not os.path.exists("ai_top_tweets.json"):
        print("🏆 No top performer data available yet.")
        return
    
    try:
        with open("ai_top_tweets.json", 'r', encoding='utf-8') as f:
            top_tweets = json.load(f)
        
        if not top_tweets:
            print("🏆 No top tweets in data file.")
            return
        
        print("\n🏆 Top Performing Tweets:")
        print("-" * 50)
        
        for i, tweet in enumerate(top_tweets[:5], 1):  # Show top 5
            print(f"\n#{i} @{tweet['account']}")
            print(f"   Content: {tweet['content'][:80]}...")
            print(f"   Engagement Score: {tweet.get('engagement_score', 0):.1f}")
            print(f"   Likes: {tweet.get('likes', 0):,} | Retweets: {tweet.get('retweets', 0):,} | Replies: {tweet.get('replies', 0):,}")
        
    except Exception as e:
        print(f"❌ Error reading top tweets: {str(e)}")

def show_quick_stats():
    """Show comprehensive quick statistics."""
    if not os.path.exists("ai_tweets_data.json"):
        print("📊 No monitoring data available yet.")
        print("   Run 'python ai_tweet_monitor.py' to collect data from 100+ accounts.")
        return
    
    try:
        with open("ai_tweets_data.json", 'r', encoding='utf-8') as f:
            tweets = json.load(f)
        
        if not tweets:
            print("📊 No tweets in data file.")
            return
        
        print("\n📊 Comprehensive Stats from Latest Data:")
        print("-" * 50)
        
        # Account activity
        accounts = {}
        total_engagement = 0
        total_likes = 0
        total_retweets = 0
        
        for tweet in tweets:
            account = tweet.get('account', 'Unknown')
            accounts[account] = accounts.get(account, 0) + 1
            total_engagement += tweet.get('engagement_score', tweet.get('engagement', 0))
            total_likes += tweet.get('likes', 0)
            total_retweets += tweet.get('retweets', 0)
        
        print(f"📱 Total Tweets: {len(tweets)}")
        print(f"🏢 Active Accounts: {len(accounts)}")
        print(f"💬 Total Engagement Score: {total_engagement:,.0f}")
        print(f"❤️ Total Likes: {total_likes:,}")
        print(f"🔄 Total Retweets: {total_retweets:,}")
        print(f"📈 Avg Engagement per Tweet: {total_engagement/len(tweets):.1f}")
        
        # Top accounts by activity
        top_accounts = sorted(accounts.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n🏆 Most Active Accounts:")
        for i, (account, count) in enumerate(top_accounts, 1):
            print(f"   {i}. @{account}: {count} tweets")
        
        # Recent activity
        latest_tweet = max(tweets, key=lambda x: x.get('timestamp', ''))
        print(f"\n⏰ Latest Tweet: @{latest_tweet.get('account', 'Unknown')}")
        print(f"   Time: {latest_tweet.get('timestamp', 'Unknown')}")
        print(f"   Engagement: {latest_tweet.get('engagement_score', 0):.1f}")
        
    except Exception as e:
        print(f"❌ Error reading tweet data: {str(e)}")

if __name__ == "__main__":
    check_ai_tweet_monitor_status()
    show_quick_stats()
    show_top_performers()
    show_rewrite_examples()