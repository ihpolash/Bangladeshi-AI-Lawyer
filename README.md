# AI-Lawyer: Advanced Legal Consultation System for Bangladesh

A professional-grade AI-powered legal consultation application tailored specifically for Bangladesh's legal system. This application leverages open-source models from Huggingface to provide accurate, accessible legal advice across various domains of law.

## Features

- **Multi-modal Input**: Submit queries through text, audio recordings, or images of documents
- **Specialized Legal Agents**: Access domain-specific AI agents trained for different areas of Bangladesh law:
  - Family Law
  - Criminal Law
  - Property Law
  - Business & Corporate Law
  - Constitutional Law
  - Labor Law
  - Tax Law
  - Immigration Law
  
- **Multilingual Support**: Interact in Bengali and English
- **Document Analysis**: Upload and analyze legal documents
- **Citation & References**: Get legal advice with citations to relevant laws and precedents
- **Consultation History**: Review previous consultations
- **Audio Responses**: Get responses read aloud (optional)

## Technical Implementation

- **Frontend**: Streamlit web application
- **Models**: Huggingface open-source language and multimodal models
- **Processing Pipeline**: 
  1. Input Collection
  2. Preprocessing
  3. Legal Domain Classification
  4. Specialized Agent Assignment
  5. Response Generation with Citations
  6. Explanation Generation

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/AI-Lawyer.git
cd AI-Lawyer
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

3. Install system dependencies (if processing audio and images):
```
# For Ubuntu/Debian
sudo apt-get install tesseract-ocr portaudio19-dev

# For Windows
# Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
```

4. Run the application:
```
streamlit run app.py
```

## Usage

1. Select your preferred language
2. Choose the input mode (text, audio, or image)
3. Select the relevant legal category
4. Submit your query/document
5. Review the AI's response and ask follow-up questions

## Privacy & Disclaimers

- All processing is done locally on your machine
- No data is sent to external servers
- This tool is for informational purposes only and does not substitute for professional legal advice
- Always consult with a qualified lawyer for critical legal matters

## License

MIT License

## Contributors

- [Your Name](https://github.com/yourusername) 