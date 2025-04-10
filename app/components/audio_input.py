import streamlit as st
import os
import tempfile
import numpy as np
import speech_recognition as sr
from datetime import datetime
import soundfile as sf

def create_audio_input():
    """
    Creates an audio input component for the AI-Lawyer application.
    This component allows users to record or upload audio for their legal queries.
    
    Returns:
        str: The transcribed text from audio if processed, None otherwise
    """
    
    # Container for audio input
    with st.container():
        st.markdown("### Record or upload your legal question")
        
        # Tabs for different audio input methods
        record_tab, upload_tab = st.tabs(["Record Audio", "Upload Audio File"])
        
        transcribed_text = None
        
        with record_tab:
            st.markdown("Please record your legal question or describe your situation:")
            
            # Audio recorder widget
            audio_bytes = st.audio_recorder(
                text="Click to record",
                recording_color="#e8b62c", 
                neutral_color="#6aa36f",
                pause_threshold=2.0
            )
            
            if audio_bytes:
                # Save audio bytes to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_bytes)
                    temp_filename = tmp_file.name
                
                st.audio(audio_bytes, format="audio/wav")
                
                # Transcribe button
                if st.button("Transcribe Recording", key="transcribe_recording"):
                    with st.spinner("Transcribing your audio..."):
                        transcribed_text = transcribe_audio(temp_filename)
                        
                        if transcribed_text:
                            st.success("Audio transcribed successfully!")
                            st.markdown("### Transcription:")
                            st.markdown(f'"{transcribed_text}"')
                        else:
                            st.error("Failed to transcribe audio. Please try again or upload an audio file.")
        
        with upload_tab:
            st.markdown("Upload an audio file containing your legal question:")
            
            # File uploader widget
            uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a", "ogg"])
            
            if uploaded_file is not None:
                # Save uploaded file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_filename = tmp_file.name
                
                st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
                
                # Transcribe button
                if st.button("Transcribe Upload", key="transcribe_upload"):
                    with st.spinner("Transcribing your audio..."):
                        transcribed_text = transcribe_audio(temp_filename)
                        
                        if transcribed_text:
                            st.success("Audio transcribed successfully!")
                            st.markdown("### Transcription:")
                            st.markdown(f'"{transcribed_text}"')
                        else:
                            st.error("Failed to transcribe audio. Please check the file format and try again.")
        
        # If we have transcribed text, allow submission
        if transcribed_text:
            # Additional context
            with st.expander("Add additional context (optional)"):
                # Allow user to edit the transcription
                transcribed_text = st.text_area(
                    "Edit transcription if needed:",
                    value=transcribed_text,
                    height=150
                )
                
                location = st.text_input(
                    "Location in Bangladesh:",
                    placeholder="e.g., Dhaka, Chittagong, etc."
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.button("Submit Query", type="primary", use_container_width=True)
            
            # If the submit button is clicked
            if submit_button and transcribed_text.strip():
                # Store the submission in session state
                st.session_state.submit_clicked = True
                
                # Add location context if provided
                if location:
                    transcribed_text += f"\n\nLocation: {location}"
                
                return transcribed_text
    
    # If no submission, return None
    return None


def transcribe_audio(audio_file_path):
    """
    Transcribes the given audio file to text.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text, or None if transcription failed
    """
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Load the audio file
        with sr.AudioFile(audio_file_path) as source:
            # Record the audio data
            audio_data = recognizer.record(source)
            
            # Attempt to recognize speech using Google Speech Recognition
            # In a production environment, you'd use a local model like Whisper
            text = recognizer.recognize_google(audio_data)
            return text
            
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None
    finally:
        # Clean up temporary file
        if os.path.exists(audio_file_path):
            os.unlink(audio_file_path) 