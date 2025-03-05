import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario

def update_current_mortgage():
    """
    Update the current_mortgage object in session state with latest widget values.
    Called automatically when navigating away from the Current Mortgage page.
    """
    try:
        # Create the mortgage object directly from widget values
        # No need to reference st.session_state for the values - they're already updated
        # by the widgets themselves
        current_mortgage = CurrentMortgage(
            _rate=st.session_state.cm_rate,
            _years=st.session_state.cm_term,
            _tax=st.session_state.cm_tax_annual if not st.session_state.cm_is_monthly_tax else st.session_state.cm_tax_monthly * 12,
            _ins=st.session_state.cm_ins_annual if not st.session_state.cm_is_monthly_ins else st.session_state.cm_ins_monthly * 12,
            _sqft=st.session_state.cm_sqft,
            _extra_principal=st.session_state.cm_prin,
            _prepay_periods=st.session_state.cm_prepay,
            _original_loan=st.session_state.cm_origin,
            _loan_amount=st.session_state.cm_balance,
            _start_date=st.session_state.cm_start_date.strftime("%m/%d/%Y"),
            _price_per_sqft=st.session_state.cm_ppsqft,
            _monthly_pmi=st.session_state.cm_pmi,
            _total_pmt=st.session_state.cm_pmt
        )
        # Save the object to session state
        st.session_state.current_mortgage = current_mortgage
    except Exception as e:
        st.error(f"Error updating current mortgage: {e}")

def update_new_mortgage():
    """
    Update the new_mortgage object in session state with latest widget values.
    Called automatically when navigating away from the New Mortgage page.
    """
    try:
        # Get the downpayment amount based on toggle state
        if st.session_state.nm_is_not_percent:
            # Use direct amount
            downpayment = st.session_state.nm_downpayment
        else:
            # Calculate from percentage
            downpayment = (st.session_state.nm_downpayment_percent / 100) * st.session_state.nm_price
            
        # Get tax amount based on toggle state
        if st.session_state.nm_is_monthly_tax:
            tax = st.session_state.nm_monthly_tax * 12
        else:
            tax = st.session_state.nm_annual_tax
            
        # Get insurance amount based on toggle state
        if st.session_state.nm_is_monthly_ins:
            insurance = st.session_state.nm_monthly_ins * 12
        else:
            insurance = st.session_state.nm_annual_ins
            
        # Create the mortgage object
        new_mortgage = NewMortgageScenario(
            _rate=st.session_state.nm_rate,
            _years=st.session_state.nm_term,
            _tax=tax,
            _ins=insurance,
            _sqft=st.session_state.nm_sqft,
            _extra_principal=st.session_state.nm_prin,
            _prepay_periods=st.session_state.nm_prepay,
            _price=st.session_state.nm_price,
            _downpayment_amount=downpayment
        )
        # Save the object to session state
        st.session_state.new_mortgage = new_mortgage
    except Exception as e:
        st.error(f"Error updating new mortgage: {e}")