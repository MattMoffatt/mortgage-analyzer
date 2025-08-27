import streamlit as st

def initialize_mortgage_app_state():
    """
    Initialize minimal session state variables needed for the mortgage app.
    """
    # Mortgage objects
    if "current_mortgage" not in st.session_state:
        st.session_state.current_mortgage = None
        
    if "new_mortgage" not in st.session_state:
        st.session_state.new_mortgage = None
        
