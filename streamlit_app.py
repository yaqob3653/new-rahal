"""
Rahhal Park - Streamlit Cloud Entry Point
This file serves as the main entry point for Streamlit Cloud deployment.
"""

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

import sys
import os

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import and run the main app
import streamlit as st
from src.app.login_page import login_page
from src.app.dashboard import show_dashboard

# Page Configuration
st.set_page_config(
    page_title="Rahhal Admin",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None

# Routing
if not st.session_state['authenticated']:
    login_page()
else:
    show_dashboard()
