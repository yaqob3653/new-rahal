"""
Centralized configuration for environment variables.
Supports both local .env files and Streamlit Cloud secrets.
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

def get_env_var(key, default=None):
    """
    Get environment variable from Streamlit secrets (Cloud) or os.getenv (Local).
    
    Args:
        key: The environment variable key
        default: Default value if not found
        
    Returns:
        The environment variable value
    """
    try:
        # Try Streamlit secrets first (for Cloud deployment)
        return st.secrets.get(key, os.getenv(key, default))
    except:
        # Fall back to os.getenv (for local development)
        return os.getenv(key, default)

# Load configuration
SUPABASE_URL = get_env_var("SUPABASE_URL")
SUPABASE_KEY = get_env_var("SUPABASE_KEY")
WEATHER_API_KEY = get_env_var("WEATHER_API_KEY")
