from setuptools import setup, find_packages

setup(
    name="ai_tools_monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "playwright>=1.40.0",
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.0",
        "praw>=7.7.0",
        "tweepy>=4.14.0",
        "python-dotenv>=1.0.0",
        "asyncio>=3.4.3",
        "aiofiles>=23.2.1",
        "tenacity>=8.2.0",
        "fake-useragent>=1.4.0",
    ],
    python_requires=">=3.8",
) 