import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import altair as alt
import streamlit as st

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario

# Check if both mortgage objects exist and are valid
if not (st.session_state.get("current_mortgage") and st.session_state.get("new_mortgage")):
    st.warning("Please fill out current and new mortgage scenario details.")
    st.stop()

currentMort = st.session_state.current_mortgage
NewMort = st.session_state.new_mortgage