import streamlit as st

def initialize_session_state():
    """
    Initializes the session state variables used throughout the application.
    This ensures that important state variables are always available when needed.
    """
    # Initialize language preference if not set
    if "language" not in st.session_state:
        st.session_state.language = "English"
    
    # Initialize submit clicked flag if not set
    if "submit_clicked" not in st.session_state:
        st.session_state.submit_clicked = False
    
    # Initialize consultation history if not set
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # Initialize model settings if not set
    if "model_type" not in st.session_state:
        st.session_state.model_type = "Standard"
    
    # Initialize voice settings if not set
    if "enable_voice" not in st.session_state:
        st.session_state.enable_voice = False
    
    if "voice_type" not in st.session_state:
        st.session_state.voice_type = "Conversational"
    
    # Initialize user preferences if not set
    if "user_preferences" not in st.session_state:
        st.session_state.user_preferences = {
            "theme": "light",
            "font_size": "medium",
            "notifications": True,
            "citation_style": "standard"
        }


def reset_input_states():
    """
    Resets the input-related session states.
    Useful after a submission has been processed.
    """
    st.session_state.submit_clicked = False
    
    # Clear any temporary input storage
    if "temp_text_input" in st.session_state:
        del st.session_state.temp_text_input
        
    if "temp_audio_path" in st.session_state:
        del st.session_state.temp_audio_path
        
    if "temp_image_path" in st.session_state:
        del st.session_state.temp_image_path 