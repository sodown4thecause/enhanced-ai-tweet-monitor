# AI Tools Monitor

A Streamlit-based dashboard for monitoring AI tools from multiple sources including Twitter, TopAI.tools, and Archon.

## Features

- 🐦 Twitter API integration for AI tool mentions
- 🔍 Web scraping from TopAI.tools
- 📊 Real-time analytics and sentiment analysis
- 🤖 AI-powered content analysis using OpenAI
- 📈 Trend analysis and monitoring

## Deployment

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to: `src/streamlit_app.py`
5. Add your environment variables in the Streamlit Cloud dashboard:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `OPENAI_API_KEY`

### Option 2: Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`
4. Add environment variables in Railway dashboard

### Option 3: Render

1. Connect your GitHub repository to Render
2. Choose "Web Service"
3. Set build command: `pip install -r requirements-deploy.txt`
4. Set start command: `streamlit run src/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables

### Option 4: Heroku

1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set TWITTER_API_KEY=your_key`
4. Deploy: `git push heroku main`

## Environment Variables

Make sure to set these environment variables in your deployment platform:

```
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
OPENAI_API_KEY=your_openai_api_key
```

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your API keys
4. Run: `streamlit run src/streamlit_app.py`

## Usage

1. Configure your API credentials in the sidebar
2. Click "Fetch Tools" to start monitoring
3. View real-time analytics and trends in the dashboard