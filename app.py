#!/usr/bin/env python3
"""
Narravox - Collaborative Story Generator
Production-ready application with enhanced security
"""

import streamlit as st
import os
import re
from dotenv import load_dotenv
import secrets
import hashlib
import time
from typing import Dict, List, Optional, Any

# Security: Load environment variables securely
load_dotenv()

# Security: Import services after environment setup
from api.perplexity_service import PerplexityService
from api.qloo_service import QlooService
from utils.session_manager import SessionManager
from utils.export_utils import ExportUtils

# Security: Add security headers and validation
def add_security_headers():
    """Add security headers to prevent common attacks."""
    # Note: Streamlit doesn't support setting HTTP headers directly
    # Security is handled through input validation and sanitization
    pass

def validate_input(text: str, max_length: int = 1000) -> tuple[bool, str]:
    """
    Validate user input for security and content.
    
    Args:
        text: Input text to validate
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Please enter a story prompt"
    
    if len(text) > max_length:
        return False, f"Input too long. Maximum {max_length} characters allowed."
    
    # Security: Check for potentially malicious content
    dangerous_patterns = [
        r'<script[^>]*>',  # Script tags
        r'javascript:',     # JavaScript protocol
        r'on\w+\s*=',      # Event handlers
        r'data:text/html', # Data URLs
        r'vbscript:',      # VBScript
        r'<iframe[^>]*>',  # Iframe tags
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Input contains potentially unsafe content"
    
    return True, ""

def sanitize_text(text: str) -> str:
    """
    Sanitize text input for safe display.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text

def rate_limit_check(user_id: str, action: str, max_attempts: int = 5, window_seconds: int = 60) -> bool:
    """
    Implement rate limiting for API calls.
    
    Args:
        user_id: Unique identifier for the user
        action: Type of action being rate limited
        max_attempts: Maximum attempts allowed
        window_seconds: Time window in seconds
        
    Returns:
        True if allowed, False if rate limited
    """
    if 'rate_limits' not in st.session_state:
        st.session_state.rate_limits = {}
    
    current_time = time.time()
    key = f"{user_id}_{action}"
    
    if key not in st.session_state.rate_limits:
        st.session_state.rate_limits[key] = []
    
    # Remove old attempts
    st.session_state.rate_limits[key] = [
        attempt_time for attempt_time in st.session_state.rate_limits[key]
        if current_time - attempt_time < window_seconds
    ]
    
    # Check if limit exceeded
    if len(st.session_state.rate_limits[key]) >= max_attempts:
        return False
    
    # Add current attempt
    st.session_state.rate_limits[key].append(current_time)
    return True

def generate_csrf_token() -> str:
    """Generate a CSRF token for form protection."""
    if 'csrf_token' not in st.session_state:
        st.session_state.csrf_token = secrets.token_urlsafe(32)
    return st.session_state.csrf_token

def validate_csrf_token(token: str) -> bool:
    """Validate CSRF token."""
    return token == st.session_state.get('csrf_token', '')

# Security: Enhanced session initialization
def initialize_secure_session():
    """Initialize session with security measures."""
    # Initialize basic session state
    SessionManager.init_session()
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = secrets.token_urlsafe(16)
    
    if 'security_level' not in st.session_state:
        st.session_state.security_level = 'high'
    
    # Initialize rate limiting
    if 'rate_limits' not in st.session_state:
        st.session_state.rate_limits = {}

