import sys
from pathlib import Path
from datetime import datetime 

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import CurrentMortgage

# Import your utility functions
from src.utils.navigation_utils import register_page, safe_navigate
from src.utils.mortgage_utils import update_current_mortgage

# Import your visualization functions
from src.visualizations.mortgage_charts import (
        create_single_mortgage_amortization_chart,
        create_interest_principal_ratio_chart,
        create_mortgage_timeline_chart,
        create_equity_growth_chart 
    )

###########################################################

# Initialize persistent storage

###########################################################

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

###########################################################

# Set session and navigation functionality
# Needed for persisting data across pages

###########################################################

register_page("current_mortgage", update_current_mortgage)

###########################################################

# Top of page

###########################################################

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;:house:&ensp;&ensp;&ensp;:violet[**Current Mortgage**]&ensp;&ensp;&ensp;:house:", divider="grey")

left, center, right = st.columns([6,18,6])

with left:
    home = st.Page("pages/00_🏡_Home_Page_(pun_intended).py")
    if st.button("**🏡 Home Page (pun intended)**", key="current_mortgage_to_home"):
        safe_navigate(home)

with right:
    pg2 = st.Page("pages/02_🆕_New_Scenario.py") 
    if st.button("**🆕 New Scenario**", key="current_mortgage_to_new_mortgage"):
        safe_navigate(pg2)

with center:
    st.write("Current mortgage details will be used to calculate comparisons to the new mortgage scenarios you are reviewing\
           and give details regarding current current metrics.")
    
###########################################################

# Helper functions

###########################################################

def update_cm_data(field):
    """Update permanent storage from temporary widget state"""
    st.session_state.cm_data[field] = st.session_state[f"temp_cm_{field}"]

def update_tax_values(source):
    """Update both annual and monthly tax values based on source"""
    if source == "monthly":
        # User changed monthly value, update annual
        st.session_state.cm_data["tax_monthly"] = st.session_state["temp_cm_tax_monthly"]
        st.session_state.cm_data["tax_annual"] = st.session_state.cm_data["tax_monthly"] * 12
        # Update the temporary value as well
        st.session_state["temp_cm_tax_annual"] = st.session_state.cm_data["tax_annual"]
    else:
        # User changed annual value, update monthly
        st.session_state.cm_data["tax_annual"] = st.session_state["temp_cm_tax_annual"]
        st.session_state.cm_data["tax_monthly"] = st.session_state.cm_data["tax_annual"] / 12
        # Update the temporary value as well
        st.session_state["temp_cm_tax_monthly"] = st.session_state.cm_data["tax_monthly"]

def update_insurance_values(source):
    """Update both annual and monthly insurance values based on source"""
    if source == "monthly":
        # User changed monthly value, update annual
        st.session_state.cm_data["ins_monthly"] = st.session_state["temp_cm_ins_monthly"]
        st.session_state.cm_data["ins_annual"] = st.session_state.cm_data["ins_monthly"] * 12
        # Update the temporary value as well
        st.session_state["temp_cm_ins_annual"] = st.session_state.cm_data["ins_annual"]
    else:
        # User changed annual value, update monthly
        st.session_state.cm_data["ins_annual"] = st.session_state["temp_cm_ins_annual"]
        st.session_state.cm_data["ins_monthly"] = st.session_state.cm_data["ins_annual"] / 12
        # Update the temporary value as well
        st.session_state["temp_cm_ins_monthly"] = st.session_state.cm_data["ins_monthly"]

###########################################################

# Input Section

###########################################################

col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 5, 0.5, 9]) # split into thre columns with two blank buffer columns in between

# Left column
with col1:
    # add white space to push down visuals
    st.write("")

    rate = st.number_input(
        "**Interest Rate (%)**",
        min_value=0.0001,
        step=0.005,
        format="%0.3f",
        key="temp_cm_rate",
        on_change=lambda: update_cm_data("rate")
    )
    
    balance = st.number_input(
        "**Current Loan Balance ($)**",
        min_value=0.0001,
        step=1000.0,
        key="temp_cm_balance",
        on_change=lambda: update_cm_data("balance")
    )
    
    origin = st.number_input(
        "**Original Loan Amount ($)**",
        min_value=0.0001,
        step=1000.0,
        key="temp_cm_origin",
        on_change=lambda: update_cm_data("origin")
    )
    
    start_date = st.date_input(
        "**Loan Start Date**",
        key="temp_cm_start_date",
        on_change=lambda: update_cm_data("start_date")
    )
    
