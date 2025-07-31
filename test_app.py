#!/usr/bin/env python3
"""
Simple test script to verify Narravox components are working
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if environment variables are loaded."""
    print("🔍 Testing Environment Variables...")
    
    perplexity_key = os.getenv('PERPLEXITY_API_KEY')
    qloo_key = os.getenv('QLOO_API_KEY')
    qloo_url = os.getenv('QLOO_BASE_URL')
    
    print(f"PERPLEXITY_API_KEY: {'✅ Set' if perplexity_key else '❌ Missing'}")
    print(f"QLOO_API_KEY: {'✅ Set' if qloo_key else '❌ Missing'}")
    print(f"QLOO_BASE_URL: {'✅ Set' if qloo_url else '❌ Missing'}")
    
    return bool(perplexity_key and qloo_key)

def test_imports():
    """Test if all required modules can be imported."""
    print("\n🔍 Testing Imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from api.perplexity_service import PerplexityService
        print("✅ PerplexityService imported")
    except ImportError as e:
        print(f"❌ PerplexityService import failed: {e}")
        return False
    
    try:
        from api.qloo_service import QlooService
        print("✅ QlooService imported")
    except ImportError as e:
        print(f"❌ QlooService import failed: {e}")
        return False
    
    try:
        from utils.session_manager import SessionManager
        print("✅ SessionManager imported")
    except ImportError as e:
        print(f"❌ SessionManager import failed: {e}")
        return False
    
    return True

def test_services():
    """Test if services can be initialized."""
    print("\n🔍 Testing Services...")
    
    try:
        from api.perplexity_service import PerplexityService
        from api.qloo_service import QlooService
        
        perplexity = PerplexityService()
        qloo = QlooService()
        
        print("✅ Services initialized")
        
        # Test API key presence
        if perplexity.api_key:
            print("✅ Perplexity API key found")
        else:
            print("❌ Perplexity API key missing")
            
        if qloo.api_key:
            print("✅ Qloo API key found")
        else:
            print("❌ Qloo API key missing")
            
        return bool(perplexity.api_key and qloo.api_key)
        
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("NARRAVOX COMPONENT TEST")
    print("=" * 50)
    
    env_ok = test_environment()
    imports_ok = test_imports()
    services_ok = test_services()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    if env_ok and imports_ok and services_ok:
        print("✅ ALL TESTS PASSED")
        print("🚀 Narravox is ready to run!")
        print("\nTo start the app, run:")
        print("python start_server.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the app.")
        
        if not env_ok:
            print("- Check your .env file and API keys")
        if not imports_ok:
            print("- Install missing dependencies: pip install -r requirements.txt")
        if not services_ok:
            print("- Verify API keys are correct")

if __name__ == "__main__":
    main() 