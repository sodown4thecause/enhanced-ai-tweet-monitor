@echo off
REM 🚀 Enhanced AI Tweet Monitor - Quick Setup Script for Windows

echo 🐦 Enhanced AI Tweet Monitor - Quick Setup
echo ==========================================

REM Check if git is initialized
if not exist ".git" (
    echo 📝 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - Enhanced AI Tweet Monitor"
) else (
    echo ✅ Git repository already initialized
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements-deploy.txt

REM Test local setup
echo 🧪 Testing local setup...
python -c "import tweepy, streamlit; print('✅ All dependencies installed successfully')"

echo.
echo 🚀 Setup complete! Choose your deployment option:
echo.
echo 1️⃣  HEROKU (Recommended for beginners)
echo    heroku create your-ai-tweet-monitor
echo    heroku config:set TWITTER_API_KEY=GcYxXIDIqPSxtxRPe1941XKdo
echo    heroku config:set TWITTER_API_SECRET=BMDWR7RBxVPlqeepuWPDz2mC7kXtqtk9ZgQ0OinI7IlnVyHWSa
echo    heroku config:set TWITTER_ACCESS_TOKEN=AAAAAAAAAAAAAAAAAAAAADf02AEAAAAA2%%2BFJY3Icc%%2Bz%%2FX%%2FjzQzPrySV7M7g%%3D22dIjxRV3E0VZB9jLDLSoMiDOjtd4Ni0EyqcRqPr8BiCfc6d6L
echo    heroku config:set TWITTER_ACCESS_TOKEN_SECRET=WEl8VIoDXH1zAKtfIUzJKXDPeMIv7SAIf1b4rEu8adk9U
echo    git push heroku main
echo.
echo 2️⃣  STREAMLIT CLOUD (Perfect for Streamlit apps)
echo    - Push to GitHub
echo    - Go to share.streamlit.io
echo    - Deploy from GitHub repo
echo.
echo 3️⃣  RAILWAY (Modern ^& easy)
echo    - Go to railway.app
echo    - Deploy from GitHub repo
echo.
echo 4️⃣  Test locally first:
echo    streamlit run streamlit_app.py
echo.
echo 📖 Full deployment guide: DEPLOYMENT_GUIDE.md
echo ✅ Your Enhanced AI Tweet Monitor is ready to deploy!

pause