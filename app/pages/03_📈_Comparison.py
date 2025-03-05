import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import altair as alt

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import your utility functions
from src.utils.navigation_utils import register_page, safe_navigate
from src.utils.session_utils import initialize_mortgage_app_state
from src.visualizations.mortgage_charts import (
    create_monthly_payment_comparison,
    create_amortization_comparison,
    create_equity_buildup_chart,
    create_interest_paid_comparison,
    create_loan_term_comparison,
    create_breakeven_chart,
    create_mortgage_comparison_dashboard
)

###############################################################

# Session state management

###############################################################

# Initialize all session state variables properly
initialize_mortgage_app_state()

# Register this page (without an update function since there's nothing to save)
register_page("comparison_page", None)

###############################################################

# Top of page

###############################################################

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;:chart_with_upwards_trend:&ensp;&ensp;&ensp;:blue[**Mortgage Comparison**]&ensp;&ensp;&ensp;:chart_with_upwards_trend:", divider="grey")

left, center, right = st.columns([6,18,6])

with left:
    pg1 = st.Page("pages/01_💸_Current_Mortgage.py")
    if st.button("**💸 Current Mortgage**", key="comparison_to_current_mortgage"):
        safe_navigate(pg1)

with right:
    pg2 = st.Page("pages/02_🆕_New_Scenario.py")
    if st.button("**🆕 New Scenario**", key="comparison_to_new_mortgage"):
        safe_navigate(pg2)

with center:    
    st.write("This page compares your current mortgage to the new mortgage scenario to help you make an informed decision.")

###############################################################

# Check if mortgage data is available

###############################################################

# Check if both mortgage objects exist and are valid
if not (st.session_state.get("current_mortgage") and st.session_state.get("new_mortgage")):
    st.warning("Please fill out both current mortgage and new mortgage scenario details before viewing comparisons.")
    st.stop()

currentMort = st.session_state.current_mortgage
newMort = st.session_state.new_mortgage

###############################################################

# Key Metrics Summary

###############################################################

st.subheader("Key Metrics Comparison", divider="blue")

# Get comparison data
comparison_df = create_mortgage_comparison_dashboard(currentMort, newMort)

# Create three columns for better visual layout
col1, col2, col3 = st.columns(3)

# Monthly payment and savings comparison
with col1:
    monthly_diff = newMort.total_pmt - currentMort.total_pmt
    monthly_diff_text = "Increase" if monthly_diff > 0 else "Savings"
    
    st.metric(
        "Monthly Payment Comparison",
        f"${newMort.total_pmt:,.2f}",
        f"{monthly_diff_text}: ${abs(monthly_diff):,.2f}",
        delta_color="inverse"
    )
    
    # Interest rate comparison
    interest_diff = newMort.rate - currentMort.rate
    interest_diff_text = "Higher" if interest_diff > 0 else "Lower"
    
    st.metric(
        "Interest Rate",
        f"{newMort.rate:.3f}%",
        f"{interest_diff_text} by {abs(interest_diff):.3f}%",
        delta_color="inverse"
    )

# Home value and equity comparison
with col2:
    equity_current = currentMort.equity_value
    equity_new = newMort.price - newMort.loan_amount
    equity_diff = equity_new - equity_current
    
    st.metric(
        "Property Value",
        f"${newMort.price:,.2f}",
        f"${newMort.price - currentMort.price:,.2f} difference",
        delta_color="normal"
    )
    
    st.metric(
        "Equity Position",
        f"${equity_new:,.2f}",
        f"${equity_diff:,.2f} difference",
        delta_color="normal"
    )

# Loan details comparison
with col3:
    # Loan term comparison
    term_diff = (newMort.periods_remaining / 12) - (currentMort.periods_remaining / 12)
    term_diff_text = "Longer" if term_diff > 0 else "Shorter"
    
    st.metric(
        "Loan Term Remaining",
        f"{newMort.periods_remaining / 12:.1f} years",
        f"{term_diff_text} by {abs(term_diff):.1f} years",
        delta_color="off"  # Neutral color as longer/shorter isn't inherently good/bad
    )
    
    # PMI comparison
    pmi_diff = newMort.monthly_pmi - currentMort.monthly_pmi
    pmi_diff_text = "Higher" if pmi_diff > 0 else "Lower"
    
    st.metric(
        "Monthly PMI",
        f"${newMort.monthly_pmi:,.2f}",
        f"{pmi_diff_text} by ${abs(pmi_diff):,.2f}",
        delta_color="inverse"
    )

