import os
import sys
import subprocess

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Run the Streamlit app
subprocess.run(['streamlit', 'run', 'app.py']) 