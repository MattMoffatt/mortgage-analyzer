
import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.mortgage_classes import NewMortgageScenario

# Import your utility functions
from src.utils.navigation_utils import register_page, safe_navigate
from src.utils.mortgage_utils import update_new_mortgage

###########################################################

# Set session and navigation functionality
# Needed for persisting data across pages

###########################################################


register_page("new_mortgage", update_new_mortgage)

###########################################################

# Top of page

###########################################################

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;:star:&ensp;&ensp;&ensp;:green[**New Mortgage**]&ensp;&ensp;&ensp;:star:", divider="grey")

left, center, right = st.columns([6,18,6])

with left:

    pg1 = st.Page("pages/01_💸_Current_Mortgage.py") 

    if st.button("**💸 Current Mortgage**"):
        safe_navigate(pg1)

with right:

    pg3 = st.Page("pages/03_📈_Comparison.py")

    if st.button("**📈 Comparison**"):
        safe_navigate(pg3)


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
        key="nm_rate",
    )

    price = st.number_input(
        "**House Price ($)**",
        min_value=0.0,
        value=st.session_state.nm_price,
        step=1000.0,
        key="nm_price",
    )

    start_date = st.date_input(
        "**Loan Start Date**",
        value=st.session_state.nm_start_date, 
        key="nm_start_date"
    )

    # Additional payment details
    prin = st.number_input(
        "**Extra Monthly Principal ($)**",
        min_value=0.0,
        value=st.session_state.nm_prin,
        step=100.0,
        key="nm_prin",
    )

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
        key="nm_sqft"
    )

    pmi = st.number_input(
        "**Current Monthly PMI ($)**", 
        min_value=0.0,
        value=st.session_state.nm_pmi, 
        step=10.0, 
        key="nm_pmi"
    )

    term = st.number_input(
        "**Loan Term (years)**", 
        min_value=0,
        value=st.session_state.nm_term, 
        key="nm_term"
    )

    prepay = st.number_input(
        "**Number of Prepay Periods (months)**",
        min_value=0,
        value=st.session_state.nm_prepay,
        step=1,
        key="nm_prepay",
    )

# right column

with col3:

    is_not_percent = st.toggle(
        "% / $",
        value=st.session_state.nm_is_not_percent, 
        key="nm_is_not_percent"
    )

    if is_not_percent:
        downpayment = st.number_input(
            "**Downpayment Amount ($)**",
            min_value=0.0,
            value=st.session_state.nm_downpayment,
            step=1000.0,
            key="nm_downpayment",
        )
    else:
        downpayment_percent = st.number_input(
            "**Downpayment (%)**",
            min_value=0.0,
            value=st.session_state.nm_downpayment_percent,
            step=1.0,
            key="nm_downpayment_percent"
        )
        st.session_state.nm_downpayment = (st.session_state.nm_downpayment_percent / 100) * st.session_state.nm_price

    # Tax section with toggle
    is_monthly_tax = st.toggle(
        "Annual/Monthly", 
        value=st.session_state.nm_is_monthly_tax,
        key="nm_is_monthly_tax"
    )

    if is_monthly_tax:
        monthly_tax = st.number_input(
            "**Monthly Tax ($)**",
            min_value=0.0,
            value=st.session_state.nm_monthly_tax,
            step=10.0,
            key="nm_monthly_tax",
        )
        st.session_state.nm_annual_tax = st.session_state.nm_monthly_tax * 12
    else:
        tax = st.number_input(
            "**Annual Tax ($)**",
            min_value=0.0,
            value=st.session_state.nm_annual_tax,
            step=100.0,
            key="nm_annual_tax",
        )
        st.session_state.nm_monthly_tax = st.session_state.nm_annual_tax / 12

    # Insurance section with toggle
    is_monthly_ins = st.toggle(
        "Annual/Monthly",
        value=st.session_state.nm_is_monthly_ins,
        key="nm_is_monthly_ins"
    )

    if is_monthly_ins:
        monthly_ins = st.number_input(
            "**Monthly Insurance ($)**",
            min_value=0.0,
            value=st.session_state.nm_monthly_ins,
            step=10.0,
            key="nm_monthly_ins",
        )
        st.session_state.nm_annual_ins = st.session_state.nm_monthly_ins * 12
    else:
        insurance = st.number_input(
            "**Annual Insurance ($)**",
            min_value=0.0,
            value=st.session_state.nm_annual_ins,
            step=100.0,
            key="nm_annual_ins",
        )
        st.session_state.nm_monthly_ins = st.session_state.nm_annual_ins / 12

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