# Enhanced Swiss Design CSS styling
def apply_swiss_design():
    st.markdown("""
    <style>
    /* Global Styles */
    .main .block-container {
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
        max-width: 1200px;
    }
    
    /* Typography */
    .main-header {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 2.5rem;
        font-weight: 300;
        color: #000000;
        text-align: left;
        margin-bottom: 0.2rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .tagline {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 1rem;
        color: #666666;
        font-weight: 300;
        margin-bottom: 1.5rem;
        line-height: 1.4;
        font-style: italic;
    }
    
    .section-header {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        color: #000000;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        border-bottom: 2px solid #000000;
        padding-bottom: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Story Content */
    .story-content {
        background-color: #FAFAFA;
        padding: 0.4rem;
        border-left: 4px solid #000000;
        margin: 0.3rem 0;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .story-content strong {
        font-weight: 600;
        color: #000000;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
    }
    
    /* Cultural Insights */
    .cultural-insight {
        background-color: #F8F8F8;
        padding: 0.3rem;
        border: 1px solid #E0E0E0;
        margin: 0.2rem 0;
        font-size: 0.9rem;
        color: #555555;
        line-height: 1.5;
        border-radius: 0;
    }
    
    .cultural-insight strong {
        color: #000000;
        font-weight: 500;
    }
    
    /* Interface Elements */
    .turn-counter {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 0.8rem;
        color: #888888;
        text-align: right;
        margin-bottom: 0.2rem;
    }
    
    /* Button Styling - Consistent Swiss Design */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0 !important;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        padding: 0.3rem 0.8rem !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        min-height: 44px !important;
    }
    
    .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-color: #000000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:disabled {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    /* Text Input Styling */
    .stTextArea textarea, .stTextInput input {
        border: 2px solid #E0E0E0 !important;
        border-radius: 0 !important;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.3rem !important;
        background-color: #FFFFFF !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #000000 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Sidebar Styling - Always Visible */
    .css-1d391kg {
        background-color: #F8F8F8 !important;
        border-right: 2px solid #E0E0E0 !important;
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div > div > div {
        background-color: #000000 !important;
    }
    
    /* Metric Styling */
    .css-1wivap2 {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
        font-weight: 400 !important;
    }
    
    /* Form Accessibility */
    .stTextArea textarea, .stTextInput input {
        autocomplete: "off";
    }
    
    /* Ensure proper label associations */
    .stTextArea label, .stTextInput label {
        display: block;
        margin-bottom: 0.3rem;
        font-weight: 500;
        color: #000000;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
    }
    
    /* Form field IDs and names */
    .stTextArea textarea, .stTextInput input {
        id: attr(data-testid);
        name: attr(data-testid);
    }
    
    /* Autocomplete attributes */
    .stTextArea textarea[data-testid="story_prompt_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="music_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="film_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="book_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="travel_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="brand_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextInput input[data-testid="other_prefs_input"] {
        autocomplete: "off";
    }
    
    .stTextArea textarea[data-testid="story_continuation_input"] {
        autocomplete: "off";
    }
    
    /* Footer Styling - Swiss Design */
    .element-container .stMarkdown {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
    }
    
    /* Footer links styling */
    .element-container .stMarkdown a {
        color: #000000;
        text-decoration: none;
        font-weight: 400;
        transition: color 0.2s ease;
    }
    
    .element-container .stMarkdown a:hover {
        color: #666666;
        text-decoration: underline;
    }
    
    /* Footer captions */
    .element-container .stCaption {
        color: #888888;
        font-size: 0.8rem;
        font-weight: 300;
    }
    
    /* Footer column spacing - more aggressive */
    .element-container .row-widget.stHorizontal {
        gap: 0.1rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Footer content spacing */
    .element-container .stMarkdown {
        margin-bottom: 0.05rem !important;
        margin-top: 0.05rem !important;
    }
    
    /* Footer container spacing */
    .element-container {
        margin-bottom: 0.2rem !important;
    }
    
    /* Specific footer column targeting */
    .element-container .stHorizontal > div {
        padding: 0 0.2rem !important;
    }
    
    /* Loading States */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        margin: 1rem 0;
    }
    
    .loading-text {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 0.9rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 0 !important;
        border-left: 4px solid !important;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #000000 !important;
        border-bottom: 1px solid #E0E0E0 !important;
    }
    
    /* Checkbox Styling */
    .stCheckbox > label {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif !important;
        font-size: 0.9rem !important;
        color: #333333 !important;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth Transitions */
    * {
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_services():
    """Initialize API services."""
    try:
        if 'perplexity_service' not in st.session_state:
            st.session_state.perplexity_service = PerplexityService()
            st.session_state.qloo_service = QlooService()
            
            # Test API connectivity
            if st.session_state.perplexity_service.api_key:
                st.session_state.api_status = "APIs initialized"
            else:
                st.session_state.api_status = "API keys missing"
                
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.write("Please check your API keys in the environment variables.")
        st.session_state.api_status = "Service initialization failed"

def main():
    # Apply Swiss Design styling
    apply_swiss_design()
    
    # Initialize session and services with error handling
    try:
        initialize_secure_session()
        initialize_services()
    except Exception as e:
        st.error(f"Failed to initialize application: {str(e)}")
        st.stop()
    
    # Main header - using div instead of h1 to avoid anchor links
    st.markdown('''
    <div class="main-header">Narravox</div>
    <div class="tagline">Vocalize Worlds Woven from Cultural Affinities</div>
    ''', unsafe_allow_html=True)
    
    # Enhanced Sidebar for controls and information - Always visible
    with st.sidebar:
        st.markdown("### SESSION OVERVIEW")
        stats = SessionManager.get_session_stats()
        
        # API Status
        if hasattr(st.session_state, 'api_status'):
            st.info(st.session_state.api_status)
        
        # Progress indicator
        progress = stats['turns_completed'] / stats['max_turns']
        st.progress(progress)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("TURN", f"{stats['turns_completed']}")
        with col2:
            st.metric("MAX", f"{stats['max_turns']}")
        
        st.metric("STORY LENGTH", f"{stats['story_length']:,} chars")
        
        st.markdown("---")
        
        # Enhanced action buttons
        st.markdown("### ACTIONS")
        
        if st.button("NEW STORY", key="new_story_button", use_container_width=True):
            SessionManager.reset_session()
            st.rerun()
        
        if st.session_state.story_started:
            if st.button("EXPORT STORY", key="export_story_button", use_container_width=True):
                show_export_options()
        
        st.markdown("---")
        
        # Demo mode with better styling
        st.markdown("### DEMO MODE")
        demo_enabled = st.checkbox("Enable Demo Examples")
        
        if demo_enabled:
            st.session_state.demo_mode = True
            show_demo_examples()
        else:
            st.session_state.demo_mode = False
            
        if st.session_state.cultural_context:
            st.markdown("---")
            st.markdown("### CULTURAL STATUS")
            st.success("Cultural enrichment active")
            context_preview = st.session_state.cultural_context[:100] + "..." if len(st.session_state.cultural_context) > 100 else st.session_state.cultural_context
            st.caption(context_preview)
    
    # Error display
    if st.session_state.last_error:
        st.error(f"Error: {st.session_state.last_error['message']}")
        if st.button("Clear Error", key="clear_error_button"):
            SessionManager.clear_error()
            st.rerun()
    
    # Main content area
    if not st.session_state.story_started:
        show_story_initiation()
    else:
        show_story_interface()
    
    # Add professional footer
    show_footer()

def show_story_initiation():
    """Display enhanced story initiation interface."""
    st.markdown('<div class="section-header">Story Creation</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div style="background-color: #F8F8F8; padding: 0.8rem; border-left: 4px solid #000000; margin: 0.8rem 0;">
        <p style="font-size: 1rem; line-height: 1.5; margin: 0; color: #333333;">
            Create narratives enriched with cultural intelligence using Qloo's Insights API. Stories are enhanced with 
            cross-domain affinities discovered through Taste Analysis, connecting music, film, travel, and lifestyle elements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Taste profile builder with enhanced styling
    with st.expander("BUILD CULTURAL TASTE PROFILE", expanded=False):
        show_taste_profile_builder()
        
        # Show if taste profile is active
        if hasattr(st.session_state, 'user_preferences') and st.session_state.user_preferences:
            st.success("Cultural profile active - will enhance your story generation")
            user_prefs = st.session_state.user_preferences
            pref_list = []
            for category, items in user_prefs.items():
                if items:
                    pref_list.extend(items[:1])  # Show one from each category
            if pref_list:
                st.info(f"Preferences: {', '.join(pref_list[:5])}")
    
    # Enhanced story prompt input
    st.markdown("### Story Prompt")
    
    # Handle demo prompt if set
    default_prompt = ""
    if hasattr(st.session_state, 'demo_prompt'):
        default_prompt = st.session_state.demo_prompt
        # Clear the demo prompt after using it
        del st.session_state.demo_prompt
    
    story_prompt = st.text_area(
        "Describe the story you want to create:",
        value=default_prompt,
        key="story_prompt_input",
        placeholder="Enter your story concept here. Include genres, themes, cultural elements, or specific interests. For example: 'A cyberpunk thriller with jazz influences set in a futuristic Tokyo where vintage vinyl records hold digital secrets.'",
        height=80,
        help="The more cultural elements you include, the richer your story will become through Qloo's AI enrichment.",
        on_change=None,
        label_visibility="visible"
    )
    
    # Enhanced action area - buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("BEGIN STORY", key="begin_story_button", disabled=not story_prompt.strip(), use_container_width=True):
            if not story_prompt.strip():
                st.error("Please enter a story prompt")
                return
            try:
                with st.spinner("Creating your story..."):
                    create_story_opener(story_prompt)
            except Exception as e:
                st.error(f"Failed to create story: {str(e)}")
    
    with col2:
        if st.button("SURPRISE ME", key="surprise_me_button", use_container_width=True):
            try:
                with st.spinner("Generating surprise story..."):
                    surprise_continuation()
            except Exception as e:
                st.error(f"Failed to generate surprise: {str(e)}")
    
    # Quick examples for inspiration
    st.markdown("### Need Inspiration?")
    
    # Inspiration buttons in a clean grid
    col1, col2 = st.columns(2)
    with col1:
        if st.button("CYBERPUNK + JAZZ", key="cyberpunk_jazz_button", use_container_width=True):
            st.session_state.demo_prompt = "A cyberpunk thriller with jazz influences set in a futuristic Tokyo where vintage vinyl records hold digital secrets."
            st.rerun()
    
    with col2:
        if st.button("ROMANCE + VINYL", key="romance_vinyl_button", use_container_width=True):
            st.session_state.demo_prompt = "A romantic story about two people who fall in love through their shared passion for vinyl records and indie music."
            st.rerun()
    
    # Handle temp prompt
    if hasattr(st.session_state, 'temp_prompt') and st.session_state.temp_prompt:
        create_story_opener(st.session_state.temp_prompt)
        del st.session_state.temp_prompt

def show_taste_profile_builder():
    """Display enhanced taste profile builder interface."""
    st.markdown("### Cultural Preferences")
    
    # Input fields for different categories
    col1, col2 = st.columns(2)
    
    with col1:
        music_prefs = st.text_input("Music Genres", key="music_prefs_input", placeholder="jazz, classical, electronic", on_change=None, label_visibility="visible")
        film_prefs = st.text_input("Film Genres", key="film_prefs_input", placeholder="sci-fi, noir, arthouse", on_change=None, label_visibility="visible")
        book_prefs = st.text_input("Book Genres", key="book_prefs_input", placeholder="mystery, fantasy, literary", on_change=None, label_visibility="visible")
    
    with col2:
        travel_prefs = st.text_input("Travel Interests", key="travel_prefs_input", placeholder="japan, vintage, urban", on_change=None, label_visibility="visible")
        brand_prefs = st.text_input("Lifestyle Brands", key="brand_prefs_input", placeholder="minimalist, sustainable, luxury", on_change=None, label_visibility="visible")
        other_prefs = st.text_input("Other Interests", key="other_prefs_input", placeholder="meditation, badminton", on_change=None, label_visibility="visible")
    
    # Build profile button
    if st.button("BUILD PROFILE", key="build_profile_button", use_container_width=True):
        try:
            # Security: Rate limiting for profile building
            user_id = st.session_state.get('session_id', 'anonymous')
            if not rate_limit_check(user_id, 'profile_building', max_attempts=3, window_seconds=120):
                st.error("Rate limit exceeded. Please wait before building another profile.")
                return
            
            with st.spinner("Building your cultural profile..."):
                # Check if Qloo service is available
                if not hasattr(st.session_state, 'qloo_service'):
                    st.error("Cultural service not available. Please refresh the page.")
                    return
                
                # Security: Validate and sanitize preferences
                def sanitize_preferences(pref_list):
                    sanitized = []
                    for pref in pref_list:
                        # Validate each preference
                        is_valid, _ = validate_input(pref, max_length=50)
                        if is_valid:
                            sanitized.append(sanitize_text(pref.strip()))
                    return sanitized
                
                # Collect and sanitize preferences
                preferences = {
                    "music": sanitize_preferences([x.strip() for x in music_prefs.split(",") if x.strip()]) if music_prefs else [],
                    "film": sanitize_preferences([x.strip() for x in film_prefs.split(",") if x.strip()]) if film_prefs else [],
                    "books": sanitize_preferences([x.strip() for x in book_prefs.split(",") if x.strip()]) if book_prefs else [],
                    "travel": sanitize_preferences([x.strip() for x in travel_prefs.split(",") if x.strip()]) if travel_prefs else [],
                    "brands": sanitize_preferences([x.strip() for x in brand_prefs.split(",") if x.strip()]) if brand_prefs else [],
                    "other": sanitize_preferences([x.strip() for x in other_prefs.split(",") if x.strip()]) if other_prefs else []
                }
                
                # Generate profile
                result = st.session_state.qloo_service.get_taste_profile_suggestions(preferences)
                
                if result["success"]:
                    # Check if this was from Qloo API or fallback
                    if result.get("source") == "qloo_api":
                        st.success("Qloo Insights API profile created successfully")
                        st.info("Cultural affinities enriched through Taste Analysis")
                    else:
                        st.success("Profile created from your preferences")
                        st.info("Using enhanced cultural analysis for your story suggestions")
                    
                    # Store both preferences and suggestions
                    st.session_state.user_preferences = preferences
                    if "suggestions" in result:
                        st.session_state.taste_suggestions = result["suggestions"]
                    
                    # Display suggestions
                    if st.session_state.taste_suggestions:
                        st.markdown("### Story Suggestions")
                        for i, suggestion in enumerate(st.session_state.taste_suggestions[:3]):
                            st.markdown(f"• {suggestion}")
                    
                    st.rerun()
                else:
                    st.warning(f"Could not generate profile: {result.get('error', 'Unknown error')}")
                    
        except Exception as e:
            st.error(f"Profile generation failed: {str(e)}")
            st.write("Please check your internet connection and try again.")

def create_story_opener(prompt: str):
    """Create the initial story using Perplexity and Qloo with security measures."""
    
    # Security: Input validation
    is_valid, error_msg = validate_input(prompt, max_length=500)
    if not is_valid:
        st.error(f"Input validation failed: {error_msg}")
        return
    
    # Security: Rate limiting
    user_id = st.session_state.get('session_id', 'anonymous')
    if not rate_limit_check(user_id, 'story_generation', max_attempts=3, window_seconds=60):
        st.error("Rate limit exceeded. Please wait before generating another story.")
        return
    
    # Security: Sanitize input
    sanitized_prompt = sanitize_text(prompt)
    
    try:
        # Check if services are initialized
        if not hasattr(st.session_state, 'qloo_service') or not hasattr(st.session_state, 'perplexity_service'):
            st.error("Services not initialized. Please refresh the page.")
            return
        
        # Get cultural context from Qloo - enhanced with taste profile
        cultural_context = ""
        try:
            # First, try to use taste profile if available
            if hasattr(st.session_state, 'user_preferences') and st.session_state.user_preferences:
                # Use actual user preferences to enhance the prompt
                user_prefs = st.session_state.user_preferences
                pref_list = []
                for category, items in user_prefs.items():
                    if items:
                        pref_list.extend(items[:2])  # Take top 2 from each category
                
                if pref_list:
                    # Ensure we include preferences from all categories, prioritizing non-empty ones
                    all_prefs = []
                    for category, items in user_prefs.items():
                        if items:
                            all_prefs.extend(items)
                    
                    # Create enhanced prompt with cultural preferences
                    enhanced_prompt = f"{sanitized_prompt} (Cultural preferences: {', '.join(all_prefs[:8])})"
                    
                    # Use the enhanced prompt for cultural context
                    cultural_context = st.session_state.qloo_service.create_cultural_context(enhanced_prompt)
                    
                    # If no relevant cultural context found, create one based on user preferences
                    if not cultural_context:
                        cultural_context = _create_cultural_context_from_preferences(all_prefs)
                    
                    # Also create cultural context directly from user preferences for better integration
                    preference_context = _create_cultural_context_from_preferences(all_prefs)
                    if preference_context:
                        cultural_context = f"{cultural_context}; {preference_context}" if cultural_context else preference_context
                    
                    SessionManager.add_cultural_explanation(
                        "Taste Profile Integration",
                        f"Enhanced story with your cultural preferences: {', '.join(all_prefs[:8])}"
                    )
                else:
                    # Fallback to extracting from prompt only
                    cultural_context = st.session_state.qloo_service.create_cultural_context(sanitized_prompt)
            else:
                # Fallback to extracting from prompt only
                cultural_context = st.session_state.qloo_service.create_cultural_context(sanitized_prompt)
            
            if cultural_context:
                SessionManager.set_cultural_context(cultural_context)
                SessionManager.add_cultural_explanation(
                    "Story Cultural Elements",
                    f"Qloo Insights API identified these cultural affinities through Taste Analysis: {cultural_context}"
                )
        except Exception as e:
            st.warning(f"Cultural context unavailable: {str(e)}")
        
        # Generate story opener with Perplexity
        result = st.session_state.perplexity_service.generate_story_opener(sanitized_prompt, cultural_context)
        
        if result["success"]:
            # Security: Sanitize AI response before storing
            sanitized_content = sanitize_text(result["content"])
            
            # Add entries to story
            SessionManager.add_story_entry(sanitized_prompt, "user")
            SessionManager.add_story_entry(sanitized_content, "ai")
            SessionManager.increment_turn()
            st.session_state.story_started = True
            st.success("Story created successfully!")
            st.rerun()
        else:
            st.error(f"Story generation failed: {result['error']}")
            SessionManager.set_error(result["error"])
            
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.write("Please check your internet connection and API keys.")

def _create_cultural_context_from_preferences(preferences: List[str]) -> str:
    """Create cultural context from user preferences when Qloo API doesn't return relevant results."""
    if not preferences:
        return ""
    
    # Map preferences to cultural domains
    cultural_mapping = {
        "japan": "travel: Japanese culture, Zen aesthetics, Traditional craftsmanship",
        "jazz": "music: Jazz improvisation, Blues influences, Swing rhythms",
        "sci-fi": "film: Science fiction, Futuristic themes, Technological innovation",
        "mystery": "books: Detective fiction, Suspense narrative, Crime investigation",
        "minimalist": "lifestyle: Minimalist design, Clean aesthetics, Functional beauty",
        "meditation": "lifestyle: Mindfulness practices, Spiritual wellness, Inner peace",
        "rock": "music: Rock energy, Electric guitars, Powerful rhythms",
        "classical": "music: Orchestral arrangements, Classical composition, Timeless elegance",
        "hip-hop": "music: Urban beats, Rap culture, Street art influence",
        "electronic": "music: Digital soundscapes, Synthesizer textures, Modern production",
        "fantasy": "books: Magical worlds, Epic quests, Mythical creatures",
        "thriller": "film: Suspenseful tension, Psychological drama, Intense pacing",
        "romance": "books: Emotional depth, Love stories, Heartfelt connections",
        "comedy": "film: Humorous situations, Light-hearted storytelling, Witty dialogue",
        "drama": "film: Character development, Emotional intensity, Realistic storytelling",
        "travel": "lifestyle: Cultural exploration, Geographic diversity, Adventure themes",
        "adventure": "lifestyle: Exploration spirit, Risk-taking, Discovery narratives",
        "historical": "books: Period settings, Historical accuracy, Time-travel themes",
        "contemporary": "lifestyle: Modern settings, Current social issues, Present-day relevance",
        "urban": "lifestyle: City life, Metropolitan culture, Street-level stories",
        "rural": "lifestyle: Countryside settings, Natural environments, Community focus",
        "futuristic": "film: Advanced technology, Sci-fi aesthetics, Tomorrow's world",
        "vintage": "lifestyle: Retro aesthetics, Nostalgic themes, Classic style",
        "modern": "lifestyle: Contemporary design, Current trends, Present-day relevance"
    }
    
    relevant_contexts = []
    for pref in preferences[:5]:  # Limit to 5 preferences
        pref_lower = pref.lower()
        for key, context in cultural_mapping.items():
            if key in pref_lower:
                relevant_contexts.append(context)
                break
    
    if relevant_contexts:
        return "; ".join(relevant_contexts)
    else:
        # Generic cultural context based on preferences
        return f"cultural: {', '.join(preferences[:3])} influences"

def show_story_interface():
    """Display the enhanced main story interface."""
    # Enhanced turn counter with progress
    stats = SessionManager.get_session_stats()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f'<div class="turn-counter">Turn {stats["turns_completed"]} of {stats["max_turns"]}</div>', unsafe_allow_html=True)
    with col2:
        if stats["turns_completed"] > 5:
            st.markdown('<div class="turn-counter">Extended</div>', unsafe_allow_html=True)
    with col3:
        if stats["has_cultural_context"]:
            st.markdown('<div class="turn-counter">Enriched</div>', unsafe_allow_html=True)
    
    # Display current story with enhanced formatting
    st.markdown('<div class="section-header">Narrative Thread</div>', unsafe_allow_html=True)
    
    # Show story history with alternating styling
    for i, entry in enumerate(st.session_state.story_history):
        if entry['type'] in ['user', 'ai']:
            speaker = "You" if entry['type'] == 'user' else "Narravox AI"
            speaker_color = "#666666" if entry['type'] == 'user' else "#000000"
            
            story_style = "story-content"
            if entry['type'] == 'user':
                story_style += '" style="border-left-color: #666666; background-color: #F5F5F5;'
            
            st.markdown(f'''
            <div class="{story_style}">
                <strong style="color: {speaker_color}">{speaker}:</strong><br/>
                {entry["content"]}
            </div>
            ''', unsafe_allow_html=True)
    
    # Enhanced cultural insights panel
    if st.session_state.cultural_explanations:
        with st.expander("CULTURAL INTELLIGENCE INSIGHTS", expanded=True):
            st.markdown("Qloo Insights API has discovered these cultural connections through Taste Analysis:")
            for key, explanation in st.session_state.cultural_explanations.items():
                st.markdown(f'<div class="cultural-insight"><strong>{key}:</strong> {explanation}</div>', 
                           unsafe_allow_html=True)
    
    # Story completion check
    if SessionManager.is_story_complete():
        st.success("Story Complete. Maximum turns reached.")
        show_export_options()
        return
    
    # Enhanced branching options
    if st.session_state.branching_options:
        show_branching_options()
    
    # Enhanced continuation interface
    st.markdown('<div class="section-header">Story Continuation</div>', unsafe_allow_html=True)
    
    # Input area with better layout
    user_input = st.text_area(
        "Continue your narrative:",
        key="story_continuation_input",
        placeholder="What happens next in your story? Describe actions, dialogue, or new elements to explore...",
        height=80,
        help="Add details, dialogue, or new plot elements to continue the story.",
        on_change=None,
        label_visibility="visible"
    )
    
    # Action buttons with loading states
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("CONTINUE STORY", key="continue_story_button", disabled=not user_input.strip(), use_container_width=True):
            try:
                with st.spinner("Continuing your story..."):
                    continue_story(user_input)
            except Exception as e:
                st.error(f"Failed to continue story: {str(e)}")
    
    with col2:
        if st.button("GENERATE OPTIONS", key="generate_options_button", use_container_width=True):
            try:
                with st.spinner("Generating story options..."):
                    generate_branching_options()
            except Exception as e:
                st.error(f"Failed to generate options: {str(e)}")
    
    with col3:
        if st.button("ENHANCE CULTURE", key="enhance_culture_button", use_container_width=True):
            try:
                with st.spinner("Enhancing with cultural context..."):
                    enhance_with_culture()
            except Exception as e:
                st.error(f"Failed to enhance culture: {str(e)}")

