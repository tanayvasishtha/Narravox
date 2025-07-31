#!/usr/bin/env python3
"""
Narravox Development Server Launcher
Fixes common Streamlit server issues and CSP problems
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up environment variables for the server."""
    env_vars = {
        'PERPLEXITY_API_KEY': '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',
        'QLOO_API_KEY': 'SpdNKtyqJCuwGRddpnxJ3JoAyytrIAXfwGoDqu6ycbc',
        'QLOO_BASE_URL': 'https://hackathon.api.qloo.com',
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✓ Environment variables configured")

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import requests
        from dotenv import load_dotenv
        import reportlab
        print("✓ All dependencies available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def start_streamlit_server():
    """Start the Streamlit server with proper configuration."""
    print("🚀 Starting Narravox development server...")
    
    # Streamlit command with all necessary flags
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.address', '0.0.0.0',
        '--server.port', '8501',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--browser.gatherUsageStats', 'false'
    ]
    
    try:
        # Start the server
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Server failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

def main():
    """Main function to start the Narravox server."""
    print("=" * 50)
    print("NARRAVOX DEVELOPMENT SERVER")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("✗ app.py not found. Please run from the Narravox project directory.")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("Please install missing dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start server
    print("🌐 Server will be available at:")
    print("   Local:    http://localhost:8501")
    print("   Network:  http://0.0.0.0:8501")
    print("\n📝 Press Ctrl+C to stop the server\n")
    
    start_streamlit_server()

if __name__ == "__main__":
    main()