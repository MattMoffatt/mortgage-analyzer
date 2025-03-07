import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st

# Import the session utility
from src.utils.session_utils import initialize_mortgage_app_state

# Initialize all session state variables properly
initialize_mortgage_app_state()

st.switch_page("pages/00_🏡_Home_Page_(pun_intended).py")
