import json
import os
from datetime import datetime

def create_enhanced_dashboard():
    """Create an enhanced HTML dashboard for the AI Tweet Monitor with rewrite features."""
    
    # Load data files
    tweets_data = []
    analysis_data = {}
    rewrites_data = []
    top_tweets_data = []
    
    try:
        if os.path.exists('ai_tweets_data.json'):
            with open('ai_tweets_data.json', 'r', encoding='utf-8') as f:
                tweets_data = json.load(f)
    except:
        pass
    
    try:
        if os.path.exists('ai_trends_analysis.json'):
            with open('ai_trends_analysis.json', 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
    except:
        pass
    
    try:
        if os.path.exists('ai_tweet_rewrites.json'):
            with open('ai_tweet_rewrites.json', 'r', encoding='utf-8') as f:
                rewrites_data = json.load(f)
    except:
        pass
    
    try:
        if os.path.exists('ai_top_tweets.json'):
            with open('ai_top_tweets.json', 'r', encoding='utf-8') as f:
                top_tweets_data = json.load(f)
    except:
        pass
    
    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced AI Tweet Monitor Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 3px solid #667eea;
            }}
            
            .header h1 {{
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .header p {{
                color: #666;
                font-size: 1.2em;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            
            .stat-card h3 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: bold;
            }}
            
            .stat-card p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .section {{
                margin-bottom: 40px;
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            }}
            
            .section h2 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-left: 4px solid #667eea;
                padding-left: 15px;
            }}
            
            .rewrite-section {{
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                border: 2px solid #667eea;
            }}
            
            .rewrite-card {{
                background: white;
                margin: 15px 0;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #f5576c;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}
            
            .rewrite-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                flex-wrap: wrap;
                gap: 10px;
            }}
            
            .rewrite-method {{
                background: #667eea;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
            }}
            
            .improvement-badge {{
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
            }}
            
            .improvement-high {{
                background: #4CAF50;
                color: white;
            }}
            
            .improvement-medium {{
                background: #FF9800;
                color: white;
            }}
            
            .improvement-low {{
                background: #9E9E9E;
                color: white;
            }}
            
            .tweet-content {{
                margin: 10px 0;
                padding: 15px;
                border-radius: 8px;
                line-height: 1.5;
            }}
            
            .original-tweet {{
                background: #f8f9fa;
                border-left: 3px solid #dc3545;
            }}
            
            .rewritten-tweet {{
                background: #e8f5e8;
                border-left: 3px solid #28a745;
            }}
            
            .tweet-label {{
                font-weight: bold;
                color: #666;
                font-size: 0.9em;
                margin-bottom: 8px;
            }}
            
            .keyword-tag {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 10px;
                margin: 5px;
                border-radius: 20px;
                font-size: 0.9em;
            }}
            
            .account-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                margin: 10px 0;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }}
            
            .account-name {{
                font-weight: bold;
                color: #333;
            }}
            
            .account-score {{
                background: #28a745;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
            }}
            
            .top-tweet {{
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 20px;
                margin: 15px 0;
                border-radius: 15px;
                border-left: 5px solid #f5576c;
            }}
            
            .tweet-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                flex-wrap: wrap;
                gap: 10px;
            }}
            
            .engagement-stats {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}
            
            .engagement-stat {{
                background: rgba(255,255,255,0.8);
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.9em;
                font-weight: bold;
            }}
            
            .last-updated {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                color: #666;
            }}
            
            .ai-status {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                margin-left: 10px;
            }}
            
            .ai-enabled {{
                background: #4CAF50;
                color: white;
            }}
            
            .ai-disabled {{
                background: #FF9800;
                color: white;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 15px;
                }}
                
                .header h1 {{
                    font-size: 2em;
                }}
                
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .rewrite-header {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                
                .tweet-meta {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                
                .engagement-stats {{
                    justify-content: flex-start;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🐦 Enhanced AI Tweet Monitor</h1>
                <p>Tracking 100+ AI Twitter accounts with intelligent tweet rewriting</p>
                <span class="ai-status {'ai-enabled' if analysis_data.get('openai_status') == 'Available' else 'ai-disabled'}">
                    {'🤖 AI-Powered Rewriting' if analysis_data.get('openai_status') == 'Available' else '📝 Rule-Based Rewriting'}
                </span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>{len(tweets_data)}</h3>
                    <p>📱 Total Tweets</p>
                </div>
                <div class="stat-card">
                    <h3>{analysis_data.get('total_accounts', 0)}</h3>
                    <p>🏢 AI Accounts</p>
                </div>
                <div class="stat-card">
                    <h3>{analysis_data.get('total_engagement', 0):,}</h3>
                    <p>💬 Total Engagement</p>
                </div>
                <div class="stat-card">
                    <h3>{len(rewrites_data)}</h3>
                    <p>✍️ Tweet Rewrites</p>
                </div>
            </div>
    """
    
    # Add rewrite section if data exists
    if rewrites_data:
        ai_rewrites = sum(1 for r in rewrites_data if 'AI-powered' in r.get('rewrite_method', ''))
        rule_rewrites = len(rewrites_data) - ai_rewrites
        high_potential = sum(1 for r in rewrites_data if r.get('improvement_potential') == 'High')
        
        html_content += f"""
            <div class="section rewrite-section">
                <h2>✍️ Tweet Rewrite Analysis</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>{ai_rewrites}</h3>
                        <p>🤖 AI-Powered</p>
                    </div>
                    <div class="stat-card">
                        <h3>{rule_rewrites}</h3>
                        <p>📝 Rule-Based</p>
                    </div>
                    <div class="stat-card">
                        <h3>{high_potential}</h3>
                        <p>🎯 High Potential</p>
                    </div>
                </div>
                
                <h3 style="margin: 30px 0 20px 0; color: #333;">📝 Sample Rewrites</h3>
        """
        
        # Show first 5 rewrites
        for i, rewrite in enumerate(rewrites_data[:5]):
            improvement_class = f"improvement-{rewrite.get('improvement_potential', 'medium').lower()}"
            
            html_content += f"""
                <div class="rewrite-card">
                    <div class="rewrite-header">
                        <div>
                            <strong>@{rewrite.get('original_account', 'Unknown')}</strong>
                            <span style="color: #666; margin-left: 10px;">→ Style from @{rewrite.get('reference_account', 'Unknown')}</span>
                        </div>
                        <div>
                            <span class="rewrite-method">{rewrite.get('rewrite_method', 'Unknown')}</span>
                            <span class="improvement-badge {improvement_class}">{rewrite.get('improvement_potential', 'Medium')} Potential</span>
                        </div>
                    </div>
                    
                    <div class="tweet-content original-tweet">
                        <div class="tweet-label">Original:</div>
                        {rewrite.get('original', 'N/A')[:200]}{'...' if len(rewrite.get('original', '')) > 200 else ''}
                    </div>
                    
                    <div class="tweet-content rewritten-tweet">
                        <div class="tweet-label">Rewritten:</div>
                        {rewrite.get('rewritten', 'N/A')[:200]}{'...' if len(rewrite.get('rewritten', '')) > 200 else ''}
                    </div>
                </div>
            """
        
        html_content += "</div>"
    
    # Add top tweets section
    if top_tweets_data:
        html_content += f"""
            <div class="section">
                <h2>🏆 Top Performing Tweets</h2>
        """
        
        for i, tweet in enumerate(top_tweets_data[:5], 1):
            html_content += f"""
                <div class="top-tweet">
                    <div class="tweet-meta">
                        <div>
                            <strong>#{i} @{tweet.get('account', 'Unknown')}</strong>
                        </div>
                        <div class="engagement-stats">
                            <span class="engagement-stat">❤️ {tweet.get('likes', 0):,}</span>
                            <span class="engagement-stat">🔄 {tweet.get('retweets', 0):,}</span>
                            <span class="engagement-stat">💬 {tweet.get('replies', 0):,}</span>
                            <span class="engagement-stat">📊 {tweet.get('engagement_score', 0):.0f}</span>
                        </div>
                    </div>
                    <div style="margin-top: 15px; line-height: 1.5;">
                        {tweet.get('content', 'N/A')[:300]}{'...' if len(tweet.get('content', '')) > 300 else ''}
                    </div>
                </div>
            """
        
        html_content += "</div>"
    
    # Add trending keywords
    if analysis_data.get('trending_keywords'):
        html_content += f"""
            <div class="section">
                <h2>🔥 Trending Keywords</h2>
                <div style="margin-top: 20px;">
        """
        
        for keyword, count in list(analysis_data['trending_keywords'].items())[:15]:
            html_content += f'<span class="keyword-tag">{keyword} ({count})</span>'
        
        html_content += "</div></div>"
    
    # Add top accounts
    if analysis_data.get('top_performing_accounts'):
        html_content += f"""
            <div class="section">
                <h2>🏆 Top Performing Accounts</h2>
        """
        
        for account_data in analysis_data['top_performing_accounts'][:10]:
            html_content += f"""
                <div class="account-item">
                    <div>
                        <span class="account-name">@{account_data.get('account', 'Unknown')}</span>
                        <span style="color: #666; margin-left: 10px;">({account_data.get('tweets', 0)} tweets)</span>
                    </div>
                    <span class="account-score">{account_data.get('avg_score', 0):.1f}</span>
                </div>
            """
        
        html_content += "</div>"
    
    # Add footer
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_analysis = analysis_data.get('analysis_timestamp', 'Never')
    
    html_content += f"""
            <div class="last-updated">
                <p><strong>Dashboard Generated:</strong> {current_time}</p>
                <p><strong>Last Analysis:</strong> {last_analysis}</p>
                <p><strong>Status:</strong> Enhanced AI Tweet Monitor with Rewrite Capabilities</p>
                <p style="margin-top: 15px; font-style: italic;">
                    Monitoring 100+ AI Twitter accounts • Intelligent tweet rewriting • Real-time trend analysis
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save the dashboard
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Enhanced dashboard created successfully!")
    print("📊 Features included:")
    print(f"   • {len(tweets_data)} tweets analyzed")
    print(f"   • {len(rewrites_data)} tweet rewrites generated")
    print(f"   • {len(top_tweets_data)} top performing tweets")
    print(f"   • Trending keywords and account performance")
    print("🌐 Open 'dashboard.html' in your browser to view the enhanced interface")

if __name__ == "__main__":
    create_enhanced_dashboard()