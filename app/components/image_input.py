import streamlit as st
import os
import tempfile
import pytesseract
from PIL import Image
import cv2
import numpy as np

def create_image_input():
    """
    Creates an image input component for the AI-Lawyer application.
    This component allows users to upload images of legal documents for analysis.
    
    Returns:
        dict: A dictionary containing the extracted text and the image path if processed, None otherwise
    """
    
    # Container for image input
    with st.container():
        st.markdown("### Upload legal documents or images")
        
        # File uploader for images
        uploaded_file = st.file_uploader(
            "Upload document images or photos",
            type=["jpg", "jpeg", "png", "pdf"],
            help="You can upload images of legal documents, contracts, notices, or any other relevant visual evidence."
        )
        
        if uploaded_file is not None:
            # Create temp file to save the uploaded image
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_filename = tmp_file.name
            
            # Display the uploaded image
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Document", use_column_width=True)
            
            # Process the image
            with st.spinner("Processing document..."):
                # Extract text from the image
                extracted_text = extract_text_from_image(temp_filename)
                
                if extracted_text:
                    st.success("Document processed successfully!")
                    
                    # Show the extracted text with an option to edit
                    with st.expander("Extracted Text (click to view/edit)"):
                        extracted_text = st.text_area(
                            "Review and edit the extracted text if needed:",
                            value=extracted_text,
                            height=250
                        )
                    
                    # Additional context
                    with st.expander("Add additional context (optional)"):
                        document_type = st.selectbox(
                            "Document type:",
                            [
                                "Select document type",
                                "Contract",
                                "Court Notice",
                                "Property Deed",
                                "Marriage Certificate",
                                "Divorce Papers",
                                "Business Registration",
                                "Tax Document",
                                "Police Report",
                                "Other"
                            ],
                            index=0
                        )
                        
                        if document_type == "Other":
                            document_type = st.text_input("Specify document type:")
                        
                        context = st.text_area(
                            "Additional information about this document:",
                            placeholder="E.g., This is a rental agreement I signed last year, but the landlord is now claiming different terms."
                        )
                    
                    # Submit button
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        submit_button = st.button("Submit for Analysis", type="primary", use_container_width=True)
                    
                    # Process submission
                    if submit_button and extracted_text.strip():
                        # Store the submission in session state
                        st.session_state.submit_clicked = True
                        
                        result = {
                            "text": extracted_text,
                            "image_path": temp_filename
                        }
                        
                        # Add metadata if available
                        if document_type and document_type != "Select document type":
                            result["document_type"] = document_type
                        
                        if context:
                            result["context"] = context
                        
                        return result
                else:
                    st.error("Failed to extract text from the document. Please try uploading a clearer image.")
        
        # Usage tips
        with st.expander("Tips for best results"):
            st.markdown("""
                **For best document analysis results:**
                - Ensure the document is well-lit and the text is clearly visible
                - Take photos straight-on to avoid distortion
                - Include the entire document in the frame
                - If uploading a photo of a physical document, place it on a contrasting background
                - Higher resolution images will yield better text extraction
            """)
    
    # If no submission, return None
    return None


def extract_text_from_image(image_path):
    """
    Extracts text from an image file using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text, or None if extraction failed
    """
    try:
        # Read the image with OpenCV
        image = cv2.imread(image_path)
        
        # Preprocess the image for better OCR
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get a binary image
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
        
        # Save the preprocessed image temporarily
        preprocessed_path = image_path + "_prep.jpg"
        cv2.imwrite(preprocessed_path, denoised)
        
        # Use pytesseract to extract text (you can use different languages here)
        # For Bengali: lang='ben'
        # For English: lang='eng'
        # For both: lang='eng+ben'
        text = pytesseract.image_to_string(Image.open(preprocessed_path), lang='eng')
        
        # Clean up preprocessed image
        os.remove(preprocessed_path)
        
        return text
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None
    finally:
        # Clean up image file if it exists
        if os.path.exists(image_path):
            # In a real application, you might want to keep this file for reference
            # or delete it after a certain period
            pass 