import streamlit as st
from dotenv import load_dotenv
import os

# Load Environment Variables FIRST (before importing modules that need them)
load_dotenv()

# Import modules
from src.app.login_page import login_page
from src.app.dashboard import show_dashboard

# Page Configuration
st.set_page_config(
    page_title="Rahhal Admin",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
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

if __name__ == "__main__":
    main()
