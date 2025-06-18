try:
    import tweepy
    print(f"Tweepy version: {tweepy.__version__}")
except Exception as e:
    print(f"Tweepy import error: {e}")

try:
    import playwright
    print(f"Playwright version: {playwright.__version__}")
except Exception as e:
    print(f"Playwright import error: {e}") 