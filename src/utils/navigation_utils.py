import sys
import datetime as dt
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from typing import Dict, Callable, Optional

def initialize_navigation_system():
    # Initialize the navigation system in session state if not already present.
    if "current_page" not in st.session_state:
        st.session_state.current_page = None
    
    # if on_page_exit key is not yet in session state, create an empty directory to store later page key-values
    if "on_page_exit" not in st.session_state:
        st.session_state.on_page_exit = {}



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
The below function calls the initialize_navigation_system() function
to check if the current page is in session state and create a lookup table
for streamlit to know which update function to use when navigating 
away from the page.
  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""   

def register_page(page_id: str, update_function: Optional[Callable] = None):
    """
    Register the current page and its update function.
    
    Args:
        page_id: Unique identifier for this page
        update_function: Function to call when navigating away from this page
    """
    # Initialize the navigation system if needed
    initialize_navigation_system()
    
    # Register the update function for this page
    st.session_state.on_page_exit[page_id] = update_function # update functions found on mortgage_utils.py
    
    # Set the current page
    st.session_state.current_page = page_id


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
This function utilizes the lookup table to run the update function
associated with the page before navigating away. 
  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""  


def safe_navigate(page_path: str):
    """
    Safely navigate to another page, ensuring any exit handlers are called first.
    
    Args:
        page_path: Path to the page to navigate to
    """
    # Run the update function for the current page if it exists
    current_page = st.session_state.get("current_page")
    if current_page and current_page in st.session_state.on_page_exit:
        update_function = st.session_state.on_page_exit[current_page]
        if update_function:
            update_function()
    
    # Then navigate
    st.switch_page(page_path)