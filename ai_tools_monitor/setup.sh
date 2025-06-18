#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -e .

# Install Playwright browsers
playwright install

# Install Chrome WebDriver for Selenium
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

echo "Setup complete! Don't forget to:"
echo "1. Create a .env file with your API keys"
echo "2. Activate the virtual environment: source venv/bin/activate" 