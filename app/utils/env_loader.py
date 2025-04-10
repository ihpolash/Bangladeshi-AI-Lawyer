import os
from dotenv import load_dotenv
import streamlit as st

def load_environment():
    """
    Load environment variables from .env file.
    Will not override existing environment variables.
    
    Returns:
        dict: A dictionary of environment variables
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Create a dictionary of environment variables
    env_vars = {
        # Hugging Face Hub settings
        "HUGGINGFACE_API_TOKEN": os.getenv("HUGGINGFACE_API_TOKEN", ""),
        
        # Application settings
        "DEBUG": os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
        "LANGUAGE": os.getenv("LANGUAGE", "English"),
        
        # Model settings
        "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "google/flan-t5-small"),
        "USE_LOCAL_MODELS": os.getenv("USE_LOCAL_MODELS", "True").lower() in ("true", "1", "t"),
        "MODEL_CACHE_DIR": os.getenv("MODEL_CACHE_DIR", "./model_cache"),
        
        # Feature flags
        "ENABLE_AUDIO_TRANSCRIPTION": os.getenv("ENABLE_AUDIO_TRANSCRIPTION", "True").lower() in ("true", "1", "t"),
        "ENABLE_DOCUMENT_ANALYSIS": os.getenv("ENABLE_DOCUMENT_ANALYSIS", "True").lower() in ("true", "1", "t"),
        "ENABLE_VOICE_RESPONSE": os.getenv("ENABLE_VOICE_RESPONSE", "False").lower() in ("true", "1", "t"),
    }
    
    # Set Hugging Face API token in environment if provided
    if env_vars["HUGGINGFACE_API_TOKEN"]:
        os.environ["HUGGINGFACE_TOKEN"] = env_vars["HUGGINGFACE_API_TOKEN"]
    
    # Store environment variables in session state for easy access
    if "env" not in st.session_state:
        st.session_state.env = env_vars
    
    return env_vars 