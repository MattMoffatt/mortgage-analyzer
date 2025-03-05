import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from typing import Callable, Optional

def initialize_navigation_system():
    """
    Initialize the navigation system in session state if not already present.
    This only tracks the current page, it doesn't manage widget values.
    """
    if "current_page" not in st.session_state:
        st.session_state.current_page = None


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
The below function calls the initialize_navigation_system() function
to check if the current page is in session state and create a lookup table
for streamlit to know which update function to use when navigating 
away from the page.
  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""   

def register_page(page_id: str, update_function: Optional[Callable] = None):
    """
    Register the current page ID.
    Widget values will be automatically maintained by Streamlit's session state.
    
    Args:
        page_id: Unique identifier for this page
        update_function: Function to call when navigating away from this page
                        (can be None if not needed)
    """
    # Initialize the navigation system if needed
    initialize_navigation_system()
    
    # Set the current page
    st.session_state.current_page = page_id
    
    # Store update function if provided
    if update_function is not None:
        if "page_update_functions" not in st.session_state:
            st.session_state.page_update_functions = {}
        st.session_state.page_update_functions[page_id] = update_function


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
This function utilizes the lookup table to run the update function
associated with the page before navigating away. 
  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""  


def safe_navigate(page_path: str):
    """
    Safely navigate to another page.
    
    Args:
        page_path: Path to the page to navigate to
    """
    # Execute any update function if it exists for the current page
    current_page = st.session_state.get("current_page")
    if current_page and "page_update_functions" in st.session_state:
        update_function = st.session_state.page_update_functions.get(current_page)
        if update_function:
            try:
                update_function()
            except Exception as e:
                st.error(f"Error updating page data: {e}")
    
    # Then navigate
    st.switch_page(page_path)