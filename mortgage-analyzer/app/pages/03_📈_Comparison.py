import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import your utility functions
from src.utils.navigation_utils import register_page, safe_navigate
from src.utils.session_utils import initialize_mortgage_app_state
from src.visualizations.mortgage_charts import (
    create_monthly_payment_comparison,
    create_equity_buildup_chart,
    create_interest_paid_comparison,
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

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;:chart_with_upwards_trend:&ensp;&ensp;&ensp;:blue[**Mortgage Comparison**]&ensp;&ensp;&ensp;:chart_with_upwards_trend:", divider="grey")

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

# Check if current mortgage exists and at least one scenario is available
if not st.session_state.get("current_mortgage"):
    st.warning("Please fill out your current mortgage details first.")
    st.stop()

# Check if at least one scenario exists
has_new_mortgage = st.session_state.get("new_mortgage") is not None
has_refinance = st.session_state.get("refinance_scenario") is not None

if not (has_new_mortgage or has_refinance):
    st.warning("Please fill out either a new mortgage scenario or refinance scenario before viewing comparisons.")
    st.stop()

currentMort = st.session_state.current_mortgage

# Determine which scenario to compare
if has_new_mortgage and has_refinance:
    # Both scenarios exist - let user choose
    scenario_choice = st.radio(
        "**Choose scenario to compare with your current mortgage:**",
        ["New Purchase", "Refinance"],
        horizontal=True,
        help="Select which scenario you want to compare against your current mortgage"
    )
    
    if scenario_choice == "New Purchase":
        newMort = st.session_state.new_mortgage
        scenario_type = "new_purchase"
    else:
        newMort = st.session_state.refinance_scenario
        scenario_type = "refinance"
        
elif has_new_mortgage:
    newMort = st.session_state.new_mortgage
    scenario_type = "new_purchase"
else:
    newMort = st.session_state.refinance_scenario
    scenario_type = "refinance"

###############################################################

# Key Metrics Summary

###############################################################

st.subheader("Key Decision Factors", divider="blue")

# Get comparison data
comparison_df = create_mortgage_comparison_dashboard(currentMort, newMort)

# Create three columns for better visual layout
col1, col2, col3 = st.columns(3)

# Monthly payment and savings comparison
with col1:
    monthly_diff = newMort.total_pmt - currentMort.total_pmt
    monthly_diff_text = "Increase" if monthly_diff > 0 else "Savings"
    
    st.metric(
        "New Monthly Payment",
        f"${newMort.total_pmt:,.2f}",
        f"{monthly_diff_text}: ${abs(monthly_diff):,.2f}",
        delta_color="inverse"
    )
    
    # Interest rate comparison
    interest_diff = newMort.rate - currentMort.rate
    interest_diff_text = "Higher" if interest_diff > 0 else "Lower"
    
    st.metric(
        "New Interest Rate",
        f"{newMort.rate:.3f}%",
        f"{interest_diff_text} by {abs(interest_diff):.3f}%",
        delta_color="inverse"
    )

# Home value and equity comparison
with col2:
    equity_current = currentMort.equity_value
    
    if scenario_type == "refinance":
        equity_new = newMort.equity_after_refinance
        equity_diff = equity_new - equity_current
        
        st.metric(
            "Property Value",
            f"${newMort.current_property_value:,.2f}",
            "Same property" if abs(newMort.current_property_value - currentMort.price) < 1000 else f"${newMort.current_property_value - currentMort.price:,.2f} difference",
            delta_color="normal"
        )
        
        st.metric(
            "Equity After Refinance",
            f"${equity_new:,.2f}",
            f"${equity_diff:,.2f} difference",
            delta_color="normal" if equity_diff >= 0 else "inverse"
        )
    else:
        equity_new = newMort.price - newMort.loan_amount
        equity_diff = equity_new - equity_current
        
        st.metric(
            "New Property Value",
            f"${newMort.price:,.2f}",
            f"${newMort.price - currentMort.price:,.2f} difference",
            delta_color="normal"
        )
        
        st.metric(
            "New Equity Position",
            f"${equity_new:,.2f}",
            f"${equity_diff:,.2f} difference",
            delta_color="normal" if equity_diff >= 0 else "inverse"
        )

# Loan details comparison
with col3:
    # Loan term comparison
    term_diff = (newMort.periods_remaining / 12) - (currentMort.periods_remaining / 12)
    term_diff_text = "Longer" if term_diff > 0 else "Shorter"
    
    if scenario_type == "refinance":
        st.metric(
            "Closing Costs",
            f"${newMort.closing_costs:,.2f}",
            help="Estimated closing costs for refinance"
        )
        if hasattr(newMort, 'cash_out_amount') and newMort.cash_out_amount > 0:
            st.metric(
                "Net Cash to You",
                f"${newMort.net_cash_to_borrower:,.2f}",
                help="Cash you receive after closing costs"
            )
    else:
        st.metric(
            "Total Initial Investment",
            f"${newMort.initial_investment:,.2f}"
        )
    
    # PMI comparison
    pmi_diff = newMort.monthly_pmi - currentMort.monthly_pmi
    pmi_diff_text = "Higher" if pmi_diff > 0 else "Lower"
    
    st.write("")

    st.metric(
        "New Monthly PMI",
        f"${newMort.monthly_pmi:,.2f}",
        f"{pmi_diff_text} by ${abs(pmi_diff):,.2f}",
        delta_color="inverse" if pmi_diff > 0 else "normal"
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
tab1, tab2, tab3 = st.tabs(["Monthly Payments", "Equity Growth Projections", "Interest Analysis"])

with tab1:

    create_monthly_payment_comparison(currentMort, newMort)

    # st.info("""
    # These ccomparisons:
    # - **Loan Balance**: Shows how quickly you'll pay down each loan
    # - **Equity Growth**: Includes both loan paydown and estimated 3% annual property appreciation
    # """)
with tab2:
    
    create_equity_buildup_chart(currentMort,newMort)
    
    st.info("""
    This chart shows how much your equity will increase over time:
    - **Equity Growth**: Includes both loan paydown and estimated 3% annual property appreciation
            * currently no support for changing this assumption
    """)

with tab3:
    
    create_interest_paid_comparison(currentMort, newMort)
    
    st.info("""
    These chart compares the total interest you will pay on each mortgage:
    - **Total Interest**: The total interest paid over the life of each loan
    - **Interest to Principal Ratio**: How much interest you will pay for each $1 of principal paid
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

if scenario_type == "refinance":
    equity_position_change = newMort.equity_after_refinance - currentMort.equity_value
    closing_costs = newMort.closing_costs
else:
    equity_position_change = (newMort.price - newMort.loan_amount) - currentMort.equity_value
    closing_costs = getattr(newMort, 'closing_costs', newMort.price * 0.03)

# Recommendation logic based on scenario type
if scenario_type == "refinance":
    # Refinance-specific recommendations
    if monthly_savings > 0 and interest_rate_diff > 0:
        # Break-even calculation for refinance
        break_even_months = closing_costs / monthly_savings if monthly_savings > 0 else float('inf')
        
        recommendation = "✅ **FAVORABLE REFINANCE**: This refinance appears beneficial."
        details = f"""
        **Key benefits:**
        - Monthly savings of ${monthly_savings:.2f}
        - Interest rate reduction of {interest_rate_diff:.3f}%
        - Break-even point: {break_even_months:.0f} months
        - {'Maintains' if abs(equity_position_change) < 1000 else 'Changes'} equity position by ${abs(equity_position_change):,.2f}
        """
        
        if hasattr(newMort, 'cash_out_amount') and newMort.cash_out_amount > 0:
            details += f"\n- Cash-out amount: ${newMort.cash_out_amount:,.2f} (net: ${newMort.net_cash_to_borrower:,.2f})"
            
    elif monthly_savings > 0 and interest_rate_diff <= 0:
        recommendation = "⚠️ **REVIEW CAREFULLY**: Monthly savings without rate improvement may indicate longer term."
        details = f"""
        **Considerations:**
        - Monthly savings of ${monthly_savings:.2f}
        - {'No rate improvement' if interest_rate_diff == 0 else f'Rate increase of {abs(interest_rate_diff):.3f}%'}
        - {'Term extended by' if term_diff > 0 else 'Term reduced by'} {abs(term_diff):.1f} years
        - Closing costs: ${closing_costs:,.2f}
        """
        
    elif monthly_savings <= 0 and interest_rate_diff > 0:
        recommendation = "⚠️ **MIXED REFINANCE**: Rate improvement but higher payments."
        details = f"""
        **Considerations:**
        - Interest rate reduction of {interest_rate_diff:.3f}%
        - Higher monthly payment of ${abs(monthly_savings):.2f}
        - May benefit from faster equity building
        - Closing costs: ${closing_costs:,.2f}
        """
        
    else:
        recommendation = "❌ **NOT RECOMMENDED**: This refinance increases both payment and rate."
        details = f"""
        **Concerns:**
        - Monthly payment increase of ${abs(monthly_savings):.2f}
        - Interest rate increase of {abs(interest_rate_diff):.3f}%
        - Closing costs: ${closing_costs:,.2f}
        """
        
else:
    # New purchase recommendations (existing logic)
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

if scenario_type == "refinance":
    with consideration_col1:
        st.markdown("""
        - **Break-even analysis**: Factor in how long you'll stay in the home
        - **Rate timing**: Consider if rates might drop further before refinancing
        - **Cash-out usage**: If borrowing extra cash, have a clear plan for use
        """)

    with consideration_col2:
        st.markdown("""
        - **PMI impact**: Refinancing might add/remove PMI based on new LTV
        - **Tax implications**: Interest deduction may change with new loan amount
        - **Appraisal requirement**: Property value may need professional appraisal
        """)
else:
    with consideration_col1:
        st.markdown("""
        - **Closing costs**: Typical costs range from 2-3% of home price
        - **Down payment source**: Consider impact on other financial goals
        - **Market conditions**: Factor in local real estate trends
        """)

    with consideration_col2:
        st.markdown("""
        - **PMI**: Consider 20% down payment to avoid PMI
        - **Future rates**: Lock in rate if favorable compared to trends
        - **Total housing costs**: Include HOA, utilities, maintenance
        """)

###############################################################

# Footer - recommended by ClaudeAI

###############################################################

st.markdown("---")
st.caption("This comparison is for informational purposes only and does not constitute financial advice. Consult with a mortgage professional before making financial decisions.")