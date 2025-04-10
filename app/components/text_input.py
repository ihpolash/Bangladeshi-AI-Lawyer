import streamlit as st

def create_text_input():
    """
    Creates a text input component for the AI-Lawyer application.
    This component allows users to enter their legal queries as text.
    
    Returns:
        str: The user's text input if submitted, None otherwise
    """
    # Container for text input
    with st.container():
        st.markdown("### Describe your legal situation or question")
        
        # Text area for user query
        user_query = st.text_area(
            "Enter your query below:",
            height=150,
            placeholder=(
                "Example: My landlord is refusing to return my security deposit even though "
                "I left the apartment in good condition. What legal actions can I take in Bangladesh?"
            ),
            key="text_query"
        )
        
        # Additional context options to help the AI provide better answers
        with st.expander("Add additional details (optional)"):
            col1, col2 = st.columns(2)
            with col1:
                location = st.text_input(
                    "Location in Bangladesh:",
                    placeholder="e.g., Dhaka, Chittagong, etc."
                )
            
            with col2:
                time_context = st.text_input(
                    "When did this occur:",
                    placeholder="e.g., Last month, 2 weeks ago, etc."
                )
            
            # Relevant documents or legal references
            known_info = st.text_area(
                "Any laws or regulations you're aware of:",
                height=100,
                placeholder="e.g., I know the Rent Control Act mentions security deposits, but I'm not sure about the specifics."
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.button("Submit Query", type="primary", use_container_width=True)
        
        # If the submit button is clicked and there's text in the input
        if submit_button and user_query.strip():
            # Store the submission in session state to process it
            st.session_state.submit_clicked = True
            
            # Combine main query with optional context
            full_query = user_query
            if location or time_context or known_info:
                full_query += "\n\nAdditional Context:"
                if location:
                    full_query += f"\nLocation: {location}"
                if time_context:
                    full_query += f"\nTime Context: {time_context}"
                if known_info:
                    full_query += f"\nRelevant Information Known: {known_info}"
            
            return full_query
        
        # If the button wasn't clicked or there's no text, return None
        return None 