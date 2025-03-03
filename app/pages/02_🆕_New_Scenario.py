import datetime as dt
import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import NewMortgageScenario

left, center, right = st.columns([6,18,6])

with left:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    pg2 = st.Page("pages/02_🆕_New_Scenario.py") 

    if st.button("**🆕 New Scenario**"):
        st.switch_page(pg2)

with right:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    pg3 = st.Page("pages/03_📈_Comparison.py")

    if st.button("**📈 Comparison**"):
        st.switch_page(pg3)


with center:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("# &ensp;&ensp;:violet[**New Mortgage**]")
    
    st.write("Put in the details of the new mortgage you are evaluating to compare to your current mortgage.")


col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 8, 0.5, 6])

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
        key="rate2",
    )
    price = st.number_input(
        "**House Price ($)**",
        min_value=0.0,
        value=300000.0,
        step=1000.0,
        key="price2",
    )

    start_date = st.date_input(
        "**Loan Start Date**", value=dt.datetime.now(), key="start1"
    )

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=0.0,
        step=100.0,
        key="prin1",
    )

with col2:
    st.write("")
    st.write("")
    st.write("")
    sqft = st.number_input(
        "**Square Footage**", min_value=0.0, value=2000.0, step=100.0, key="sqft1"
    )
    pmi = st.number_input(
        "**Current Monthly PMI ($)**", min_value=0.0, value=50.0, step=10.0, key="pmi1"
    )
    term = st.number_input("**Loan Term (years)**", min_value=0, value=30, key="term1")

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=0,
        step=1,
        key="prepay1",
    )

with col3:

    is_not_percent = st.toggle("% / $", value=False, key="down2")
    if is_not_percent:
        downpayment = st.number_input(
            "**Downpayment Amount ($)**",
            min_value=0.0,
            value=(price*0.20),
            step=1000.0,
            key="downamount2",
        )
    else:
        downpayment_percent = st.number_input(
            "**Downpayment (%)**",
            min_value=0.0,
            value=20.0,
            step=1.0,
            key="downpercent2"
        )
        downpayment = (downpayment_percent / 100 * price)
        

    # Tax section with toggle
    is_monthly_tax = st.toggle("Annual/Monthly", key="taxtoggle1", value=False)

    if is_monthly_tax:
        monthly_tax = st.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0,
            value=216.67,
            step=10.0,
            key="tax1_monthly",
        )
        tax = monthly_tax * 12  # Convert to annual for consistency
    else:
        tax = st.number_input(
            "**Annual Tax ($)**",
            min_value=0.0,
            value=2600.0,
            step=100.0,
            key="tax1_annual",
        )

    # Insurance section with toggle
    is_monthly_ins = st.toggle("Annual/Monthly", key="instoggle1", value=False)

    if is_monthly_ins:
        monthly_ins = st.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0,
            value=183.33,
            step=10.0,
            key="insurance1_monthly",
        )
        insurance = monthly_ins * 12  # Convert to annual for consistency
    else:
        insurance = st.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0,
            value=2200.0,
            step=100.0,
            key="insurance1_annual",
        )


NewMort = NewMortgageScenario(
    _rate=rate,
    _years=term,
    _tax=tax,
    _ins=insurance,
    _sqft=sqft,
    _extra_principal=prin,
    _prepay_periods=prepay,
    _price=price,
    _downpayment_amount=downpayment
)

buff3, mid, buff4 = st.columns([5, 15, 2])

with mid:
    st.write("")
    # Display mortgage details
    st.write("## &ensp;&ensp;:violet[**Mortgage Calcs**]")


dols, buffer, ratios = st.columns([8, 3, 8])   
with dols:    
    st.write(f"#### **Loan Amount**: :green[${NewMort.loan_amount:,.2f}]")
    st.write(
        f"#### **Principal & Interest**: :green[${NewMort.principal_and_interest:,.2f}]"
    )

with ratios:
    st.write(f"#### **Expected PMI**: :green[${NewMort.monthly_pmi:,.2f}]")
    st.write(f"#### **Total Monthly Payment**: :green[${NewMort.total_pmt:,.2f}]")

# Save to session state for use in other pages
st.session_state["new_mortgage"] = NewMort

# st.write(st.session_state)
