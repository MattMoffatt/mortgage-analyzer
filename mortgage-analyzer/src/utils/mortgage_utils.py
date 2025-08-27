import sys
from pathlib import Path
import streamlit as st
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario, RefinanceScenario

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

def current_mortgage_persistent_storage():

    # Initialize permanent storage if not already present
    if "cm_data" not in st.session_state:
        st.session_state.cm_data = {
            "rate": 4.5,
            "balance": 200000.0,
            "origin": 250000.0,
            "start_date": datetime.now(),  # Default to today
            "sqft": 2000.0,
            "ppsqft": 150.0,
            "pmt": 1500.0,
            "pmi": 100.0,
            "term": 30,
            "is_monthly_tax": False,
            "tax_annual": 2400.0,
            "tax_monthly": 200.0,
            "is_monthly_ins": False,
            "ins_annual": 1200.0,
            "ins_monthly": 100.0,
            "prin": 0.0,
            "prepay": 0
        }

    # Set temporary widget keys with values from permanent storage
    for key, value in st.session_state.cm_data.items():
        widget_key = f"temp_cm_{key}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = value

    # Always explicitly set toggle states to ensure they persist
    st.session_state["temp_cm_is_monthly_tax"] = st.session_state.cm_data["is_monthly_tax"]
    st.session_state["temp_cm_is_monthly_ins"] = st.session_state.cm_data["is_monthly_ins"]


def new_mortgage_persistent_storage():

    if "nm_data" not in st.session_state:
        st.session_state.nm_data = {
            "rate": 4.5,
            "price": 300000.0,
            "start_date": datetime.now(),  # Default to today
            "sqft": 2000.0,
            "term": 30,
            "prin": 0.0,
            "prepay": 0,
            "is_not_percent": False,
            "downpayment": 60000.0,
            "downpayment_percent": 20.0,
            "is_monthly_tax": False,
            "annual_tax": 3000.0,
            "monthly_tax": 250.0,
            "is_monthly_ins": False,
            "annual_ins": 1200.0,
            "monthly_ins": 100.0
        }

    # Set temporary widget keys with values from permanent storage
    for key, value in st.session_state.nm_data.items():
        widget_key = f"temp_nm_{key}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = value

    # Always explicitly set toggle states to ensure they persist
    st.session_state["temp_nm_is_not_percent"] = st.session_state.nm_data["is_not_percent"]
    st.session_state["temp_nm_is_monthly_tax"] = st.session_state.nm_data["is_monthly_tax"]
    st.session_state["temp_nm_is_monthly_ins"] = st.session_state.nm_data["is_monthly_ins"]

    # Ensure all related values are initialized
    if "temp_nm_downpayment" not in st.session_state:
        st.session_state["temp_nm_downpayment"] = st.session_state.nm_data["downpayment"]
    if "temp_nm_downpayment_percent" not in st.session_state:
        st.session_state["temp_nm_downpayment_percent"] = st.session_state.nm_data["downpayment_percent"]
    if "temp_nm_monthly_tax" not in st.session_state:
        st.session_state["temp_nm_monthly_tax"] = st.session_state.nm_data["monthly_tax"]
    if "temp_nm_annual_tax" not in st.session_state:
        st.session_state["temp_nm_annual_tax"] = st.session_state.nm_data["annual_tax"]
    if "temp_nm_monthly_ins" not in st.session_state:
        st.session_state["temp_nm_monthly_ins"] = st.session_state.nm_data["monthly_ins"]
    if "temp_nm_annual_ins" not in st.session_state:
        st.session_state["temp_nm_annual_ins"] = st.session_state.nm_data["annual_ins"]