# middle column
with col2:
    # add white space to push down visuals
    st.write("")

    sqft = st.number_input(
        "**Square Footage**", 
        min_value=0.0001,
        step=100.0, 
        key="temp_cm_sqft",
        on_change=lambda: update_cm_data("sqft")
    )

    ppsqft = st.number_input(
        "**Price per Sqft ($)**", 
        min_value=0.0001,
        step=1.0, 
        key="temp_cm_ppsqft",
        on_change=lambda: update_cm_data("ppsqft")
    )

    pmt = st.number_input(
        "**Total Monthly PMT ($)**", 
        min_value=0.0001,
        step=50.0, 
        key="temp_cm_pmt",
        on_change=lambda: update_cm_data("pmt")
    )

    pmi = st.number_input(
        "**Current Monthly PMI ($)**", 
        min_value=0.0001,
        step=10.0, 
        key="temp_cm_pmi",
        on_change=lambda: update_cm_data("pmi")
    )

    term = st.number_input(
        "**Loan Term (years)**", 
        min_value=1,
        key="temp_cm_term",
        on_change=lambda: update_cm_data("term")
    )
    
# right column
with col3:
    # add white space to push down visuals
    st.write("")

    # Tax section with toggle
    tax_col1, tax_col2 = st.columns([9, 8])

    is_monthly_tax = tax_col1.toggle(
        "Annual/Monthly",
        key="temp_cm_is_monthly_tax",
        on_change=lambda: update_cm_data("is_monthly_tax")
    )

    if is_monthly_tax:
        monthly_tax = tax_col2.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0001,
            step=10.0,
            key="temp_cm_tax_monthly",
            on_change=lambda: update_tax_values("monthly")
        )
        # Set both values to ensure they stay in sync
        annual_tax = st.session_state["temp_cm_tax_monthly"] * 12
        st.session_state.cm_data["tax_annual"] = annual_tax
    else:
        annual_tax = tax_col2.number_input(
            "**Annual Tax ($)**",
            min_value=0.0001,
            step=10.0,
            key="temp_cm_tax_annual",
            on_change=lambda: update_tax_values("annual")
        )
        # Set both values to ensure they stay in sync
        monthly_tax = st.session_state["temp_cm_tax_annual"] / 12
        st.session_state.cm_data["tax_monthly"] = monthly_tax

    # Insurance section with toggle
    ins_col1, ins_col2 = st.columns([9, 8])

    is_monthly_ins = ins_col1.toggle(
        "Annual/Monthly",
        key="temp_cm_is_monthly_ins",
        on_change=lambda: update_cm_data("is_monthly_ins")
    )

    if is_monthly_ins:
        monthly_ins = ins_col2.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0001,
            step=10.0,
            key="temp_cm_ins_monthly",
            on_change=lambda: update_insurance_values("monthly")
        )
        # Set both values to ensure they stay in sync
        annual_ins = st.session_state["temp_cm_ins_monthly"] * 12
        st.session_state.cm_data["ins_annual"] = annual_ins
    else:
        annual_ins = ins_col2.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0001,
            step=100.0,
            key="temp_cm_ins_annual",
            on_change=lambda: update_insurance_values("annual")
        )
        # Set both values to ensure they stay in sync
        monthly_ins = st.session_state["temp_cm_ins_annual"] / 12
        st.session_state.cm_data["ins_monthly"] = monthly_ins

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        step=100.0,
        key="temp_cm_prin",
        on_change=lambda: update_cm_data("prin")
    )

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        step=1,
        key="temp_cm_prepay",
        on_change=lambda: update_cm_data("prepay")
    )

###########################################################

# Display Metrics Section

###########################################################

st.write("")
calc_col1, calc_col2, calc_col3 = st.columns([4, 2, 4])

