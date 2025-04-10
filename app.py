import streamlit as st
import os
from app.components.sidebar import create_sidebar
from app.components.header import create_header
from app.components.text_input import create_text_input
from app.components.audio_input import create_audio_input
from app.components.image_input import create_image_input
from app.utils.session_state import initialize_session_state
from app.utils.env_loader import load_environment
from app.models.legal_agent import get_legal_agent
import pandas as pd

# Load environment variables
env = load_environment()

# Page configuration
st.set_page_config(
    page_title="AI-Lawyer | Bangladesh Legal Consultant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
with open("app/assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state for persistent data
    initialize_session_state()
    
    # Create sidebar with navigation and options
    create_sidebar()
    
    # Create header with title and description
    create_header()
    
    # Main content area
    st.write("---")
    
    # Input selection tabs
    input_tab, history_tab = st.tabs(["New Consultation", "Consultation History"])
    
    with input_tab:
        # User selects input method
        input_method = st.radio(
            "Choose how you'd like to communicate:",
            ["Text", "Audio", "Image/Document"],
            horizontal=True,
        )
        
        # Legal domain selection
        legal_categories = [
            "Family Law", 
            "Criminal Law", 
            "Property Law", 
            "Business & Corporate", 
            "Constitutional Law",
            "Labor Law",
            "Tax Law", 
            "Immigration Law", 
            "General Legal Advice"
        ]
        
        selected_category = st.selectbox(
            "Select legal domain for your query:",
            legal_categories
        )
        
        # Input components based on selected method
        user_input = None
        if input_method == "Text":
            user_input = create_text_input()
        elif input_method == "Audio" and env.get("ENABLE_AUDIO_TRANSCRIPTION", True):
            user_input = create_audio_input()
        elif input_method == "Image/Document" and env.get("ENABLE_DOCUMENT_ANALYSIS", True):
            user_input = create_image_input()
        else:
            st.warning("This input method is currently disabled. Please use text input instead.")
            user_input = create_text_input()
            
        # Process the input if provided
        if user_input and st.session_state.get('submit_clicked', False):
            with st.spinner(f"Consulting with {selected_category} specialist..."):
                # Get the appropriate legal agent
                legal_agent = get_legal_agent(selected_category)
                
                # Process query with the legal agent
                response = legal_agent.process_query(
                    user_input, 
                    input_type=input_method.lower()
                )
                
                # Display response
                st.markdown("## Legal Advice")
                st.markdown(response['advice'])
                
                if response.get('citations'):
                    st.markdown("### References & Citations")
                    st.markdown(response['citations'])
                
                # Add to consultation history
                if 'history' not in st.session_state:
                    st.session_state.history = []
                    
                st.session_state.history.append({
                    'timestamp': pd.Timestamp.now(),
                    'category': selected_category,
                    'input_type': input_method,
                    'query': user_input,
                    'response': response
                })
                
                # If voice responses are enabled, provide audio output
                if st.session_state.get('enable_voice', False) and env.get("ENABLE_VOICE_RESPONSE", False):
                    st.markdown("### Audio Response")
                    st.warning("Voice response functionality will be implemented in a future update.")
                
                st.session_state.submit_clicked = False
    
    with history_tab:
        if 'history' in st.session_state and st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.expander(f"{item['timestamp'].strftime('%Y-%m-%d %H:%M')} - {item['category']}"):
                    st.markdown(f"**Input Method:** {item['input_type']}")
                    
                    if item['input_type'] == "Text":
                        st.markdown(f"**Query:** {item['query']}")
                    elif item['input_type'] == "Audio":
                        st.audio(item['query'])
                    else:  # Image
                        st.image(item['query'])
                        
                    st.markdown("**Response:**")
                    st.markdown(item['response']['advice'])
                    
                    if item['response'].get('citations'):
                        st.markdown("**Citations:**")
                        st.markdown(item['response']['citations'])
        else:
            st.info("No consultation history available. Start a new consultation to see your history.")
    
    # Debug mode
    if env.get("DEBUG", False):
        st.markdown("---")
        st.subheader("Debug Information")
        st.json({"session_state": {k: str(v) for k, v in st.session_state.items() if k != "history"}})

# Run the application
if __name__ == "__main__":
    main() 