# Show detailed metric table with expandable section
with st.expander("View Detailed Metrics Comparison"):
    # Exclude format and better columns from display
    display_df = comparison_df[["Metric", "Current", "New", "Difference"]].copy()
    
    # Format values according to the format column
    for i, row in comparison_df.iterrows():
        display_df.loc[i, "Current"] = row["Format"].format(row["Current"])
        display_df.loc[i, "New"] = row["Format"].format(row["New"])
        
        # Format difference and add indicator
        diff_value = row["Difference"]
        if row["Better"] == "lower":
            indicator = "✅" if diff_value < 0 else "❌" if diff_value > 0 else "➖"
        elif row["Better"] == "higher":
            indicator = "✅" if diff_value > 0 else "❌" if diff_value < 0 else "➖"
        else:  # "context" or other
            indicator = ""
            
        formatted_diff = row["Format"].format(diff_value)
        if diff_value > 0:
            formatted_diff = "+" + formatted_diff
            
        display_df.loc[i, "Difference"] = f"{formatted_diff} {indicator}"
    
    st.table(display_df)

###############################################################

# Visual Comparisons

###############################################################

st.subheader("Visual Comparisons", divider="blue")

# Create tabs for different visualization categories
tab1, tab2, tab3 = st.tabs(["Monthly Payments", "Loan Balance & Equity", "Interest & Term"])

with tab2:
    # Two-column layout for related charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Loan Balance Over Time")
        st.altair_chart(create_amortization_comparison(currentMort, newMort), use_container_width=True)
    
    with col2:
        st.subheader("Equity Growth Over Time")
        st.altair_chart(create_equity_buildup_chart(currentMort, newMort), use_container_width=True)
    
    st.info("""
    These charts show how your loan balance decreases and your equity increases over time:
    - **Loan Balance**: Shows how quickly you'll pay down each loan
    - **Equity Growth**: Includes both loan paydown and estimated 3% annual property appreciation
    """)

with tab3:
    # Two-column layout for related charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Interest Comparison")
        st.altair_chart(create_interest_paid_comparison(currentMort, newMort), use_container_width=True)
    
    with col2:
        st.subheader("Loan Term Comparison")
        st.altair_chart(create_loan_term_comparison(currentMort, newMort), use_container_width=True)
    
    st.info("""
    These charts compare the overall cost and duration of each mortgage:
    - **Total Interest**: The total interest paid over the life of each loan
    - **Loan Term**: How long until each loan is paid off
    """)

# with tab4:
#     st.subheader("Refinance Breakeven Analysis")
#     st.altair_chart(create_breakeven_chart(currentMort, newMort), use_container_width=True)
    
#     st.info("""
#     This analysis shows when refinancing would break even, including estimated closing costs:
#     - **Above zero line**: You're still paying for the cost of refinancing
#     - **Below zero line**: You've recovered costs and are saving money
#     - **Where line crosses zero**: Your breakeven point
    
#     *Assumes approximately 3% closing costs on the new loan amount.*
#     """)

###############################################################

# Amortization Schedule Comparison

###############################################################

with st.expander("View Amortization Schedules"):
    amort_tab1, amort_tab2 = st.tabs(["Current Mortgage", "New Mortgage"])
    
    with amort_tab1:
        current_schedule = currentMort.amortization_schedule()
        current_schedule["Year"] = (current_schedule["month"] / 12).apply(lambda x: round(x, 1))
        st.dataframe(
            current_schedule,
            hide_index=True,
            column_config={
                "month": "Month",
                "payment": st.column_config.NumberColumn("Payment", format="$%.2f"),
                "principal": st.column_config.NumberColumn("Principal", format="$%.2f"),
                "interest": st.column_config.NumberColumn("Interest", format="$%.2f"),
                "principal_paydown": st.column_config.NumberColumn("Extra Principal", format="$%.2f"),
                "balance": st.column_config.NumberColumn("Remaining Balance", format="$%.2f"),
                "Year": "Year"
            },
            use_container_width=True
        )
    
    with amort_tab2:
        new_schedule = newMort.amortization_schedule()
        new_schedule["Year"] = (new_schedule["month"] / 12).apply(lambda x: round(x, 1))
        st.dataframe(
            new_schedule,
            hide_index=True,
            column_config={
                "month": "Month",
                "payment": st.column_config.NumberColumn("Payment", format="$%.2f"),
                "principal": st.column_config.NumberColumn("Principal", format="$%.2f"),
                "interest": st.column_config.NumberColumn("Interest", format="$%.2f"),
                "principal_paydown": st.column_config.NumberColumn("Extra Principal", format="$%.2f"),
                "balance": st.column_config.NumberColumn("Remaining Balance", format="$%.2f"),
                "Year": "Year"
            },
            use_container_width=True
        )

