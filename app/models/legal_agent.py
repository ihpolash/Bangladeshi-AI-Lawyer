import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
import nltk
from nltk.tokenize import sent_tokenize
import json
import time

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Legal domain model mappings
LEGAL_MODELS = {
    "Family Law": "google/flan-t5-small",
    "Criminal Law": "google/flan-t5-small",
    "Property Law": "google/flan-t5-small",
    "Business & Corporate": "google/flan-t5-small",
    "Constitutional Law": "google/flan-t5-small",
    "Labor Law": "google/flan-t5-small",
    "Tax Law": "google/flan-t5-small",
    "Immigration Law": "google/flan-t5-small",
    "General Legal Advice": "google/flan-t5-small"
}

# Default models when specific ones are not available
DEFAULT_MODEL = "google/flan-t5-small"
DOCUMENT_MODEL = "BAAI/bge-small-en-v1.5"
SPEECH_MODEL = "google/flan-t5-small"

# Model config based on user selection
MODEL_CONFIG = {
    "Standard": {
        "max_length": 512,
        "temperature": 0.7,
        "top_p": 0.9,
    },
    "Advanced": {
        "max_length": 1024,
        "temperature": 0.6,
        "top_p": 0.8,
    },
    "Efficient": {
        "max_length": 256,
        "temperature": 0.8,
        "top_p": 0.95,
    }
}

# Load specialized legal data from JSON files (if available)
def load_legal_data(category):
    try:
        data_file = os.path.join("app", "data", f"{category.lower().replace(' & ', '_').replace(' ', '_')}.json")
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading legal data: {e}")
        return {}