def show_branching_options():
    """Display branching narrative options."""
    if not st.session_state.branching_options:
        return
    
    st.markdown('<div class="section-header">Story Branching Options</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F8F8F8; padding: 0.8rem; border-left: 4px solid #000000; margin: 0.8rem 0;">
        <p style="font-size: 0.9rem; line-height: 1.5; margin: 0; color: #666666;">
            Choose a direction for your story to continue:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display options in a clean grid
    for i, option in enumerate(st.session_state.branching_options):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f'<div class="story-content">{option}</div>', unsafe_allow_html=True)
        with col2:
            if st.button(f"CHOOSE {i+1}", key=f"branch_{i}", use_container_width=True):
                try:
                    with st.spinner("Continuing with your choice..."):
                        continue_story(option, is_branching_choice=True)
                except Exception as e:
                    st.error(f"Failed to continue with choice: {str(e)}")

def continue_story(user_input: str, is_branching_choice: bool = False):
    """Continue the story with user input and security measures."""
    
    # Security: Input validation
    is_valid, error_msg = validate_input(user_input, max_length=500)
    if not is_valid:
        st.error(f"Input validation failed: {error_msg}")
        return
    
    # Security: Rate limiting
    user_id = st.session_state.get('session_id', 'anonymous')
    if not rate_limit_check(user_id, 'story_continuation', max_attempts=5, window_seconds=30):
        st.error("Rate limit exceeded. Please wait before continuing the story.")
        return
    
    # Security: Sanitize input
    sanitized_input = sanitize_text(user_input)
    
    try:
        # Check if services are available
        if not hasattr(st.session_state, 'perplexity_service'):
            st.error("❌ Perplexity service not available. Please refresh the page.")
            return
        
        # Add user input to history (sanitized)
        if not is_branching_choice:
            SessionManager.add_story_entry(sanitized_input, "user")
        
        # Get AI continuation
        result = st.session_state.perplexity_service.continue_story(
            st.session_state.story_history,
            sanitized_input,
            st.session_state.cultural_context
        )
        
        if result["success"]:
            # Security: Sanitize AI response before storing
            sanitized_content = sanitize_text(result["content"])
            
            SessionManager.add_story_entry(sanitized_content, "ai")
            SessionManager.increment_turn()
            
            # Clear branching options and input
            st.session_state.branching_options = []
            
            # Enhance with new cultural context if entities found
            try:
                enhance_story_with_new_culture(sanitized_input)
            except Exception as e:
                st.warning(f"Cultural enhancement failed: {str(e)}")
            
            st.success("Story continued successfully!")
            st.rerun()
        else:
            st.error(f"Story continuation failed: {result['error']}")
            SessionManager.set_error(result["error"])
            
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.write("Please check your internet connection and try again.")

