import os
import subprocess
import sys
from datetime import datetime

def main():
    """Run the Enhanced AI Tweet Monitor web interface."""
    print("🐦 Enhanced AI Tweet Monitor - Web Interface")
    print("=" * 50)
    print(f"🕒 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if streamlit is available
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed")
    
    # Set environment variables for Heroku
    port = int(os.environ.get("PORT", 8501))
    
    print(f"🌐 Starting web server on port {port}")
    print("🔗 Access your monitor at the provided URL")
    
    # Run Streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(port),
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running server: {str(e)}")

if __name__ == "__main__":
    main()