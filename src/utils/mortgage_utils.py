import sys
from pathlib import Path
import datetime

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario


def update_current_mortgage():
    """
    Update the current_mortgage object in session state with latest values.
    Call this before navigating away from the Current Mortgage page.
    """
    if st.session_state.current_page == "current_mortgage":
        try:
            # Format the date properly
            if isinstance(st.session_state.cm_start_date, datetime):
                start_date_str = st.session_state.cm_start_date.strftime("%m/%d/%Y")
            else:
                start_date_str = st.session_state.cm_start_date
                
            # Update the current_mortgage object with latest values
            st.session_state.current_mortgage = CurrentMortgage(
                _rate=st.session_state.cm_rate,
                _years=st.session_state.cm_term,
                _tax=st.session_state.cm_tax_annual,
                _ins=st.session_state.cm_ins_annual,
                _sqft=st.session_state.cm_sqft,
                _extra_principal=st.session_state.cm_prin,
                _prepay_periods=st.session_state.cm_prepay,
                _original_loan=st.session_state.cm_origin,
                _loan_amount=st.session_state.cm_balance,
                _start_date=start_date_str,
                _price_per_sqft=st.session_state.cm_ppsqft,
                _monthly_pmi=st.session_state.cm_pmi,
                _total_pmt=st.session_state.cm_pmt
            )
        except Exception as e:
            st.error(f"Error updating current mortgage: {e}")

def update_new_mortgage():
    """
    Update the new_mortgage object in session state with latest values.
    Call this before navigating away from the New Mortgage page.
    """
    if st.session_state.current_page == "new_mortgage":
        try:
            # Update the new_mortgage object with latest values
            st.session_state.new_mortgage = NewMortgageScenario(
                _rate=st.session_state.nm_rate,
                _years=st.session_state.nm_term,
                _tax=st.session_state.nm_annual_tax,
                _ins=st.session_state.nm_annual_ins,
                _sqft=st.session_state.nm_sqft,
                _extra_principal=st.session_state.nm_prin,
                _prepay_periods=st.session_state.nm_prepay,
                _price=st.session_state.nm_price,
                _downpayment_amount=st.session_state.nm_downpayment
            )
        except Exception as e:
            st.error(f"Error updating new mortgage: {e}")