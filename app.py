import streamlit as st
import os
from typing import Dict, List
import json

# Import custom modules
from api.perplexity_service import PerplexityService
from api.qloo_service import QlooService
from utils.session_manager import SessionManager
from utils.export_utils import ExportUtils

# Enhanced Swiss Design CSS styling
def apply_swiss_design():
    st.markdown("""
    <style>
    /* Global Styles */
    .main .block-container {
        padding-top: 1.4rem;
        padding-bottom: 1.4rem;
        max-width: 1200px;
    }
    
    /* Typography */
    .main-header {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 3rem;
        font-weight: 300;
        color: #000000;
        text-align: left;
        margin-bottom: 0.3rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .tagline {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 1.1rem;
        color: #666666;
        font-weight: 300;
        margin-bottom: 2.8rem;
        line-height: 1.4;
        font-style: italic;
    }
    
    .section-header {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 1.4rem;
        font-weight: 400;
        color: #000000;
        margin-top: 2.1rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #000000;
        padding-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Story Content */
    .story-content {
        background-color: #FAFAFA;
        padding: 1.4rem;
        border-left: 4px solid #000000;
        margin: 1rem 0;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        line-height: 1.7;
        font-size: 1.05rem;
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
        padding: 1rem;
        border: 1px solid #E0E0E0;
        margin: 0.7rem 0;
        font-size: 0.95rem;
        color: #555555;
        line-height: 1.6;
        border-radius: 0;
    }
    
    .cultural-insight strong {
        color: #000000;
        font-weight: 500;
    }
    
    /* Interface Elements */
    .turn-counter {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 0.85rem;
        color: #888888;
        text-align: right;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-weight: 400;
        letter-spacing: 0.05em;
        padding: 0.5rem 1.4rem;
        text-transform: uppercase;
        font-size: 0.9rem;
        border-radius: 0;
    }
    
    .stButton > button:hover {
        background-color: #333333;
        color: #FFFFFF;
    }
    
    .stButton > button:active {
        background-color: #000000;
    }
    
    /* Text Areas and Inputs */
    .stTextArea textarea {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        border-radius: 0;
        border: 2px solid #E0E0E0;
        padding: 0.7rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #000000;
        box-shadow: 0 0 0 1px #000000;
    }
    
    .stTextInput input {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        border-radius: 0;
        border: 1px solid #CCCCCC;
        padding: 0.5rem;
    }
    
    .stTextInput input:focus {
        border-color: #000000;
        box-shadow: 0 0 0 1px #000000;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #F8F8F8;
    }
    
    .css-1d391kg .stMarkdown {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-weight: 500;
        color: #000000;
        font-size: 1.1rem;
    }
    
    /* Progress and Status */
    .stProgress .st-bo {
        background-color: #000000;
    }
    
    .stSuccess {
        background-color: #F0F8F0;
        color: #2D5A2D;
        border-left: 4px solid #4CAF50;
    }
    
    .stError {
        background-color: #FFF5F5;
        color: #C53030;
        border-left: 4px solid #E53E3E;
    }
    
    .stInfo {
        background-color: #F0F8FF;
        color: #1A365D;
        border-left: 4px solid #3182CE;
    }
    
    /* Custom Grid Layouts */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 2rem;
        text-align: center;
    }
    
    .feature-card h3 {
        font-family: 'Helvetica Neue', 'Helvetica', Arial, sans-serif;
        font-weight: 500;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        color: #000000;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .story-content {
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1.5rem;
            font-size: 0.85rem;
        }
    }
    
    /* Hide Streamlit Branding and Links */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove header anchor links */
    .main-header a {
        text-decoration: none !important;
        color: #000000 !important;
        pointer-events: none;
    }
    
    .main-header a:hover {
        text-decoration: none !important;
        color: #000000 !important;
    }
    
    /* Hide all header link icons */
    .element-container .stMarkdown h1 a,
    .element-container .stMarkdown h2 a,
    .element-container .stMarkdown h3 a {
        display: none !important;
    }
    
    /* Remove hover effects on headers */
    .element-container .stMarkdown h1:hover::after,
    .element-container .stMarkdown h2:hover::after,
    .element-container .stMarkdown h3:hover::after {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_services():
    """Initialize API services."""
    try:
        if 'perplexity_service' not in st.session_state:
            st.session_state.perplexity_service = PerplexityService()
            st.session_state.qloo_service = QlooService()
            # st.success("✅ API services initialized successfully!")
    except Exception as e:
        st.error(f"❌ Failed to initialize services: {str(e)}")
        st.write("Please check your API keys in the environment variables.")

def main():
    # Apply Swiss Design styling
    apply_swiss_design()
    
    # Initialize session and services
    SessionManager.init_session()
    initialize_services()
    
    # Main header - using div instead of h1 to avoid anchor links
    st.markdown('''
    <div class="main-header">Narravox</div>
    <div class="tagline">Vocalize Worlds Woven from Cultural Affinities</div>
    ''', unsafe_allow_html=True)
    
    # Enhanced Sidebar for controls and information
    with st.sidebar:
        st.markdown("### SESSION OVERVIEW")
        stats = SessionManager.get_session_stats()
        
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
        
        if st.button("NEW STORY", use_container_width=True):
            SessionManager.reset_session()
            st.rerun()
        
        if st.session_state.story_started:
            if st.button("EXPORT STORY", use_container_width=True):
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
        if st.button("Clear Error"):
            SessionManager.clear_error()
            st.rerun()
    
    # Main content area
    if not st.session_state.story_started:
        show_story_initiation()
    else:
        show_story_interface()

def show_story_initiation():
    """Display enhanced story initiation interface."""
    st.markdown('<div class="section-header">Story Creation</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div style="background-color: #F8F8F8; padding: 1.4rem; border-left: 4px solid #000000; margin: 1.4rem 0;">
        <p style="font-size: 1.1rem; line-height: 1.6; margin: 0; color: #333333;">
            Create narratives enriched with cultural intelligence. Stories are enhanced with 
            cross-domain affinities connecting music, film, travel, and lifestyle elements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Taste profile builder with enhanced styling
    with st.expander("BUILD CULTURAL TASTE PROFILE", expanded=False):
        show_taste_profile_builder()
    
    # Enhanced story prompt input
    st.markdown("### Story Prompt")
    story_prompt = st.text_area(
        "Describe the story you want to create:",
        placeholder="Enter your story concept here. Include genres, themes, cultural elements, or specific interests. For example: 'A cyberpunk thriller with jazz influences set in a futuristic Tokyo where vintage vinyl records hold digital secrets.'",
        height=120,
        help="The more cultural elements you include, the richer your story will become through Qloo's AI enrichment."
    )
    
    # Enhanced action area
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button("BEGIN STORY", disabled=not story_prompt.strip(), use_container_width=True):
            try:
                st.write("Button clicked! Starting story creation...")
                create_story_opener(story_prompt)
            except Exception as e:
                st.error(f"Error creating story: {str(e)}")
                st.write("Please check your API keys and try again.")
    
    # Quick examples for inspiration
    if not story_prompt:
        st.markdown("### Need Inspiration?")
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            if st.button("CYBERPUNK + JAZZ", use_container_width=True):
                st.session_state.temp_prompt = "A cyberpunk thriller with jazz influences in Neo-Tokyo"
                st.rerun()
        
        with example_col2:
            if st.button("ROMANCE + VINYL", use_container_width=True):
                st.session_state.temp_prompt = "A romantic comedy involving vintage vinyl records and food trucks"
                st.rerun()
    
    # Handle temp prompt
    if hasattr(st.session_state, 'temp_prompt'):
        create_story_opener(st.session_state.temp_prompt)
        del st.session_state.temp_prompt

def show_taste_profile_builder():
    """Display taste profile builder interface."""
    st.write("Tell us about your preferences to enrich your story with cultural insights:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        music_prefs = st.text_input("Music you enjoy:")
        film_prefs = st.text_input("Favorite films/genres:")
        book_prefs = st.text_input("Books you love:")
    
    with col2:
        travel_prefs = st.text_input("Places you'd visit:")
        brand_prefs = st.text_input("Brands you like:")
        other_prefs = st.text_input("Other interests:")
    
    if st.button("Build Profile"):
        preferences = {
            "music": music_prefs.split(",") if music_prefs else [],
            "film": film_prefs.split(",") if film_prefs else [],
            "books": book_prefs.split(",") if book_prefs else [],
            "travel": travel_prefs.split(",") if travel_prefs else [],
            "brands": brand_prefs.split(",") if brand_prefs else [],
            "other": other_prefs.split(",") if other_prefs else []
        }
        
        # Clean up preferences
        preferences = {k: [item.strip() for item in v if item.strip()] for k, v in preferences.items()}
        st.session_state.user_preferences = preferences
        
        # Get Qloo suggestions
        profile_result = st.session_state.qloo_service.get_taste_profile_suggestions(preferences)
        
        if profile_result["success"]:
            st.success("Profile created! Your cultural affinities will enrich your stories.")
            if profile_result.get("suggestions"):
                st.write("Story suggestions based on your profile:")
                for suggestion in profile_result["suggestions"]:
                    st.write(f"• {suggestion}")
        else:
            st.warning("Could not generate full profile, but your preferences are saved.")

def create_story_opener(prompt: str):
    """Create the initial story using Perplexity and Qloo."""
    try:
        st.write("🔄 Processing your story request...")
        
        with st.spinner("Creating your story opener..."):
            # Check if services are initialized
            if not hasattr(st.session_state, 'qloo_service') or not hasattr(st.session_state, 'perplexity_service'):
                st.error("Services not initialized. Please refresh the page.")
                return
            
            st.write("📡 Getting cultural context from Qloo...")
            # Get cultural context from Qloo
            cultural_context = st.session_state.qloo_service.create_cultural_context(prompt)
            
            if cultural_context:
                st.write(f"✅ Cultural context found: {cultural_context[:100]}...")
                SessionManager.set_cultural_context(cultural_context)
                # Add cultural explanation
                SessionManager.add_cultural_explanation(
                    "Story Cultural Elements",
                    f"Qloo identified these cultural affinities: {cultural_context}"
                )
            else:
                st.write("ℹ️ No specific cultural context found, proceeding with story generation...")
            
            st.write("🤖 Generating story with Perplexity Sonar Pro...")
            # Generate story opener with Perplexity
            result = st.session_state.perplexity_service.generate_story_opener(prompt, cultural_context)
            
            if result["success"]:
                st.write("✅ Story generated successfully!")
                # Add entries to story
                SessionManager.add_story_entry(prompt, "user")
                SessionManager.add_story_entry(result["content"], "ai")
                SessionManager.increment_turn()
                st.session_state.story_started = True
                st.success("Story created! Refreshing interface...")
                st.rerun()
            else:
                st.error(f"❌ Story generation failed: {result['error']}")
                SessionManager.set_error(result["error"])
                
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.write("Please check your internet connection and API keys.")

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
            st.markdown("Qloo AI has discovered these cultural connections in your story:")
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
        placeholder="What happens next in your story? Describe actions, dialogue, or new elements to explore...",
        height=120,
        key="story_input",
        help="Your input will be enriched with cultural context automatically."
    )
    
    # Action buttons in a clean layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("CONTINUE STORY", disabled=not user_input.strip(), use_container_width=True):
            continue_story(user_input)
    
    with col2:
        if st.button("GET OPTIONS", use_container_width=True):
            generate_branching_options()
    
    with col3:
        if st.button("ENHANCE CULTURE", use_container_width=True):
            enhance_with_culture()
    
    with col4:
        if st.button("SURPRISE ME", use_container_width=True):
            surprise_continuation()

def show_branching_options():
    """Display branching narrative options."""
    st.markdown('<div class="section-header">Choose Your Path</div>', unsafe_allow_html=True)
    
    for i, option in enumerate(st.session_state.branching_options):
        if st.button(f"Option {i+1}: {option}", key=f"option_{i}"):
            continue_story(option, is_branching_choice=True)

def continue_story(user_input: str, is_branching_choice: bool = False):
    """Continue the story with user input."""
    with st.spinner("AI is continuing the story..."):
        # Add user input to history
        if not is_branching_choice:
            SessionManager.add_story_entry(user_input, "user")
        
        # Get AI continuation
        result = st.session_state.perplexity_service.continue_story(
            st.session_state.story_history,
            user_input,
            st.session_state.cultural_context
        )
        
        if result["success"]:
            SessionManager.add_story_entry(result["content"], "ai")
            SessionManager.increment_turn()
            
            # Clear branching options and input
            st.session_state.branching_options = []
            
            # Enhance with new cultural context if entities found
            enhance_story_with_new_culture(user_input)
            
            st.rerun()
        else:
            SessionManager.set_error(result["error"])
            st.rerun()

def generate_branching_options():
    """Generate branching narrative options."""
    with st.spinner("Generating story options..."):
        current_story = SessionManager.get_story_text()
        
        result = st.session_state.perplexity_service.generate_branching_options(
            current_story,
            st.session_state.cultural_context
        )
        
        if result["success"]:
            st.session_state.branching_options = result["options"]
            st.rerun()
        else:
            SessionManager.set_error(result["error"])
            st.rerun()

def enhance_with_culture():
    """Enhance story with additional cultural context."""
    with st.spinner("Discovering cultural connections..."):
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
            
            st.success("New cultural connections discovered!")
            st.rerun()
        else:
            st.info("No new cultural connections found at this time.")

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
        if st.button("Download Text"):
            text_content = ExportUtils.create_story_text(story_data)
            st.download_button(
                label="Download Story.txt",
                data=text_content,
                file_name=f"narravox_story_{story_data['session_id'][:8]}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("Download PDF"):
            try:
                pdf_path = ExportUtils.create_story_pdf(story_data)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Story.pdf",
                        data=pdf_file.read(),
                        file_name=f"narravox_story_{story_data['session_id'][:8]}.pdf",
                        mime="application/pdf"
                    )
                ExportUtils.cleanup_temp_file(pdf_path)
            except Exception as e:
                st.error(f"PDF generation failed: {str(e)}")
    
    with col3:
        if st.button("Copy Share Link"):
            share_link = ExportUtils.create_shareable_link(story_data['session_id'])
            st.code(share_link)
            st.info("Link copied! (Feature will be available after deployment)")

def surprise_continuation():
    """Generate a surprise story continuation with random cultural elements."""
    surprise_prompts = [
        "Suddenly, an unexpected character from a different cultural background appears",
        "The story takes a turn involving an ancient tradition or modern trend",
        "A cultural artifact or symbol becomes central to the plot",
        "The setting shifts to a location rich with cultural significance",
        "A piece of music, art, or literature influences the characters' actions"
    ]
    
    import random
    surprise_element = random.choice(surprise_prompts)
    continue_story(surprise_element, is_branching_choice=True)

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

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("PERPLEXITY_API_KEY"):
        st.error("Please set PERPLEXITY_API_KEY environment variable")
        st.stop()
    
    if not os.getenv("QLOO_API_KEY"):
        st.error("Please set QLOO_API_KEY environment variable")
        st.stop()
    
    main() 