def generate_branching_options():
    """Generate branching narrative options."""
    try:
        # Check if services are available
        if not hasattr(st.session_state, 'perplexity_service'):
            st.error("❌ Perplexity service not available. Please refresh the page.")
            return
        
        current_story = SessionManager.get_story_text()
        
        result = st.session_state.perplexity_service.generate_branching_options(
            current_story,
            st.session_state.cultural_context
        )
        
        if result["success"]:
            st.session_state.branching_options = result["options"]
            st.success("Story options generated!")
            st.rerun()
        else:
            st.error(f"Failed to generate options: {result['error']}")
            SessionManager.set_error(result["error"])
            
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.write("Please check your internet connection and try again.")

def enhance_with_culture():
    """Enhance story with additional cultural context."""
    try:
        # Check if services are available
        if not hasattr(st.session_state, 'qloo_service'):
            st.error("❌ Qloo service not available. Please refresh the page.")
            return
        
        # Get new entities from recent story content
        recent_content = ""
        if st.session_state.story_history:
            recent_entries = st.session_state.story_history[-2:]  # Last 2 entries
            recent_content = " ".join([entry["content"] for entry in recent_entries])
        
        new_context = st.session_state.qloo_service.create_cultural_context(recent_content)
        
        if new_context and new_context != st.session_state.cultural_context:
            # Update cultural context
            current_context = st.session_state.cultural_context
            enhanced_context = f"{current_context}; {new_context}" if current_context else new_context
            SessionManager.set_cultural_context(enhanced_context)
            
            # Add explanation
            SessionManager.add_cultural_explanation(
                f"Cultural Discovery (Turn {st.session_state.turn_count})",
                f"New cultural connections found: {new_context}"
            )
            
            st.success("✅ New cultural connections discovered!")
            st.rerun()
        else:
            st.info("ℹ️ No new cultural connections found at this time.")
            
    except Exception as e:
        st.error(f"❌ Cultural enhancement failed: {str(e)}")
        st.write("Please check your internet connection and try again.")

