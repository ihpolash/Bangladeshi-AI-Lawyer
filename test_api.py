import os
import sys
from dotenv import load_dotenv
import argparse
from transformers import AutoTokenizer, pipeline

def test_huggingface_api():
    """
    Test the Hugging Face API connection and model loading.
    """
    # Load environment variables
    load_dotenv()
    
    # Get API token from environment
    api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")
    
    print("Testing Hugging Face API connection...")
    
    if api_token:
        print("✓ API token found")
        # Set the token in the environment
        os.environ["HUGGINGFACE_TOKEN"] = api_token
    else:
        print("⚠ No API token found. Some models may not be accessible.")
    
    try:
        # Test loading a simple model
        model_name = "google/flan-t5-small"
        print(f"Loading model: {model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print(f"✓ Tokenizer loaded successfully")
        
        # Create a simple pipeline
        print("Creating text generation pipeline...")
        pipe = pipeline(
            "text-generation", 
            model=model_name,
            tokenizer=tokenizer,
            max_length=50
        )
        print("✓ Pipeline created successfully")
        
        # Test the pipeline
        prompt = "What are the basic principles of law?"
        print(f"Testing with prompt: '{prompt}'")
        
        result = pipe(prompt)
        
        if result:
            print("✓ Model generated a response successfully")
            print("\nSample output:")
            print(result[0]['generated_text'])
            print("\nAPI test completed successfully! The application should work correctly.")
            return True
        else:
            print("✗ Model failed to generate a response")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify your Hugging Face API token is correct")
        print("3. Try a different model")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Hugging Face API connection")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        # Enable verbose output
        from transformers import logging
        logging.set_verbosity_info()
    
    success = test_huggingface_api()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 