def current_mortgage_run_calcs():
    for key in st.session_state.cm_data.keys():
        temp_key = f"temp_cm_{key}"
        if temp_key in st.session_state:
            st.session_state.cm_data[key] = st.session_state[temp_key]

    # Format the date properly
    if isinstance(st.session_state.cm_data['start_date'], datetime):
        start_date_formatted = st.session_state.cm_data['start_date'].strftime("%m/%d/%Y")
    else:
        start_date_formatted = st.session_state.cm_data['start_date'].strftime("%m/%d/%Y")

    # Call the update function directly to create the mortgage object
    currentMort = CurrentMortgage(
        _rate=st.session_state.cm_data['rate'],
        _years=st.session_state.cm_data['term'],
        _tax=st.session_state.cm_data['tax_annual'],
        _ins=st.session_state.cm_data['ins_annual'],
        _sqft=st.session_state.cm_data['sqft'],
        _extra_principal=st.session_state.cm_data['prin'],
        _prepay_periods=st.session_state.cm_data['prepay'],
        _original_loan=st.session_state.cm_data['origin'],
        _loan_amount=st.session_state.cm_data['balance'],
        _start_date=start_date_formatted,
        _price_per_sqft=st.session_state.cm_data['ppsqft'],
        _monthly_pmi=st.session_state.cm_data['pmi'],
        _total_pmt=st.session_state.cm_data['pmt']
    )
    
    if currentMort is not None:
        # Set the flag to show calculations
        st.session_state.show_current_mortgage_calcs = True
        # Store the mortgage object in session state
        st.session_state.current_mortgage = currentMort

def new_mortgage_run_calcs():
    for key in st.session_state.nm_data.keys():
        temp_key = f"temp_nm_{key}"
        if temp_key in st.session_state:
            st.session_state.nm_data[key] = st.session_state[temp_key]
            
    # Force recalculate downpayment based on percentage if using percentage mode
    if not st.session_state.nm_data["is_not_percent"]:
        st.session_state.nm_data["downpayment"] = (st.session_state.nm_data["downpayment_percent"] / 100) * st.session_state.nm_data["price"]
        # Also update temp value for display
        st.session_state["temp_nm_downpayment"] = st.session_state.nm_data["downpayment"]
    
    # Create mortgage object from permanent storage
    NewMort = NewMortgageScenario(
        _rate=st.session_state.nm_data["rate"],
        _years=st.session_state.nm_data["term"],
        _tax=st.session_state.nm_data["annual_tax"],
        _ins=st.session_state.nm_data["annual_ins"],
        _sqft=st.session_state.nm_data["sqft"],
        _extra_principal=st.session_state.nm_data["prin"],
        _prepay_periods=st.session_state.nm_data["prepay"],
        _price=st.session_state.nm_data["price"],
        _downpayment_amount=st.session_state.nm_data["downpayment"]
    )
    
    if NewMort is not None:
        # Set the flag to show calculations
        st.session_state.show_new_mortgage_calcs = True
        # Store the mortgage object in session state
        st.session_state.new_mortgage = NewMort


def refinance_persistent_storage():
    """Initialize persistent storage for refinance scenario data"""
    if "rf_data" not in st.session_state:
        # Get default values from current mortgage if available
        current_balance = 200000.0
        current_value = 300000.0
        current_sqft = 2000.0
        current_tax = 3000.0
        current_ins = 1200.0
        
        # Try to get values from current mortgage if it exists
        if "current_mortgage" in st.session_state and st.session_state.current_mortgage:
            cm = st.session_state.current_mortgage
            current_balance = cm.loan_amount
            current_value = cm.price
            current_sqft = cm.sqft
            current_tax = cm.tax
            current_ins = cm.ins
        
        st.session_state.rf_data = {
            "rate": 4.0,  # Typically refinancing for better rate
            "term": 30,
            "current_loan_balance": current_balance,
            "current_property_value": current_value,
            "cash_out_amount": 0.0,
            "closing_cost_percentage": 2.5,  # 2.5% default
            "sqft": current_sqft,
            "annual_tax": current_tax,
            "monthly_tax": current_tax / 12,
            "annual_ins": current_ins,
            "monthly_ins": current_ins / 12,
            "is_monthly_tax": False,
            "is_monthly_ins": False,
            "prin": 0.0,
            "prepay": 0
        }

    # Set temporary widget keys with values from permanent storage
    for key, value in st.session_state.rf_data.items():
        widget_key = f"temp_rf_{key}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = value

    # Always explicitly set toggle states to ensure they persist
    st.session_state["temp_rf_is_monthly_tax"] = st.session_state.rf_data["is_monthly_tax"]
    st.session_state["temp_rf_is_monthly_ins"] = st.session_state.rf_data["is_monthly_ins"]


