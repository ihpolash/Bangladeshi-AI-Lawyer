# Running the AI-Lawyer Bangladesh Application

This document provides instructions for setting up and running the AI-Lawyer Bangladesh application.

## Prerequisites

Before running the application, you need to have the following installed:

1. Python 3.8 or higher
2. Pip (Python package manager)
3. For image processing: Tesseract OCR
4. For audio processing: PortAudio or equivalent for your platform

## Installation

1. Clone the repository (if you haven't already):
   ```
   git clone <your-repository-url>
   cd AI-Lawyer
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   
   Then edit the `.env` file with your preferred settings.

4. If you're using Hugging Face models that require authentication, add your Hugging Face API token to the `.env` file:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   ```

## Testing the Installation

Before running the full application, you can test the Hugging Face API connection:

```
python test_api.py
```

This will verify that your environment is properly set up to download and use the language models.

## Running the Application

To start the Streamlit application:

```
streamlit run app.py
```

This will launch the application and open it in your default web browser. If it doesn't open automatically, you can access it at `http://localhost:8501`.

## Application Structure

The application is organized as follows:

- `app.py`: Main application entry point
- `app/components/`: UI components
- `app/models/`: AI model implementations
- `app/utils/`: Utility functions
- `app/data/`: Legal data in JSON format
- `app/assets/`: Static assets like CSS and images

## Features

- **Multi-modal Input**: Submit queries through text, audio recordings, or document images
- **Specialized Legal Agents**: Domain-specific agents for different areas of Bangladesh law
- **Multilingual Support**: Interact in Bengali and English
- **Document Analysis**: Upload and analyze legal documents
- **Citation & References**: Get legal advice with citations to relevant laws
- **Consultation History**: Review previous consultations

## Troubleshooting

If you encounter any issues:

1. Check that all dependencies are installed correctly
2. Verify your `.env` file has the correct settings
3. Ensure you have proper internet connectivity to download models
4. Check the console logs for specific error messages

For audio transcription issues, make sure your audio input devices are properly configured.

For image processing issues, ensure Tesseract OCR is properly installed and accessible.

## Limitations

- The application requires internet connectivity to download models on first use
- Large language models may take significant time to load initially
- Audio and image processing may not work perfectly in all environments

## License

This project is licensed under the MIT License - see the LICENSE file for details. 