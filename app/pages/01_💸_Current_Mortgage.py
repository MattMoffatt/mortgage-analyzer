
import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario


###########################################################

# Set session and navigation functionality
# Needed for persisting data across pages

###########################################################


# Track which page we're on
if "current_page" not in st.session_state:
    st.session_state.current_page = None

# Define update function for Current Mortgage page
def update_current_mortgage():
    if st.session_state.current_page == "current_mortgage":
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
            _start_date=st.session_state.cm_start_date.strftime("%m/%d/%Y"),
            _price_per_sqft=st.session_state.cm_ppsqft,
            _monthly_pmi=st.session_state.cm_pmi,
            _total_pmt=st.session_state.cm_pmt
        )
    
def update_new_mortgage():
    if st.session_state.current_page == "new_mortgage":
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
        
# Register these functions to run when navigating away
if "on_page_exit" not in st.session_state:
    st.session_state.on_page_exit = {
        "current_mortgage": update_current_mortgage,
        "new_mortgage": update_new_mortgage
    }

# Set current page flag
# In Current Mortgage page:
st.session_state.current_page = "current_mortgage"



###########################################################

# Top of page

###########################################################

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;:house:&ensp;&ensp;&ensp;:violet[**Current Mortgage**]&ensp;&ensp;&ensp;:house:", divider="grey")

left, center, right = st.columns([6,18,6])

with left:

    home = st.Page("pages/00_🏡_Home_Page_(pun_intended).py")

    if st.button("**🏡 Home Page (pun intended)**"):
        st.switch_page(home)

with right:

    pg2 = st.Page("pages/02_🆕_New_Scenario.py") 

    if st.button("**🆕 New Scenario**"):
        st.switch_page(pg2)


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
        min_value=0.0,
        value=st.session_state.cm_rate,
        step=0.005,
        format="%0.3f",
        key="cm_rate",
    )
    

    balance = st.number_input(
        "**Current Loan Balance ($)**",
        min_value=0.0,
        value=st.session_state.cm_balance,
        step=1000.0,
        key="cm_balance",
    )
    

    origin = st.number_input(
        "**Original Loan Amount ($)**",
        min_value=0.0,
        value=st.session_state.cm_origin,
        step=1000.0,
        key="cm_origin",
    )
    

    start_date = st.date_input(
        "**Loan Start Date**",
        value=st.session_state.cm_start_date, 
        key="cm_start_date"
    )
    
# middle column

with col2:
    # add white space to push down visuals
    st.write("")

    sqft = st.number_input(
        "**Square Footage**", 
        min_value=0.0, 
        value=st.session_state.cm_sqft,
        step=100.0, 
        key="cm_sqft"
    )


    ppsqft = st.number_input(
        "**Price per Sqft ($)**", 
        min_value=0.0,
        value=st.session_state.cm_ppsqft, 
        step=1.0, 
        key="cm_ppsqft"
    )


    pmt = st.number_input(
        "**Total Monthly PMT ($)**", 
        min_value=0.0, 
        value=st.session_state.cm_pmt,
        step=50.0, 
        key="cm_pmt"
    )

    pmi = st.number_input(
        "**Current Monthly PMI ($)**", 
        min_value=0.0, 
        value=st.session_state.cm_pmi,
        step=10.0, 
        key="cm_pmi"
    )

    term = st.number_input(
        "**Loan Term (years)**", 
        min_value=0, 
        value=st.session_state.cm_term,
        key="cm_term"
    )
    

with col3:
    # add white space to push down visuals
    st.write("")

    # Tax section with toggle
    tax_col1, tax_col2 = st.columns([9, 8])

    is_monthly_tax = tax_col1.toggle(
        "Annual/Monthly",
        value=st.session_state.cm_is_monthly_tax, 
        key="cm_is_monthly_tax_flag"
    )

    if is_monthly_tax:
        monthly_tax = tax_col2.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0,
            value=st.session_state.cm_tax_monthly,
            step=10.0,
            key="cm_tax_monthly",
        )
        st.session_state.cm_tax_annual = st.session_state.cm_tax_monthly * 12
    else:
        annual_tax = tax_col2.number_input(
            "**Annual Tax ($)**",
            min_value=0.0,
            value=st.session_state.cm_tax_annual,
            step=10.0,
            key="cm_tax_annual",
        )
        st.session_state.cm_tax_monthly = st.session_state.cm_tax_annual / 12
    

    # Insurance section with toggle
    ins_col1, ins_col2 = st.columns([9, 8])

    is_monthly_ins = ins_col1.toggle(
        "Annual/Monthly", 
        value=st.session_state.cm_is_monthly_ins,
        key="cm_is_monthly_ins_flag"
    )

    if is_monthly_ins:
        monthly_ins = ins_col2.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0,
            value=st.session_state.cm_ins_monthly,
            step=10.0,
            key="cm_ins_monthly",
        )
        st.session_state.cm_ins_annual = st.session_state.cm_ins_monthly * 12
    else:
        annual_ins = ins_col2.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0,
            value=st.session_state.cm_ins_annual,
            step=100.0,
            key="cm_ins_annual",
        )
        st.session_state.cm_ins_monthly = st.session_state.cm_ins_annual / 12

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=st.session_state.cm_prin,
        step=100.0,
        key="cm_prin",
    )

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=st.session_state.cm_prepay,
        step=1,
        key="cm_prepay",
    )

# inputs get saved into CurrentMortgage class for later comparison
currentMort = CurrentMortgage(
    _rate=st.session_state.cm_rate,
    _years=st.session_state.cm_term,
    _tax=st.session_state.cm_tax_annual,
    _ins=st.session_state.cm_ins_annual,
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

###########################################################

# Display Metrics Section

###########################################################

buff3, mid, buff4 = st.columns([6, 18, 6])

# # attempt at center justification...
# with mid:
#     st.write("")
#     # Display mortgage details
#     st.write("## &ensp;:violet[**Mortgage Calcs**]")

with mid:
    st.write("")

    st.header("&ensp;&ensp;:violet[**Mortgage Calculations**]")


values, ratios, time = st.columns([3, 3, 3])   

with values:
    
    st.subheader("&ensp;Value Metrics", divider="violet")

    st.metric(
        "**Current Value:**",
        value=f"${currentMort.price:,.2f}"
    )

    st.metric(
        "**Current Equity:**",
        value=f"${currentMort.equity_value:,.2f}"
    )

    st.metric(
        "**Value in 5 Years (3% annual growth):**",
        value=f"${currentMort.estimate_value_at_year(5):,.2f}",
        delta=f"${(currentMort.estimate_value_at_year(5) - currentMort.price):,.2f}"
    )


with ratios:

    st.subheader("&ensp;Ratio Metrics", divider="violet")

    st.metric(
        "**Loan to Value Ratio:**",
        value=f"{currentMort.loan_to_value:.2%}"
    )

    st.metric(
        "**Equity Ratio:**",
        value=f"{(1-currentMort.loan_to_value):.2%}"
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

# Save to session state for use in other pages
st.session_state["current_mortgage"] = currentMort

# st.write(st.session_state)
