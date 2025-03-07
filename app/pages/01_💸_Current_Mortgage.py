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

###########################################################

# restore widget state

###########################################################

from src.utils.mortgage_utils import restore_current_mortgage_widget_values

restore_current_mortgage_widget_values()

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
        value=st.session_state.get("cm_rate") if "nm_rate" in st.session_state else 0.001,
        step=0.005,
        format="%0.3f",
        key="cm_rate",
    )
    

    balance = st.number_input(
        "**Current Loan Balance ($)**",
        min_value=0.0001,
        value=st.session_state.get("cm_balance",0.0001),
        step=1000.0,
        key="cm_balance",
    )
    

    origin = st.number_input(
        "**Original Loan Amount ($)**",
        min_value=0.0001,
        value=st.session_state.get("cm_origin",0.0001),
        step=1000.0,
        key="cm_origin",
    )
    

    start_date = st.date_input(
        "**Loan Start Date**",
        value=st.session_state.get("cm_start_date",datetime.now()),
        key="cm_start_date"
    )
    
# middle column

with col2:
    # add white space to push down visuals
    st.write("")

    sqft = st.number_input(
        "**Square Footage**", 
        min_value=0.0001,
        value=st.session_state.get("cm_sqft",0.0001), 
        step=100.0, 
        key="cm_sqft"
    )


    ppsqft = st.number_input(
        "**Price per Sqft ($)**", 
        min_value=0.0001,
        value=st.session_state.get("cm_ppsqft",0.0001), 
        step=1.0, 
        key="cm_ppsqft"
    )


    pmt = st.number_input(
        "**Total Monthly PMT ($)**", 
        min_value=0.0001,
        value=st.session_state.get("cm_pmt",0.0001), 
        step=50.0, 
        key="cm_pmt"
    )

    pmi = st.number_input(
        "**Current Monthly PMI ($)**", 
        min_value=0.0001,
        value=st.session_state.get("cm_pmi",0.0001), 
        step=10.0, 
        key="cm_pmi"
    )

    term = st.number_input(
        "**Loan Term (years)**", 
        min_value=1,
        value=st.session_state.get("cm_term",1),  
        key="cm_term"
    )
    

with col3:
    # add white space to push down visuals
    st.write("")

    # Tax section with toggle
    tax_col1, tax_col2 = st.columns([9, 8])

    is_monthly_tax = tax_col1.toggle(
        "Annual/Monthly",
        value=st.session_state.get("cm_is_monthly_tax",False),
        key="cm_is_monthly_tax"
    )

    if is_monthly_tax:
        monthly_tax = tax_col2.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0001,
            value=st.session_state.get("cm_tax_monthly",0.0001),
            step=10.0,
            key="cm_tax_monthly",
        )
        st.session_state.cm_tax_annual = st.session_state.cm_tax_monthly * 12
    else:
        annual_tax = tax_col2.number_input(
            "**Annual Tax ($)**",
            min_value=0.0001,
            value=st.session_state.get("cm_tax_annual",0.0001),
            step=10.0,
            key="cm_tax_annual",
        )
        st.session_state.cm_tax_monthly = st.session_state.cm_tax_annual / 12
    

    # Insurance section with toggle
    ins_col1, ins_col2 = st.columns([9, 8])

    is_monthly_ins = ins_col1.toggle(
        "Annual/Monthly",
        value=st.session_state.get("cm_is_monthly_ins",False), 
        key="cm_is_monthly_ins"
    )

    if is_monthly_ins:
        monthly_ins = ins_col2.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0001,
            value=st.session_state.get("cm_ins_monthly",0.0001),
            step=10.0,
            key="cm_ins_monthly",
        )
        st.session_state.cm_ins_annual = st.session_state.cm_ins_monthly * 12
    else:
        annual_ins = ins_col2.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0001,
            value=st.session_state.get("cm_ins_annual",0.0001),
            step=100.0,
            key="cm_ins_annual",
        )
        st.session_state.cm_ins_monthly = st.session_state.cm_ins_annual / 12

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=st.session_state.get("cm_prin",0.0),
        step=100.0,
        key="cm_prin",
    )

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=st.session_state.get("cm_prepay",0),
        step=1,
        key="cm_prepay",
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
        # Call the update function directly to create the mortgage object
        currentMort = CurrentMortgage(
            _rate=rate,
            _years=term,
            _tax=annual_tax,
            _ins=annual_ins,
            _sqft=sqft,
            _extra_principal=prin,
            _prepay_periods=prepay,
            _original_loan=origin,
            _loan_amount=balance,
            _start_date=start_date.strftime("%m/%d/%Y"),
            _price_per_sqft=ppsqft,
            _monthly_pmi=pmi,
            _total_pmt=pmt
        )
        if currentMort is not None:
            # Set the flag to show calculations
            st.session_state.show_current_mortgage_calcs = True

if st.session_state.show_current_mortgage_calcs:

    try:
        # Attempt to get the current mortgage object
        # Either from the local variable (if just calculated) or from session state (if returning to page)
        if 'currentMort' not in locals():
            if "current_mortgage" in st.session_state and st.session_state.current_mortgage is not None:
                currentMort = st.session_state.current_mortgage
            else:
                # No valid mortgage object found
                st.warning("Please click Calculate to update the metrics.")
                st.stop()  # Stop execution here to prevent errors

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

        # Save to session state for use in other pages
        st.session_state["current_mortgage"] = currentMort

        # Add this at the bottom of any page to debug
        if st.checkbox("Show session state debug info", key="debug_checkbox"):
            st.write(st.session_state)
    
    except NameError:
        st.warning("Please click Calculate to update the metrics.")
        st.stop()

st.write(st.session_state)