with calc_col2:
    # Initialize calculation flag if it doesn't exist
    if "show_current_mortgage_calcs" not in st.session_state:
        st.session_state.show_current_mortgage_calcs = False
        
    if st.button("**Calculate**", key="calculate_current_mortgage"):
        # Update all data from temp widgets to permanent storage
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

metrics, amort, growth, interest_breakdown, timeline = st.tabs(["Calculations","Amortization","Equity Growth","Interest Analysis","Mortgage Timeline"])

# Rest of the code for tabs remains unchanged
with metrics:
    if st.session_state.show_current_mortgage_calcs:
        try:
            # Attempt to get the current mortgage object
            if 'currentMort' not in locals():
                if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                    currentMort = st.session_state.current_mortgage
                else:
                    st.warning("Please click Calculate to update the metrics.")
                    st.stop()

            buff3, mid, buff4 = st.columns([6, 18, 6])
            with mid:
                st.write("")
                st.header("&ensp;&ensp;:violet[**Mortgage Calculations**]")

            values, ratios, time = st.columns([3, 3, 3])   
            with values:
                st.subheader("&ensp;Value Metrics", divider="violet")
                st.metric(
                    "**Current Value:**",
                    value=f"${max(currentMort.price,0):,.2f}"
                )
                st.metric(
                    "**Current Equity:**",
                    value=f"${max(currentMort.equity_value,0):,.2f}"
                )
                st.metric(
                    "**Value in 5 Years (3% annual growth):**",
                    value=f"${max(currentMort.estimate_value_at_year(5),0):,.2f}",
                    delta=f"${max((currentMort.estimate_value_at_year(5) - currentMort.price),0):,.2f}"
                )

            with ratios:
                st.subheader("&ensp;Ratio Metrics", divider="violet")
                st.metric(
                    "**Loan to Value Ratio:**",
                    value="N/A" if currentMort.loan_to_value > 100 else f"{currentMort.loan_to_value:.2%}"
                )
                st.metric(
                    "**Equity Ratio:**",
                    value="N/A" if currentMort.loan_to_value > 100 else f"{(1-currentMort.loan_to_value):.2%}"
                )

            with time:
                st.subheader("&ensp;Time Metrics", divider="violet")
                st.metric(
                    "**Loan End Date:**",
                    value=f"{currentMort.end_date}"
                )
                st.metric(
                    "**Pay Periods Left:**",
                    value=f"{currentMort.periods_remaining}"
                )
                st.metric(
                    "**PMI Periods Remaining:**",
                    value=f"{currentMort.pmi_periods_remaining()}"
                )
        
        except NameError:
            st.warning("Please click Calculate to update the metrics.")
            st.stop()

# The rest of your code for other tabs remains unchanged...
with amort:
    if st.session_state.show_current_mortgage_calcs:
        try:
            if 'currentMort' not in locals():
                if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                    currentMort = st.session_state.current_mortgage
                else:
                    st.warning("Please click Calculate to update the metrics.")
                    st.stop()
            create_single_mortgage_amortization_chart(currentMort)
        except NameError:
            st.warning("Please click Calculate to update the metrics.")
            st.stop()

with growth:
    if st.session_state.show_current_mortgage_calcs:
        try:
            if 'currentMort' not in locals():
                if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                    currentMort = st.session_state.current_mortgage
                else:
                    st.warning("Please click Calculate to update the metrics.")
                    st.stop()
            create_equity_growth_chart(currentMort)
        except NameError:
            st.warning("Please click Calculate to update the metrics.")
            st.stop()

with interest_breakdown:
    if st.session_state.show_current_mortgage_calcs:
        try:
            if 'currentMort' not in locals():
                if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                    currentMort = st.session_state.current_mortgage
                else:
                    st.warning("Please click Calculate to update the metrics.")
                    st.stop()
            create_interest_principal_ratio_chart(currentMort)
        except NameError:
            st.warning("Please click Calculate to update the metrics.")
            st.stop()

with timeline:
    if st.session_state.show_current_mortgage_calcs:
        try:
            if 'currentMort' not in locals():
                if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                    currentMort = st.session_state.current_mortgage
                else:
                    st.warning("Please click Calculate to update the metrics.")
                    st.stop()
            create_mortgage_timeline_chart(currentMort)
        except NameError:
            st.warning("Please click Calculate to update the metrics.")
            st.stop()