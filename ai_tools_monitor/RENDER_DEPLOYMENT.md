# 🚀 Render Deployment Guide

## Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

1. **Click the Deploy Button** (once we add it to README)
2. **Set Environment Variables** in Render dashboard
3. **Deploy!**

### Option 2: Manual Deployment

#### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

#### Step 2: Deploy from GitHub
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `enhanced-ai-tweet-monitor`
3. Configure the service:
   - **Name**: `enhanced-ai-tweet-monitor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

#### Step 3: Set Environment Variables
In the Render dashboard, add these environment variables:

**Required:**
- `TWITTER_API_KEY` = your_twitter_api_key
- `TWITTER_API_SECRET` = your_twitter_api_secret  
- `TWITTER_ACCESS_TOKEN` = your_twitter_access_token
- `TWITTER_ACCESS_TOKEN_SECRET` = your_twitter_access_token_secret

**Optional:**
- `OPENAI_API_KEY` = your_openai_api_key
- `ANTHROPIC_API_KEY` = your_anthropic_api_key

#### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## 🔧 Configuration Details

### Build Settings
- **Environment**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### Environment Variables
All API keys should be added in the Render dashboard under "Environment Variables"

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- 750 hours/month free usage
- Slower cold starts

## 🚨 Important Notes

1. **Never commit API keys** - Always use environment variables
2. **Free tier sleeps** - App may take 30-60 seconds to wake up
3. **Build time** - First deployment takes 5-10 minutes
4. **Logs** - Check Render dashboard for deployment logs

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Streamlit on Render](https://render.com/docs/deploy-streamlit)
- [Environment Variables](https://render.com/docs/environment-variables)

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt for compatibility
2. **App won't start**: Verify start command and port configuration
3. **Environment variables**: Ensure all required keys are set
4. **Import errors**: Check Python path and module imports

### Getting Help:
- Check Render logs in dashboard
- Review this guide
- Check GitHub issues