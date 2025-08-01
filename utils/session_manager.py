import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st

class SessionManager:
    """Manages story sessions and user interactions."""
    
    @staticmethod
    def init_session():
        """Initialize session state variables if they don't exist."""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        if 'story_history' not in st.session_state:
            st.session_state.story_history = []
        
        if 'current_story' not in st.session_state:
            st.session_state.current_story = ""
        
        if 'cultural_context' not in st.session_state:
            st.session_state.cultural_context = ""
        
        if 'turn_count' not in st.session_state:
            st.session_state.turn_count = 0
        
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        
        if 'story_started' not in st.session_state:
            st.session_state.story_started = False
        
        if 'last_error' not in st.session_state:
            st.session_state.last_error = None
        
        if 'branching_options' not in st.session_state:
            st.session_state.branching_options = []
        
        if 'cultural_explanations' not in st.session_state:
            st.session_state.cultural_explanations = {}
        
        if 'demo_mode' not in st.session_state:
            st.session_state.demo_mode = False
        
        if 'demo_prompt' not in st.session_state:
            st.session_state.demo_prompt = ""
        
        if 'temp_prompt' not in st.session_state:
            st.session_state.temp_prompt = ""
        
        if 'taste_suggestions' not in st.session_state:
            st.session_state.taste_suggestions = []
    
    @staticmethod
    def add_story_entry(content: str, entry_type: str, metadata: Dict = None):
        """Add an entry to the story history."""
        entry = {
            'id': str(uuid.uuid4()),
            'content': content,
            'type': entry_type,  # 'user', 'ai', 'system'
            'timestamp': datetime.now().isoformat(),
            'turn': st.session_state.turn_count,
            'metadata': metadata or {}
        }
        
        st.session_state.story_history.append(entry)
        
        # Update current story for display
        if entry_type in ['user', 'ai']:
            if st.session_state.current_story:
                st.session_state.current_story += f"\n\n{content}"
            else:
                st.session_state.current_story = content
    
    @staticmethod
    def increment_turn():
        """Increment the turn counter."""
        st.session_state.turn_count += 1
    
    @staticmethod
    def get_story_summary() -> str:
        """Get a summary of the current story for display."""
        if not st.session_state.story_history:
            return "No story started yet."
        
        story_parts = []
        for entry in st.session_state.story_history:
            if entry['type'] in ['user', 'ai']:
                prefix = "User: " if entry['type'] == 'user' else "AI: "
                story_parts.append(f"{prefix}{entry['content']}")
        
        return "\n\n".join(story_parts)
    
    @staticmethod
    def reset_session():
        """Reset the current session to start fresh."""
        # Keep session_id but reset everything else
        session_id = st.session_state.session_id
        
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key != 'session_id':
                del st.session_state[key]
        
        # Reinitialize
        SessionManager.init_session()
        st.session_state.session_id = session_id
    
    @staticmethod
    def export_story_data() -> Dict:
        """Export current story data for sharing or saving."""
        return {
            'session_id': st.session_state.session_id,
            'story_history': st.session_state.story_history,
            'current_story': st.session_state.current_story,
            'cultural_context': st.session_state.cultural_context,
            'turn_count': st.session_state.turn_count,
            'user_preferences': st.session_state.user_preferences,
            'export_timestamp': datetime.now().isoformat(),
            'cultural_explanations': st.session_state.cultural_explanations
        }
    
    @staticmethod
    def get_story_text() -> str:
        """Get clean story text for export."""
        story_parts = []
        
        for entry in st.session_state.story_history:
            if entry['type'] in ['user', 'ai']:
                story_parts.append(entry['content'])
        
        return "\n\n".join(story_parts)
    
    @staticmethod
    def set_cultural_context(context: str):
        """Set cultural context for the session."""
        st.session_state.cultural_context = context
    
    @staticmethod
    def add_cultural_explanation(key: str, explanation: str):
        """Add cultural explanation for later display."""
        st.session_state.cultural_explanations[key] = explanation
    
    @staticmethod
    def get_max_turns() -> int:
        """Get maximum allowed turns for a story."""
        return 15
    
    @staticmethod
    def is_story_complete() -> bool:
        """Check if story has reached maximum turns."""
        return st.session_state.turn_count >= SessionManager.get_max_turns()
    
    @staticmethod
    def set_error(error_message: str):
        """Set error message for display."""
        st.session_state.last_error = {
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def clear_error():
        """Clear error message."""
        st.session_state.last_error = None
    
    @staticmethod
    def get_session_stats() -> Dict:
        """Get session statistics."""
        return {
            'session_id': st.session_state.session_id,
            'turns_completed': st.session_state.turn_count,
            'max_turns': SessionManager.get_max_turns(),
            'story_length': len(st.session_state.current_story),
            'entries_count': len(st.session_state.story_history),
            'has_cultural_context': bool(st.session_state.cultural_context),
            'cultural_explanations_count': len(st.session_state.cultural_explanations)
        } 