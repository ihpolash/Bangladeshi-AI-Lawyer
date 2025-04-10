import streamlit as st

def create_sidebar():
    """
    Creates the sidebar for the AI-Lawyer application.
    Includes language selection, about section, and other settings.
    """
    with st.sidebar:
        # Text-based logo instead of image
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #2e4057; margin-bottom: 0;">⚖️</h1>
                <h2 style="color: #2e4057; margin-bottom: 0;">AI-Lawyer</h2>
                <p style="color: #48639c;">Bangladesh Legal Specialist</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.caption("v1.0.0")
        
        st.markdown("---")
        
        # Language selection
        language = st.selectbox(
            "Language / ভাষা",
            options=["English", "বাংলা (Bengali)"],
            index=0
        )
        
        if language != st.session_state.get("language", "English"):
            st.session_state.language = language
            # In a real app, you would implement language switching logic here
        
        st.markdown("---")
        
        # Settings
        st.subheader("Settings")
        
        # AI Model selection
        model_options = {
            "Standard": "A balanced model for general legal advice",
            "Advanced": "More in-depth analysis for complex legal matters (slower)",
            "Efficient": "Faster responses for simpler queries"
        }
        
        selected_model = st.radio(
            "AI Model",
            options=list(model_options.keys()),
            index=0,
            help="Select the AI model that best fits your needs"
        )
        
        st.caption(model_options[selected_model])
        
        # Voice output option
        enable_voice = st.checkbox("Enable voice responses", value=False)
        if enable_voice:
            voice_type = st.select_slider(
                "Voice style",
                options=["Formal", "Conversational", "Detailed"]
            )
        
        st.markdown("---")
        
        # About section
        with st.expander("About AI-Lawyer"):
            st.markdown(
                """
                **AI-Lawyer** is an advanced legal consultation tool designed specifically for 
                Bangladesh's legal system. Our application uses natural language processing and 
                machine learning models from Hugging Face to provide you with relevant legal information 
                and guidance.
                
                The system is trained on Bangladesh's legal code, precedents, and common legal practices 
                to deliver accurate and contextually relevant advice.
                
                For feedback or support, please contact:
                support@ai-lawyer-bd.example.com
                """
            )
            
        # Disclaimer
        with st.expander("Disclaimer"):
            st.markdown(
                """
                **Legal Disclaimer:**
                
                The information provided by AI-Lawyer is for general informational purposes only 
                and is not intended to be legal advice. The application does not create an attorney-client 
                relationship. While we strive to provide accurate information, laws change frequently 
                and vary from jurisdiction to jurisdiction.
                
                Always consult a qualified lawyer for specific legal advice regarding your particular 
                situation. Never disregard professional legal advice or delay in seeking it because of 
                something you have read on this application.
                """
            )
            
        # Add version information at the bottom
        st.markdown("---")
        st.caption("© 2023 AI-Lawyer Bangladesh") 