def enhance_story_with_new_culture(user_input: str):
    """Automatically enhance story with cultural context from new user input."""
    entities = st.session_state.qloo_service.extract_entities_from_text(user_input)
    
    if entities:
        new_context = st.session_state.qloo_service.create_cultural_context(user_input)
        
        if new_context:
            current_context = st.session_state.cultural_context
            if new_context not in current_context:
                enhanced_context = f"{current_context}; {new_context}" if current_context else new_context
                SessionManager.set_cultural_context(enhanced_context)
                
                # Add subtle explanation
                SessionManager.add_cultural_explanation(
                    f"Auto-Discovery (Turn {st.session_state.turn_count})",
                    f"Cultural elements from your input: {new_context}"
                )

def show_export_options():
    """Display export and sharing options."""
    st.markdown('<div class="section-header">Export & Share</div>', unsafe_allow_html=True)
    
    story_data = SessionManager.export_story_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download Text", key="download_text_button"):
            text_content = ExportUtils.create_story_text(story_data)
            st.download_button(
                label="Download Story.txt",
                data=text_content,
                file_name=f"narravox_story_{story_data['session_id'][:8]}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("Download PDF", key="download_pdf_button"):
            try:
                pdf_path = ExportUtils.create_story_pdf(story_data)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Story.pdf",
                        data=pdf_file.read(),
                        file_name=f"narravox_story_{story_data['session_id'][:8]}.pdf",
                        mime="application/pdf"
                    )
                # Cleanup is handled by create_story_pdf if it uses a temporary file
            except Exception as e:
                st.error(f"PDF generation failed: {str(e)}")
    
    with col3:
        if st.button("Copy Share Link", key="copy_share_link_button"):
            share_link = ExportUtils.create_shareable_link(story_data['session_id'])
            st.code(share_link)
            st.info("Link copied! (Feature will be available after deployment)")

