"""
Rahhal Park - Streamlit Cloud Entry Point
This file serves as the main entry point for Streamlit Cloud deployment.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from app.app import main

if __name__ == "__main__":
    main()