def update_refinance_scenario():
    """Update the refinance scenario object in session state"""
    try:
        # Get tax amount based on toggle state
        if st.session_state.rf_is_monthly_tax:
            tax = st.session_state.rf_monthly_tax * 12
        else:
            tax = st.session_state.rf_annual_tax
            
        # Get insurance amount based on toggle state
        if st.session_state.rf_is_monthly_ins:
            insurance = st.session_state.rf_monthly_ins * 12
        else:
            insurance = st.session_state.rf_annual_ins
            
        # Create the refinance scenario object
        refinance_scenario = RefinanceScenario(
            _rate=st.session_state.rf_rate,
            _years=st.session_state.rf_term,
            _tax=tax,
            _ins=insurance,
            _sqft=st.session_state.rf_sqft,
            _extra_principal=st.session_state.rf_prin,
            _prepay_periods=st.session_state.rf_prepay,
            _current_loan_balance=st.session_state.rf_current_loan_balance,
            _current_property_value=st.session_state.rf_current_property_value,
            _cash_out_amount=st.session_state.rf_cash_out_amount,
            _closing_cost_percentage=st.session_state.rf_closing_cost_percentage / 100
        )
        
        # Save the object to session state
        st.session_state.refinance_scenario = refinance_scenario
        
        # Also save widget values
        st.session_state.refinance_widget_values = {
            "rf_is_monthly_tax": st.session_state.rf_is_monthly_tax,
            "rf_is_monthly_ins": st.session_state.rf_is_monthly_ins,
            "rf_rate": st.session_state.rf_rate,
            "rf_term": st.session_state.rf_term,
            "rf_current_loan_balance": st.session_state.rf_current_loan_balance,
            "rf_current_property_value": st.session_state.rf_current_property_value,
            "rf_cash_out_amount": st.session_state.rf_cash_out_amount,
            "rf_closing_cost_percentage": st.session_state.rf_closing_cost_percentage,
            "rf_sqft": st.session_state.rf_sqft,
            "rf_prin": st.session_state.rf_prin,
            "rf_prepay": st.session_state.rf_prepay,
            "rf_annual_tax": st.session_state.get("rf_annual_tax", 0),
            "rf_monthly_tax": st.session_state.get("rf_monthly_tax", 0),
            "rf_annual_ins": st.session_state.get("rf_annual_ins", 0),
            "rf_monthly_ins": st.session_state.get("rf_monthly_ins", 0)
        }
        
    except Exception as e:
        st.error(f"Error updating refinance scenario: {e}")


def refinance_run_calcs():
    """Run calculations for refinance scenario and store in session state"""
    # Update permanent storage from temporary widgets
    for key in st.session_state.rf_data.keys():
        temp_key = f"temp_rf_{key}"
        if temp_key in st.session_state:
            st.session_state.rf_data[key] = st.session_state[temp_key]
    
    # Create refinance scenario object
    RefinanceScen = RefinanceScenario(
        _rate=st.session_state.rf_data["rate"],
        _years=st.session_state.rf_data["term"],
        _tax=st.session_state.rf_data["annual_tax"],
        _ins=st.session_state.rf_data["annual_ins"],
        _sqft=st.session_state.rf_data["sqft"],
        _extra_principal=st.session_state.rf_data["prin"],
        _prepay_periods=st.session_state.rf_data["prepay"],
        _current_loan_balance=st.session_state.rf_data["current_loan_balance"],
        _current_property_value=st.session_state.rf_data["current_property_value"],
        _cash_out_amount=st.session_state.rf_data["cash_out_amount"],
        _closing_cost_percentage=st.session_state.rf_data["closing_cost_percentage"] / 100
    )
    
    if RefinanceScen is not None:
        # Set the flag to show calculations
        st.session_state.show_refinance_calcs = True
        # Store the scenario object in session state
        st.session_state.refinance_scenario = RefinanceScen

