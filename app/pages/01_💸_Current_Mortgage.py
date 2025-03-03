import datetime as dt
import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import CurrentMortgage

left, center, right = st.columns([2,10,1])

center.write("# :violet[**Current Mortgage Details**]")

center.write("Current mortgage details will be used to calculate comparisons to the new mortgage scenarios you are reviewing.")


col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 5, 0.5, 9])

with col1:
    st.write("")
    st.write("")
    st.write("")
    rate = st.number_input(
        "**Interest Rate (%)**",
        min_value=0.0,
        value=5.5,
        step=0.005,
        format="%0.3f",
        key="rate1",
    )
    balance = st.number_input(
        "**Current Loan Balance ($)**",
        min_value=0.0,
        value=300000.0,
        step=1000.0,
        key="balance1",
    )
    origin = st.number_input(
        "**Original Loan Amount ($)**",
        min_value=0.0,
        value=350000.0,
        step=1000.0,
        key="origin1",
    )
    start_date = st.date_input(
        "**Loan Start Date**", value=dt.datetime.now(), key="start1"
    )

with col2:
    st.write("")
    st.write("")
    st.write("")
    sqft = st.number_input(
        "**Square Footage**", min_value=0.0, value=2000.0, step=100.0, key="sqft1"
    )
    ppsqft = st.number_input(
        "**Price per Sqft ($)**", min_value=0.0, value=170.0, step=1.0, key="ppsqft1"
    )
    pmt = st.number_input(
        "**Total Monthly PMT ($)**", min_value=0.0, value=1500.0, step=50.0, key="pmt1"
    )
    pmi = st.number_input(
        "**Current Monthly PMI ($)**", min_value=0.0, value=50.0, step=10.0, key="pmi1"
    )
    term = st.number_input("**Loan Term (years)**", min_value=0, value=30, key="term1")

with col3:
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Tax section with toggle
    tax_col1, tax_col2 = st.columns([9, 8])
    is_annual_tax = tax_col1.toggle("Annual/Monthly", key="taxtoggle1", value=True)

    if is_annual_tax:
        tax = tax_col2.number_input(
            "**Annual Tax ($)**",
            min_value=0.0,
            value=2600.0,
            step=100.0,
            key="tax1_annual",
        )
    else:
        monthly_tax = tax_col2.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0,
            value=216.67,
            step=10.0,
            key="tax1_monthly",
        )
        tax = monthly_tax * 12  # Convert to annual for consistency

    # Insurance section with toggle
    ins_col1, ins_col2 = st.columns([9, 8])
    is_annual_ins = ins_col1.toggle("Annual/Monthly", key="instoggle1", value=True)

    if is_annual_ins:
        insurance = ins_col2.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0,
            value=2200.0,
            step=100.0,
            key="insurance1_annual",
        )
    else:
        monthly_ins = ins_col2.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0,
            value=183.33,
            step=10.0,
            key="insurance1_monthly",
        )
        insurance = monthly_ins * 12  # Convert to annual for consistency

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=0.0,
        step=100.0,
        key="prin1",
    )

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=0,
        step=1,
        key="prepay1",
    )

currentMort = CurrentMortgage(
    _rate=rate,
    _years=term,
    _tax=tax,
    _ins=insurance,
    _sqft=sqft,
    _extra_principal=prin,
    _prepay_periods=prepay,
    _original_loan=origin,
    _loan_amount=balance,
    _start_date=start_date.strftime("%m/%d/%Y"),
    _price_per_sqft=ppsqft,
    _monthly_pmi=pmi,
    _total_pmt=pmt,
)

buff3, mid, buff4 = st.columns([4, 11, 1])

with mid:
    st.write("")
    st.write("")
    # Display mortgage details
    st.write("## :violet[**Mortgage Calcs**]")
    st.write(
        f"### **Principal & Interest**: :green[${currentMort.principal_and_interest:,.2f}]"
    )
    st.write(f"### **Current House Value**: :green[${currentMort.price:,.2f}]")
    st.write(f"### **Current Equity**: :green[${currentMort.equity_value:,.2f}]")
    st.write(f"### **Loan to Value Ratio**: :blue[{currentMort.loan_to_value:.2%}]")
    st.write(f"### **Loan End Date**: :blue[{currentMort.end_date}]")

# Save to session state for use in other pages
st.session_state["current_mortgage"] = currentMort

# st.write(st.session_state)
