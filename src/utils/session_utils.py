import streamlit as st
import datetime as dt
from typing import Any, Dict

def initialize_session_state(defaults: Dict[str, Any]):
    """
    Initialize session state variables only if they don't already exist.
    
    Args:
        defaults: Dictionary of variable names and their default values
    """
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def initialize_mortgage_app_state():
    """Initialize all session state variables needed for the mortgage app."""
    # Mortgage objects
    initialize_session_state({
        "current_mortgage": None,
        "new_mortgage": None
    })
    
    # Current Mortgage inputs
    initialize_session_state({
        "cm_rate": 5.5,
        "cm_balance": 300000.0,
        "cm_origin": 350000.0,
        "cm_start_date": dt.datetime.now(),
        "cm_sqft": 2000.0,
        "cm_ppsqft": 170.0,
        "cm_pmt": 1500.0,
        "cm_pmi": 50.0,
        "cm_term": 30,
        "cm_is_monthly_tax": False,
        "cm_tax_annual": 2600.0,
        "cm_is_monthly_ins": False,
        "cm_ins_annual": 2200.0,
        "cm_prin": 0.0,
        "cm_prepay": 0
    })
    
    # Only calculate these if they're not already set
    if "cm_tax_monthly" not in st.session_state:
        st.session_state.cm_tax_monthly = st.session_state.cm_tax_annual / 12
        
    if "cm_ins_monthly" not in st.session_state:
        st.session_state.cm_ins_monthly = st.session_state.cm_ins_annual / 12
    
    # New Mortgage inputs
    initialize_session_state({
        "nm_rate": 5.5,
        "nm_price": 300000.0,
        "nm_start_date": dt.datetime.now(),
        "nm_sqft": 2000.0,
        "nm_pmi": 50.0,
        "nm_term": 30,
        "nm_is_not_percent": False,
        "nm_downpayment_percent": 20.0,
        "nm_is_monthly_tax": False,
        "nm_annual_tax": 2600.0,
        "nm_is_monthly_ins": False,
        "nm_annual_ins": 2200.0,
        "nm_prin": 0.0,
        "nm_prepay": 0
    })
    
    # Only calculate these if they're not already set
    if "nm_downpayment" not in st.session_state:
        st.session_state.nm_downpayment = st.session_state.nm_price * 0.20
        
    if "nm_monthly_tax" not in st.session_state:
        st.session_state.nm_monthly_tax = st.session_state.nm_annual_tax / 12
        
    if "nm_monthly_ins" not in st.session_state:
        st.session_state.nm_monthly_ins = st.session_state.nm_annual_ins / 12