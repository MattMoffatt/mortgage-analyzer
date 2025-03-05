import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.session_utils import initialize_mortgage_app_state
from src.utils.navigation_utils import register_page, safe_navigate

###############################################################

# Session state management

###############################################################

# Initialize all session state variables properly
initialize_mortgage_app_state()

# Register this as the home page (without an update function since there's nothing to save)
register_page("home_page", None)


###############################################################

# Page Layout

###############################################################


st.header("&ensp;&ensp;&ensp;&ensp;&ensp;:dollar::house: Mortgage Calculator App :house::dollar:", divider="violet")

st.subheader("This app helps you compare your current mortgage to new mortgage \
scenarios you are pursuing.")

st.subheader("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;Navigation:", divider="grey")

col1, col2 = st.columns([2, 5])

# Initialize session state for mortgage objects
if "current_mortgage" not in st.session_state:
    st.session_state.current_mortgage = None
if "new_mortgage" not in st.session_state:
    st.session_state.new_mortgage = None

with col1:
    if st.button("💸 Current Mortgage"):
        safe_navigate("pages/01_💸_Current_Mortgage.py")
    
    if st.button("🆕 New Scenario"):
        safe_navigate("pages/02_🆕_New_Scenario.py")
    
    if st.button("📈 Comparison"):
        safe_navigate("pages/03_📈_Comparison.py")

with col2:
    st.write("input your current mortgage details")
    st.write("")
    st.write("select number of new mortgages (1-3) to review and input details")
    st.write("")
    st.write("review comparisons between current and new scenarios")

st.write("")
st.write("")
st.write("")
st.write("")

buff1, center, buff2 = st.columns([3,3,3])

with center:
    st.link_button("Original Repo Link", "https://github.com/MattMoffatt/mortgage-analyzer")