class LegalAgent:
    """
    LegalAgent class that handles legal queries using Huggingface models.
    Each instance is specialized for a particular legal domain.
    """
    
    def __init__(self, category):
        """
        Initialize a legal agent for the given category.
        
        Args:
            category (str): The legal domain/category for this agent
        """
        self.category = category
        self.model_name = LEGAL_MODELS.get(category, DEFAULT_MODEL)
        self.legal_data = load_legal_data(category)
        
        # Get model configuration based on user preferences
        model_type = st.session_state.get("model_type", "Standard")
        self.config = MODEL_CONFIG[model_type]
        
        # Initialize model and tokenizer lazily (only when needed)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        
    def _load_model(self):
        """Load the model and tokenizer if they haven't been loaded yet"""
        if self.model is None or self.tokenizer is None:
            with st.spinner(f"Loading {self.category} specialist model... This may take a moment."):
                # Load model with lower precision for efficiency
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                
                # Use sequence-to-sequence model for T5 models
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    self.model_name, 
                    torch_dtype=torch.float16,
                    device_map="auto",
                    load_in_8bit=True
                )
                
                # Create text generation pipeline
                self.pipeline = pipeline(
                    "text2text-generation",  # Use text2text-generation for seq2seq models
                    model=self.model,
                    tokenizer=self.tokenizer,
                    max_length=self.config["max_length"],
                    temperature=self.config["temperature"],
                    top_p=self.config["top_p"]
                )
    
    def _preprocess_query(self, query, input_type="text"):
        """
        Preprocess the query based on input type.
        
        Args:
            query: The user query (text string or dict for image/document input)
            input_type: The type of input ('text', 'audio', or 'image')
            
        Returns:
            str: The preprocessed query ready for the model
        """
        if input_type == "text":
            return query
        
        elif input_type == "audio":
            # For audio, we already have the transcribed text
            return query
        
        elif input_type == "image/document":
            # For document/image, extract the text and any context
            if isinstance(query, dict):
                result = f"Document Analysis Request: {query.get('text', '')}"
                
                if query.get("document_type"):
                    result += f"\nDocument Type: {query['document_type']}"
                
                if query.get("context"):
                    result += f"\nContext: {query['context']}"
                    
                return result
            return str(query)
        
        # Default fallback
        return str(query)
    
    def _format_prompt(self, preprocessed_query):
        """
        Format the preprocessed query into a prompt for the model.
        
        Args:
            preprocessed_query: The preprocessed query
            
        Returns:
            str: The formatted prompt
        """
        # Create a prompt that includes the legal domain and Bangladesh context
        prompt = f"""You are an AI legal assistant specializing in {self.category} under Bangladesh law. 
        Provide accurate, helpful legal information based on Bangladesh's legal system.
        
        User Query: {preprocessed_query}
        
        Legal Analysis and Advice:"""
        
        return prompt
    
    def _extract_citations(self, response):
        """
        Extract legal citations from the response.
        
        Args:
            response: The model's response
            
        Returns:
            tuple: (response without citations, extracted citations)
        """
        # Simple implementation - in practice, this would use regex or NLP to identify citations
        sentences = sent_tokenize(response)
        citations = []
        regular_text = []
        
        for sentence in sentences:
            if any(citation_marker in sentence for citation_marker in ["Section", "Act", "Article", "Code", "vs.", "v."]):
                citations.append(sentence)
            else:
                regular_text.append(sentence)
        
        # If no citations were found in the standard way, check for a "References:" section
        if not citations and "References:" in response:
            parts = response.split("References:")
            if len(parts) > 1:
                regular_text = [parts[0]]
                citations = [f"References: {parts[1]}"]
        
        return " ".join(regular_text), "\n".join(citations) if citations else ""
    
    def _postprocess_response(self, raw_response):
        """
        Clean up and format the model's response.
        
        Args:
            raw_response: The raw response from the model
            
        Returns:
            dict: A dictionary with 'advice' and 'citations' keys
        """
        # Extract the generated text from the pipeline output
        if isinstance(raw_response, list) and len(raw_response) > 0:
            if isinstance(raw_response[0], dict) and "generated_text" in raw_response[0]:
                text = raw_response[0]["generated_text"]
            else:
                text = str(raw_response[0])
        else:
            text = str(raw_response)
        
        # Remove any prompt that might be included in the response
        if "User Query:" in text:
            text = text.split("Legal Analysis and Advice:")[-1]
        
        # Extract citations
        advice, citations = self._extract_citations(text.strip())
        
        # Format the response
        return {
            "advice": advice.strip(),
            "citations": citations.strip()
        }
    
    def _enhance_with_legal_data(self, response):
        """
        Enhance the response with specific Bangladesh legal data if available.
        
        Args:
            response: The response dictionary
            
        Returns:
            dict: The enhanced response
        """
        # If we don't have legal data for this category, return as is
        if not self.legal_data:
            return response
        
        # If there are no citations, add some based on the legal data
        if not response.get("citations") and self.legal_data.get("acts"):
            relevant_acts = []
            
            # Simple keyword matching to find relevant acts
            for act in self.legal_data.get("acts", []):
                # Check if keywords from the act appear in the response
                if any(keyword.lower() in response["advice"].lower() for keyword in act.get("keywords", [])):
                    relevant_acts.append(act)
            
            # Add citations for relevant acts
            if relevant_acts:
                citations = ["Relevant Bangladesh Laws and Regulations:"]
                for act in relevant_acts[:3]:  # Limit to 3 most relevant
                    citations.append(f"- {act['name']} ({act['year']}): {act.get('description', '')}")
                response["citations"] = "\n".join(citations)
        
        return response
    
    def process_query(self, query, input_type="text"):
        """
        Process a user query and generate a legal response.
        
        Args:
            query: The user query (text string or dict for document input)
            input_type: The type of input ('text', 'audio', or 'image')
            
        Returns:
            dict: A dictionary with the response including advice and citations
        """
        # Ensure the model is loaded
        self._load_model()
        
        # Preprocess the query based on input type
        preprocessed_query = self._preprocess_query(query, input_type)
        
        # Format the prompt for the model
        prompt = self._format_prompt(preprocessed_query)
        
        # Generate the response
        with st.spinner("Analyzing and generating legal advice..."):
            # Introduce a small delay to simulate deep thinking
            time.sleep(1)
            
            try:
                raw_response = self.pipeline(prompt)
                response = self._postprocess_response(raw_response)
                enhanced_response = self._enhance_with_legal_data(response)
                return enhanced_response
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                # Fallback response
                return {
                    "advice": "I apologize, but I encountered an issue while analyzing your query. Please try again or rephrase your question.",
                    "citations": ""
                }


def get_legal_agent(category):
    """
    Factory function to get or create a legal agent for the specified category.
    Caches agents to avoid reloading models unnecessarily.
    
    Args:
        category (str): The legal domain/category
        
    Returns:
        LegalAgent: An instance of LegalAgent for the specified category
    """
    # Check if we already have this agent in session state
    agent_key = f"legal_agent_{category.lower().replace(' & ', '_').replace(' ', '_')}"
    
    if agent_key not in st.session_state:
        # Create a new agent
        st.session_state[agent_key] = LegalAgent(category)
    
    return st.session_state[agent_key] 