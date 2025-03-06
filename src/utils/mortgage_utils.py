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
        
        # Also save toggle states and other widget values that aren't directly in the mortgage object
        st.session_state.current_mortgage_widget_values = {
            "cm_is_monthly_tax": st.session_state.cm_is_monthly_tax,
            "cm_is_monthly_ins": st.session_state.cm_is_monthly_ins,
            "cm_rate": st.session_state.cm_rate,
            "cm_term": st.session_state.cm_term,
            "cm_sqft": st.session_state.cm_sqft,
            "cm_balance": st.session_state.cm_balance,
            "cm_origin": st.session_state.cm_origin,
            "cm_ppsqft": st.session_state.cm_ppsqft, 
            "cm_pmt": st.session_state.cm_pmt,
            "cm_pmi": st.session_state.cm_pmi,
            "cm_prin": st.session_state.cm_prin,
            "cm_prepay": st.session_state.cm_prepay,
            "cm_tax_annual": st.session_state.get("cm_tax_annual", 0),
            "cm_tax_monthly": st.session_state.get("cm_tax_monthly", 0),
            "cm_ins_annual": st.session_state.get("cm_ins_annual", 0),
            "cm_ins_monthly": st.session_state.get("cm_ins_monthly", 0),
            "cm_start_date": st.session_state.cm_start_date
        }
        
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
        
        # Also save toggle states and other widget values
        st.session_state.new_mortgage_widget_values = {
            "nm_is_monthly_tax": st.session_state.nm_is_monthly_tax,
            "nm_is_monthly_ins": st.session_state.nm_is_monthly_ins,
            "nm_is_not_percent": st.session_state.nm_is_not_percent,
            "nm_rate": st.session_state.nm_rate,
            "nm_term": st.session_state.nm_term,
            "nm_sqft": st.session_state.nm_sqft,
            "nm_price": st.session_state.nm_price,
            "nm_prin": st.session_state.nm_prin,
            "nm_prepay": st.session_state.nm_prepay,
            "nm_downpayment": st.session_state.get("nm_downpayment", 0),
            "nm_downpayment_percent": st.session_state.get("nm_downpayment_percent", 20),
            "nm_annual_tax": st.session_state.get("nm_annual_tax", 0),
            "nm_monthly_tax": st.session_state.get("nm_monthly_tax", 0),
            "nm_annual_ins": st.session_state.get("nm_annual_ins", 0),
            "nm_monthly_ins": st.session_state.get("nm_monthly_ins", 0),
            "nm_start_date": st.session_state.get("nm_start_date", None)
        }
        
    except Exception as e:
        st.error(f"Error updating new mortgage: {e}")

def restore_current_mortgage_widget_values():
    """
    Restore widget values for the current mortgage page from session state.
    Call this at the top of the current mortgage page.
    """
    if 'current_mortgage_widget_values' in st.session_state:
        widget_values = st.session_state.current_mortgage_widget_values
        
        # Dynamically update all saved widget values
        for key, value in widget_values.items():
            st.session_state[key] = value

def restore_new_mortgage_widget_values():
    """
    Restore widget values for the new mortgage page from session state.
    Call this at the top of the new mortgage page.
    """
    if 'new_mortgage_widget_values' in st.session_state:
        widget_values = st.session_state.new_mortgage_widget_values
        
        # Dynamically update all saved widget values
        for key, value in widget_values.items():
            st.session_state[key] = value