def surprise_continuation():
    """Generate a surprise story with random cultural elements."""
    surprise_prompts = [
        "A cyberpunk detective in Neo-Tokyo discovers jazz music holds the key to solving crimes",
        "A vintage vinyl collector in Paris finds love through shared passion for indie music",
        "A classical musician in Vienna discovers hip-hop culture changes their perspective on tradition",
        "A street artist in Berlin combines graffiti with ancient calligraphy techniques",
        "A tea ceremony master in Kyoto incorporates modern electronic music into traditional rituals",
        "A fashion designer in Milan finds inspiration in ancient tribal patterns and modern streetwear",
        "A chef in New Orleans blends Creole traditions with molecular gastronomy",
        "A photographer in Morocco captures the intersection of traditional markets and digital commerce"
    ]
    
    import random
    surprise_prompt = random.choice(surprise_prompts)
    create_story_opener(surprise_prompt)

def show_demo_examples():
    """Show demo examples for quick testing."""
    st.markdown("**Quick Start Examples:**")
    
    examples = [
        ("CYBERPUNK + JAZZ", "A cyberpunk thriller with jazz influences in Neo-Tokyo"),
        ("ROMANCE + VINYL", "A romantic comedy involving vintage vinyl records and food trucks"),
        ("FANTASY + HIP-HOP", "A fantasy adventure combining Norse mythology with modern hip-hop culture"),
        ("SCI-FI + CLASSICAL", "A space opera where classical music holds the key to interstellar communication")
    ]
    
    for title, example in examples:
        if st.button(title, key=f"demo_{title}", use_container_width=True):
            # Reset session and start with example
            SessionManager.reset_session()
            create_story_opener(example)

def show_footer():
    """Display a professional footer with copyright and social links."""
    # Add spacing
    st.markdown("---")
    
    # Compact footer layout
    st.markdown("**NARRAVOX** | **Connect** | **Project**")
    st.markdown("Collaborative Story Generator | [Twitter](https://x.com/TanayVasishtha) [GitHub](https://github.com/tanayvasishtha/Narravox) | Qloo LLM Hackathon 2025")
    st.caption("Powered by Perplexity Sonar & Qloo Insights API (Taste Analysis) | | Built with Streamlit & Python")
    
    # Copyright section
    st.markdown("---")
    st.markdown("© 2025 Narravox. All rights reserved. | @TanayVasishtha | Made with ❤️ for the Qloo LLM Hackathon", help="Footer links and copyright information")

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("PERPLEXITY_API_KEY"):
        st.error("Please set PERPLEXITY_API_KEY environment variable")
        st.stop()
    
    if not os.getenv("QLOO_API_KEY"):
        st.error("Please set QLOO_API_KEY environment variable")
        st.stop()
    
    main() 