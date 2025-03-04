import datetime as dt
import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import NewMortgageScenario

###########################################################

# Top of page

###########################################################

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;:star:&ensp;&ensp;&ensp;:green[**New Mortgage**]&ensp;&ensp;&ensp;:star:", divider="grey")

left, center, right = st.columns([6,18,6])

with left:

    pg1 = st.Page("pages/01_💸_Current_Mortgage.py") 

    if st.button("**💸 Current Mortgage**"):
        st.switch_page(pg1)

with right:

    pg3 = st.Page("pages/03_📈_Comparison.py")

    if st.button("**📈 Comparison**"):
        st.switch_page(pg3)


with center:
    
    st.write("Put in the details of the new mortgage you are evaluating to compare to your current mortgage.")

###########################################################

# Input Section

###########################################################    


col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 8, 0.5, 6]) # split into thre columns with two blank buffer columns in between

# left column

with col1:
    st.write("")
    st.write("")
    st.write("")

    rate = st.number_input(
        "**Interest Rate (%)**",
        min_value=0.0,
        value=st.session_state.nm_rate,
        step=0.005,
        format="%0.3f",
        key="nm_rate_input",
    )
    st.session_state.nm_rate = rate

    price = st.number_input(
        "**House Price ($)**",
        min_value=0.0,
        value=st.session_state.nm_price,
        step=1000.0,
        key="nm_price_input",
    )
    st.session_state.nm_price = price

    start_date = st.date_input(
        "**Loan Start Date**", 
        value=st.session_state.nm_start_date, 
        key="nm_start_date_input"
    )
    st.session_state.nm_start_date = start_date

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=st.session_state.nm_prin,
        step=100.0,
        key="nm_prin_input",
    )
    st.session_state.nm_prin = prin

# middle column

with col2:
    st.write("")
    st.write("")
    st.write("")

    sqft = st.number_input(
        "**Square Footage**", 
        min_value=0.0, 
        value=st.session_state.nm_sqft, 
        step=100.0, 
        key="nm_sqft_input"
    )
    st.session_state.nm_sqft = sqft

    pmi = st.number_input(
        "**Current Monthly PMI ($)**", 
        min_value=0.0, 
        value=st.session_state.nm_pmi, 
        step=10.0, 
        key="nm_pmi_input"
    )
    st.session_state.nm_pmi = pmi

    term = st.number_input(
        "**Loan Term (years)**", 
        min_value=0, 
        value=st.session_state.nm_term, 
        key="nm_term_input"
    )
    st.session_state.nm_term = term

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=st.session_state.nm_prepay,
        step=1,
        key="nm_prepay_input",
    )
    st.session_state.nm_prepay = prepay

# right column

with col3:

    is_not_percent = st.toggle(
        "% / $", 
        value=st.session_state.nm_is_not_percent, 
        key="nm_is_not_percent_input"
    )
    st.session_state.nm_is_not_percent = is_not_percent

    if is_not_percent:
        downpayment = st.number_input(
            "**Downpayment Amount ($)**",
            min_value=0.0,
            value=st.session_state.nm_downpayment,
            step=1000.0,
            key="nm_downpayment_input",
        )
        st.session_state.nm_downpayment = downpayment
    else:
        downpayment_percent = st.number_input(
            "**Downpayment (%)**",
            min_value=0.0,
            value=st.session_state.nm_downpayment_percent,
            step=1.0,
            key="nm_downpayment_percent_input"
        )
        st.session_state.nm_downpayment_percent = downpayment_percent
        st.session_state.nm_downpayment = (st.session_state.nm_downpayment_percent / 100) * st.session_state.nm_price
        
    # Tax section with toggle
    is_monthly_tax = st.toggle(
        "Annual/Monthly", 
        value=st.session_state.nm_is_monthly_tax,
        key="nm_is_monthly_tax_input"
    )
    st.session_state.nm_is_monthly_tax = is_monthly_tax

    if is_monthly_tax:
        monthly_tax = st.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0,
            value=st.session_state.nm_monthly_tax,
            step=10.0,
            key="nm_monthly_tax_input",
        )
        st.session_state.nm_monthly_tax = monthly_tax
        tax = monthly_tax * 12  # Convert to annual for consistency
    else:
        tax = st.number_input(
            "**Annual Tax ($)**",
            min_value=0.0,
            value=st.session_state.nm_annual_tax,
            step=100.0,
            key="nm_annual_tax_input",
        )
        st.session_state.nm_annual_tax = tax

    # Insurance section with toggle
    is_monthly_ins = st.toggle(
        "Annual/Monthly",
        value=st.session_state.nm_is_monthly_tax,
        key="nm_is_monthly_ins_input"
    )

    if is_monthly_ins:
        monthly_ins = st.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0,
            value=st.session_state.nm_monthly_ins,
            step=10.0,
            key="nm_monthly_ins_input",
        )
        st.session_state.nm_monthly_ins = monthly_ins
        insurance = monthly_ins * 12  # Convert to annual for consistency
    else:
        insurance = st.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0,
            value=st.session_state.nm_annual_ins,
            step=100.0,
            key="nm_annual_ins_input",
        )
        st.session_state.nm_annual_ins = insurance


NewMort = NewMortgageScenario(
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

###########################################################

# Display Metrics Section

###########################################################

buff3, mid, buff4 = st.columns([6, 18, 6])

with mid:
    st.write("")

    st.header("&ensp;:green[**Mortgage Calculations**]")


loan_col, payment_col = st.columns([6,6])

with loan_col: 

    st.subheader("**&ensp;&ensp;&ensp;&ensp;&ensp;Loan Metrics:**",divider="green")

    st.metric(
        "**Loan Amount Today:**",
        value=f"${NewMort.loan_amount:,.2f}"
    )

    st.metric(
        "**Value in 5 Years (3% annual growth):**",
        value=f"${NewMort.estimate_value_at_year(5):,.2f}",
        delta=F"${(NewMort.estimate_value_at_year(5) - NewMort.price):,.2f}",
        delta_color="normal"
    )

    st.metric(
        "**Value in 10 Years (3% annual growth):**",
        value=f"${NewMort.estimate_value_at_year(10):,.2f}",
        delta=F"${(NewMort.estimate_value_at_year(10) - NewMort.price):,.2f}",
        delta_color="normal"
    )

    # st.write(f"#### **Loan Amount**: :green[${NewMort.loan_amount:,.2f}]")
    # st.write(
    #     f"#### **Principal & Interest**: :green[${NewMort.principal_and_interest:,.2f}]"
    # )

with payment_col:

    st.subheader("**&ensp;&ensp;&ensp;&ensp;&ensp;Payment Metrics:**",divider="green")

    st.metric(
        "**Total Monthly Payment:**",
        value=f"${NewMort.total_pmt:,.2f}"
    )

    st.metric(
        "**Estimated Monthly PMI:**",
        value=f"${NewMort.monthly_pmi:,.2f}"
    )
    
    st.metric(
        "**Months of PMI payments:**",
        value=f"{NewMort.pmi_periods_remaining()}"
    )

    # st.write(f"#### **Expected PMI**: :green[${NewMort.monthly_pmi:,.2f}]")
    # st.write(f"#### **Total Monthly Payment**: :green[${NewMort.total_pmt:,.2f}]")

# Save to session state for use in other pages
st.session_state["new_mortgage"] = NewMort

# st.write(st.session_state)
