# 🐦 Enhanced AI Tweet Monitor

A powerful Streamlit-based dashboard for monitoring AI trends and tools from Twitter with advanced analytics and AI-powered insights.

## ✨ Features

- 🐦 **Twitter Integration**: Real-time AI tool mentions and trends
- 🔍 **Smart Analytics**: Sentiment analysis and trend detection  
- 🤖 **AI-Powered**: Content analysis using OpenAI and Anthropic
- 📊 **Interactive Dashboard**: Beautiful Streamlit interface
- 📈 **Real-time Monitoring**: Live updates and notifications
- 🎯 **Customizable Filters**: Focus on specific AI topics

## 🚀 Quick Deploy

### Deploy to Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sodown4thecause/enhanced-ai-tweet-monitor)

**One-click deployment to Render's free tier!**

1. Click the deploy button above
2. Set your environment variables (see below)
3. Deploy and enjoy!

### Manual Deployment Options

#### Option 1: Render
1. Fork this repository
2. Connect to [Render](https://render.com)
3. Create new Web Service from your repo
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables (see below)

#### Option 2: Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file: `streamlit_app.py`
4. Add environment variables

#### Option 3: Railway
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`
4. Add environment variables in dashboard

## 🔑 Environment Variables

Add these in your deployment platform:

### Required
```
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
```

### Optional (for AI features)
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## 🛠️ Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sodown4thecause/enhanced-ai-tweet-monitor.git
   cd enhanced-ai-tweet-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📚 Documentation

- [📖 Quick Start Guide](QUICK_START.md)
- [🚀 Render Deployment Guide](RENDER_DEPLOYMENT.md)
- [🔧 Development Guide](DEPLOYMENT_GUIDE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- 📖 Check the [documentation](RENDER_DEPLOYMENT.md)
- 🐛 [Report issues](https://github.com/sodown4thecause/enhanced-ai-tweet-monitor/issues)
- 💬 [Discussions](https://github.com/sodown4thecause/enhanced-ai-tweet-monitor/discussions)

---

**Made with ❤️ for the AI community**