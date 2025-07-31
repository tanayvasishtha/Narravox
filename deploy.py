#!/usr/bin/env python3
"""
Narravox Deployment Script
Helps prepare the application for deployment
"""
import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    required_vars = ['PERPLEXITY_API_KEY', 'QLOO_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your deployment environment.")
        return False
    else:
        print("✅ All environment variables are set")
        return True

def check_dependencies():
    """Check if all dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    try:
        import streamlit
        import requests
        from dotenv import load_dotenv
        import reportlab
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_files():
    """Check if all required files exist."""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'README.md',
        '.gitignore',
        'api/perplexity_service.py',
        'api/qloo_service.py',
        'utils/session_manager.py',
        'utils/export_utils.py',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def run_tests():
    """Run basic functionality tests."""
    print("\n🔍 Running basic tests...")
    
    try:
        # Test imports
        from api.perplexity_service import PerplexityService
        from api.qloo_service import QlooService
        from utils.session_manager import SessionManager
        from utils.export_utils import ExportUtils
        
        print("✅ All modules import successfully")
        
        # Test service initialization
        perplexity = PerplexityService()
        qloo = QlooService()
        
        if perplexity.api_key and qloo.api_key:
            print("✅ API services initialized successfully")
            return True
        else:
            print("⚠️ API keys not found in environment")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main deployment check function."""
    print("=" * 50)
    print("NARRAVOX DEPLOYMENT CHECK")
    print("=" * 50)
    
    env_ok = check_environment()
    deps_ok = check_dependencies()
    files_ok = check_files()
    tests_ok = run_tests()
    
    print("\n" + "=" * 50)
    print("DEPLOYMENT STATUS")
    print("=" * 50)
    
    if env_ok and deps_ok and files_ok and tests_ok:
        print("✅ READY FOR DEPLOYMENT")
        print("\nYour Narravox application is ready to deploy!")
        print("\nDeployment options:")
        print("1. Render: Push to GitHub and connect to Render")
        print("2. Heroku: Use heroku create and git push heroku main")
        print("3. Railway: Connect GitHub repository to Railway")
        print("4. Vercel: Use vercel --prod")
    else:
        print("❌ NOT READY FOR DEPLOYMENT")
        print("\nPlease fix the issues above before deploying.")
        
        if not env_ok:
            print("- Set environment variables in your deployment platform")
        if not deps_ok:
            print("- Install missing dependencies")
        if not files_ok:
            print("- Ensure all required files are present")
        if not tests_ok:
            print("- Check API keys and service configuration")

if __name__ == "__main__":
    main() 