###############################################################

# Recommendation Section

###############################################################

st.subheader("Mortgage Recommendation", divider="blue")

# Calculate key decision factors
monthly_savings = currentMort.total_pmt - newMort.total_pmt
interest_rate_diff = currentMort.rate - newMort.rate
term_diff = (newMort.periods_remaining / 12) - (currentMort.periods_remaining / 12)
equity_position_change = (newMort.price - newMort.loan_amount) - currentMort.equity_value

# Simple recommendation logic
if monthly_savings > 0 and interest_rate_diff > 0:
    recommendation = "✅ **FAVORABLE**: The new mortgage scenario appears favorable. You'll save on monthly payments and have a lower interest rate."
    details = f"""
    **Key benefits:**
    - Monthly savings of ${monthly_savings:.2f}
    - Interest rate reduction of {interest_rate_diff:.3f}%
    - {'Increased equity position' if equity_position_change > 0 else 'Consider impact on equity position'}
    """
elif monthly_savings > 0 and interest_rate_diff <= 0:
    recommendation = "⚠️ **POTENTIALLY FAVORABLE**: The new scenario offers monthly savings but not from a rate reduction. Consider the full term cost."
    details = f"""
    **Considerations:**
    - Monthly savings of ${monthly_savings:.2f} may be from a longer term rather than better rate
    - {'Term extended by' if term_diff > 0 else 'Term reduced by'} {abs(term_diff):.1f} years
    - Review total interest paid over the life of the loan
    """
elif monthly_savings <= 0 and interest_rate_diff > 0:
    recommendation = "⚠️ **MIXED SCENARIO**: Lower rate but higher monthly payment. May be beneficial for long-term interest savings or building equity faster."
    details = f"""
    **Considerations:**
    - Interest rate reduction of {interest_rate_diff:.3f}%
    - Higher monthly payment of ${abs(monthly_savings):.2f}
    - {'Term reduced by' if term_diff < 0 else 'Term extended by'} {abs(term_diff):.1f} years
    - {'Higher equity position' if equity_position_change > 0 else 'Lower equity position'} of ${abs(equity_position_change):.2f}
    """
else:
    recommendation = "❌ **NOT RECOMMENDED**: This scenario increases both your monthly payment and interest rate."
    details = f"""
    **Concerns:**
    - Monthly payment increase of ${abs(monthly_savings):.2f}
    - Interest rate increase of {abs(interest_rate_diff):.3f}%
    - {'Term extended by' if term_diff > 0 else 'Term reduced by'} {abs(term_diff):.1f} years
    """

# Display recommendation
st.markdown(recommendation)
st.markdown(details)

# Additional considerations
st.write("**Additional considerations:**")
consideration_col1, consideration_col2 = st.columns(2)

with consideration_col1:
    st.markdown("""
    - **Closing costs**: Typical refinance costs range from 2-5% of loan amount
    - **How long you'll stay**: If moving soon, may not recoup costs
    - **Cash-out refinance**: Consider if you need funds for other purposes
    """)

with consideration_col2:
    st.markdown("""
    - **Tax implications**: Mortgage interest deduction may change
    - **PMI**: New loan might add or remove PMI requirements
    - **Future rates**: Consider if rates might drop further
    """)

###############################################################

# Footer

###############################################################

st.markdown("---")
st.caption("This comparison is for informational purposes only and does not constitute financial advice. Consult with a mortgage professional before making financial decisions.")