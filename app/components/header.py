import streamlit as st

def create_header():
    """
    Creates the main header for the AI-Lawyer application.
    This function is responsible for the title, subtitle, and any introductory elements.
    """
    # Main title and description in a styled container
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])
        
        with col2:
            st.markdown(
                """
                <div class="main-header">
                    <h1>🇧🇩 AI-Lawyer Bangladesh</h1>
                    <p>Your AI-powered legal consultant for Bangladesh law</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Introduction text
            st.markdown(
                """
                Welcome to AI-Lawyer, your intelligent legal assistant for navigating Bangladesh's legal system. 
                Get professional legal consultation by submitting your query through text, voice, or document upload.
                
                Our specialized AI agents are trained on Bangladesh's laws and precedents to provide you with accurate
                and relevant legal guidance.
                
                **Disclaimer:** While our AI provides legal information based on Bangladesh law, it should not replace 
                professional legal advice. For critical matters, please consult with a licensed attorney.
                """
            ) 