loan_col, payment_col, ann = st.columns([4,4,4])

with loan_col: 

    st.subheader("**Loan Metrics:**",divider="green")

    st.metric(
        "**Loan Amount Today:**",
        value=f"${NewMort.loan_amount:,.2f}"
    )

    st.metric(
        "**Value in 5 Years (3% Ann growth):**",
        value=f"${NewMort.estimate_value_at_year(5):,.2f}",
        delta=F"${(NewMort.estimate_value_at_year(5) - NewMort.price):,.2f}",
        delta_color="normal"
    )

    st.metric(
        "**Value in 10 Years (3% Ann growth):**",
        value=f"${NewMort.estimate_value_at_year(10):,.2f}",
        delta=F"${(NewMort.estimate_value_at_year(10) - NewMort.price):,.2f}",
        delta_color="normal"
    )

    # st.write(f"#### **Loan Amount**: :green[${NewMort.loan_amount:,.2f}]")
    # st.write(
    #     f"#### **Principal & Interest**: :green[${NewMort.principal_and_interest:,.2f}]"
    # )

with payment_col:

    st.subheader("**Pmt Metrics:**",divider="green")

    st.metric(
        "**Total Monthly Payment:**",
        value=f"${NewMort.total_pmt:,.2f}"
    )

    st.metric(
        "**Estimated Monthly PMI:**",
        value=f"${NewMort.monthly_pmi:,.2f}"
    )
    
    st.write("")

    st.metric(
        "**Months of PMI payments:**",
        value=f"{NewMort.pmi_periods_remaining()}"
    )

with ann:

    st.subheader("**Other:**",divider="green")

    if is_monthly_tax:
        st.metric(
            "**Annual Tax Amount ($)**",
            value=f"${NewMort.tax:,.2f}"
        )

    if is_monthly_ins:
        st.metric(
            "**Annual Ins Amount ($)**",
            value=f"${NewMort.ins:,.2f}"
        )
    
    if not is_not_percent:
        st.metric(
            "**Downpayment Amount ($):**",
            value=f"${NewMort.downpayment_amount:,.2f}"
        )




# else:

#     loan_col, payment_col, dpm = st.columns([4,4,4])

#     with loan_col: 

#         st.subheader("**Loan Metrics:**",divider="green")

#         st.metric(
#             "**Loan Amount Today:**",
#             value=f"${NewMort.loan_amount:,.2f}"
#         )

#         st.metric(
#             "**Value in 5 Years (3% annual growth):**",
#             value=f"${NewMort.estimate_value_at_year(5):,.2f}",
#             delta=F"${(NewMort.estimate_value_at_year(5) - NewMort.price):,.2f}",
#             delta_color="normal"
#         )

#         st.metric(
#             "**Value in 10 Years (3% annual growth):**",
#             value=f"${NewMort.estimate_value_at_year(10):,.2f}",
#             delta=F"${(NewMort.estimate_value_at_year(10) - NewMort.price):,.2f}",
#             delta_color="normal"
#         )

#         # st.write(f"#### **Loan Amount**: :green[${NewMort.loan_amount:,.2f}]")
#         # st.write(
#         #     f"#### **Principal & Interest**: :green[${NewMort.principal_and_interest:,.2f}]"
#         # )

#     with payment_col:

#         st.subheader("**Pmt Metrics:**",divider="green")

#         st.metric(
#             "**Total Monthly Payment:**",
#             value=f"${NewMort.total_pmt:,.2f}"
#         )

#         st.metric(
#             "**Estimated Monthly PMI:**",
#             value=f"${NewMort.monthly_pmi:,.2f}"
#         )
        
#         st.write("")

#         st.metric(
#             "**Months of PMI payments:**",
#             value=f"{NewMort.pmi_periods_remaining()}"
#         )
    
#     with dpm:

#         st.subheader("**Downpayment:**",divider="green")
        
#         st.metric(
#             "**Downpayment Amount ($):**",
#             value=f"${NewMort.downpayment_amount:,.2f}"
#         )
    




    # st.write(f"#### **Expected PMI**: :green[${NewMort.monthly_pmi:,.2f}]")
    # st.write(f"#### **Total Monthly Payment**: :green[${NewMort.total_pmt:,.2f}]")

# Save to session state for use in other pages
st.session_state["new_mortgage"] = NewMort

# st.write(st.session_state)
