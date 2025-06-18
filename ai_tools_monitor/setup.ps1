# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -e .

# Install Playwright browsers
playwright install

# Install Chrome WebDriver for Selenium
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

Write-Host "Setup complete! Don't forget to:"
Write-Host "1. Create a .env file with your API keys"
Write-Host "2. Activate the virtual environment: .\venv\Scripts\Activate.ps1" 