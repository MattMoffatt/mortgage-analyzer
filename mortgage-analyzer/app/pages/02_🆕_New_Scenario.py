import sys
from pathlib import Path

import streamlit as st

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))


# Import your utility functions
from src.utils.navigation_utils import register_page, safe_navigate
from src.utils.mortgage_utils import update_new_mortgage, new_mortgage_persistent_storage, new_mortgage_run_calcs, refinance_persistent_storage, refinance_run_calcs

# Import your visualization functions
from src.visualizations.mortgage_charts import (
        create_single_mortgage_payment_breakdown, 
        create_single_mortgage_amortization_chart,
        create_interest_principal_ratio_chart,
        create_mortgage_timeline_chart,
        create_equity_growth_chart 
    )

###########################################################

# Initialize persistent storage if not already present

###########################################################

new_mortgage_persistent_storage()
refinance_persistent_storage()

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
    if st.button("**💸 Current Mortgage**", key="new_mortgage_to_current_mortgage"):
        safe_navigate(pg1)

with right:
    pg3 = st.Page("pages/03_📈_Comparison.py")
    if st.button("**📈 Comparison**", key="new_mortgage_to_comparison"):
        safe_navigate(pg3)

with center:
    st.write("Put in the details of the new mortgage you are evaluating to compare to your current mortgage.")

###########################################################

# Helper functions - only used in this script so not defined in util files

###########################################################

def update_nm_data(field):
    # Update permanent storage from temporary widget state
    st.session_state.nm_data[field] = st.session_state[f"temp_nm_{field}"]

def update_downpayment_values(source):
    # Update downpayment values based on source
    if source == "amount":
        # User changed amount, update percentage
        st.session_state.nm_data["downpayment"] = st.session_state["temp_nm_downpayment"]
        if st.session_state.nm_data["price"] > 0:
            st.session_state.nm_data["downpayment_percent"] = (st.session_state.nm_data["downpayment"] / st.session_state.nm_data["price"]) * 100
            st.session_state["temp_nm_downpayment_percent"] = st.session_state.nm_data["downpayment_percent"]

    elif source == "percent":
        # User changed percentage, update amount
        st.session_state.nm_data["downpayment_percent"] = st.session_state["temp_nm_downpayment_percent"]
        st.session_state.nm_data["downpayment"] = (st.session_state.nm_data["downpayment_percent"] / 100) * st.session_state.nm_data["price"]
        st.session_state["temp_nm_downpayment"] = st.session_state.nm_data["downpayment"]

    elif source == "price":
        # Price changed, update amount based on percentage
        if not st.session_state.nm_data["is_not_percent"]:
            st.session_state.nm_data["downpayment"] = (st.session_state.nm_data["downpayment_percent"] / 100) * st.session_state.nm_data["price"]
            st.session_state["temp_nm_downpayment"] = st.session_state.nm_data["downpayment"]

    elif source == "toggle":
        # Toggle changed, update appropriate values
        if st.session_state.nm_data["is_not_percent"]:
            # Switched to amount mode - nothing needed as the amount is already set
            pass
        else:
            # Switched to percentage mode - recalculate percentage from amount
            if st.session_state.nm_data["price"] > 0:
                st.session_state.nm_data["downpayment_percent"] = (st.session_state.nm_data["downpayment"] / st.session_state.nm_data["price"]) * 100
                st.session_state["temp_nm_downpayment_percent"] = st.session_state.nm_data["downpayment_percent"]

def update_nm_tax_values(source):
    # Update both annual and monthly tax values based on source
    if source == "monthly":
        # User changed monthly value, update annual
        st.session_state.nm_data["monthly_tax"] = st.session_state["temp_nm_monthly_tax"]
        st.session_state.nm_data["annual_tax"] = st.session_state.nm_data["monthly_tax"] * 12

        # Update the temporary value as well
        st.session_state["temp_nm_annual_tax"] = st.session_state.nm_data["annual_tax"]

    elif source == "annual":
        # User changed annual value, update monthly
        st.session_state.nm_data["annual_tax"] = st.session_state["temp_nm_annual_tax"]
        st.session_state.nm_data["monthly_tax"] = st.session_state.nm_data["annual_tax"] / 12

        # Update the temporary value as well
        st.session_state["temp_nm_monthly_tax"] = st.session_state.nm_data["monthly_tax"]

    elif source == "toggle":
        # Toggle changed, ensure both values are synced
        if st.session_state.nm_data["is_monthly_tax"]:
            # Switched to monthly view, make sure monthly value is set
            st.session_state["temp_nm_monthly_tax"] = st.session_state.nm_data["monthly_tax"]
        else:
            # Switched to annual view, make sure annual value is set
            st.session_state["temp_nm_annual_tax"] = st.session_state.nm_data["annual_tax"]

def update_nm_insurance_values(source):
    # Update both annual and monthly insurance values based on source
    if source == "monthly":
        # User changed monthly value, update annual
        st.session_state.nm_data["monthly_ins"] = st.session_state["temp_nm_monthly_ins"]
        st.session_state.nm_data["annual_ins"] = st.session_state.nm_data["monthly_ins"] * 12

        # Update the temporary value as well
        st.session_state["temp_nm_annual_ins"] = st.session_state.nm_data["annual_ins"]

    elif source == "annual":
        # User changed annual value, update monthly
        st.session_state.nm_data["annual_ins"] = st.session_state["temp_nm_annual_ins"]
        st.session_state.nm_data["monthly_ins"] = st.session_state.nm_data["annual_ins"] / 12

        # Update the temporary value as well
        st.session_state["temp_nm_monthly_ins"] = st.session_state.nm_data["monthly_ins"]

    elif source == "toggle":
        # Toggle changed, ensure both values are synced
        if st.session_state.nm_data["is_monthly_ins"]:
            # Switched to monthly view, make sure monthly value is set
            st.session_state["temp_nm_monthly_ins"] = st.session_state.nm_data["monthly_ins"]

        else:
            # Switched to annual view, make sure annual value is set
            st.session_state["temp_nm_annual_ins"] = st.session_state.nm_data["annual_ins"]

###########################################################

# Input Section

###########################################################    

st.write("")

new, refinance = st.tabs(['New Mortgage', 'Refinance'])

with new:
    col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 8, 0.5, 6]) # split into thre columns with two blank buffer columns in between

    # left column
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        rate = st.number_input(
            "**Interest Rate (%)**",
            min_value=0.0001,
            step=0.005,
            format="%0.3f",
            key="temp_nm_rate",
            on_change=lambda: update_nm_data("rate")
        )
        st.write("")
        price = st.number_input(
            "**House Price ($)**",
            min_value=0.0001,
            step=1000.0,
            key="temp_nm_price",
            on_change=lambda: (update_nm_data("price"), update_downpayment_values("price"))
        )
        st.write("")
        start_date = st.date_input(
            "**Loan Start Date**",
            key="temp_nm_start_date",
            on_change=lambda: update_nm_data("start_date")
        )

    # middle column
    with col2:
        st.write("")
        st.write("")
        st.write("")

        sqft = st.number_input(
            "**Square Footage**", 
            min_value=0.0001,
            step=100.0, 
            key="temp_nm_sqft",
            on_change=lambda: update_nm_data("sqft")
        )

        term = st.number_input(
            "**Loan Term (years)**", 
            min_value=1,
            key="temp_nm_term",
            on_change=lambda: update_nm_data("term")
        )

        # Additional payment details
        prin = st.number_input(
            "**Extra Monthly Principal ($)**",
            min_value=0.0,
            step=100.0,
            key="temp_nm_prin",
            on_change=lambda: update_nm_data("prin")
        )

        prepay = st.number_input(
            "**Number of Prepay Periods (months)**",
            min_value=0,
            step=1,
            key="temp_nm_prepay",
            on_change=lambda: update_nm_data("prepay")
        )

    # right column
    with col3:
        is_not_percent = st.toggle(
            "% / $",
            key="temp_nm_is_not_percent",
            on_change=lambda: (update_nm_data("is_not_percent"), update_downpayment_values("toggle"))
        )

        if is_not_percent:
            downpayment = st.number_input(
                "**Downpayment Amount ($)**",
                min_value=0.0001,
                step=1000.0,
                key="temp_nm_downpayment",
                on_change=lambda: update_downpayment_values("amount")
            )
        else:
            downpayment_percent = st.number_input(
                "**Downpayment (%)**",
                min_value=0.0001,
                step=1.0,
                key="temp_nm_downpayment_percent",
                on_change=lambda: update_downpayment_values("percent")
            )
            
            # Force calculate the downpayment
            st.session_state.nm_data["downpayment"] = (st.session_state["temp_nm_downpayment_percent"] / 100) * st.session_state["temp_nm_price"]
            st.session_state["temp_nm_downpayment"] = st.session_state.nm_data["downpayment"]
            downpayment = st.session_state.nm_data["downpayment"]

        is_monthly_tax = st.toggle(
            "Annual/Monthly",
            key="temp_nm_is_monthly_tax",
            on_change=lambda: (update_nm_data("is_monthly_tax"), update_nm_tax_values("toggle"))
        )

        if is_monthly_tax:
            monthly_tax = st.number_input(
                "**Monthly Tax ($)**",
                min_value=0.0001,
                step=10.0,
                key="temp_nm_monthly_tax",
                on_change=lambda: update_nm_tax_values("monthly")
            )
            
            # Force update the annual tax value
            st.session_state.nm_data["annual_tax"] = st.session_state["temp_nm_monthly_tax"] * 12
            st.session_state["temp_nm_annual_tax"] = st.session_state.nm_data["annual_tax"]
            tax = st.session_state.nm_data["annual_tax"]
        else:
            tax = st.number_input(
                "**Annual Tax ($)**",
                min_value=0.0001,
                step=100.0,
                key="temp_nm_annual_tax",
                on_change=lambda: update_nm_tax_values("annual")
            )
            
            # Force update the monthly tax value
            st.session_state.nm_data["monthly_tax"] = st.session_state["temp_nm_annual_tax"] / 12
            st.session_state["temp_nm_monthly_tax"] = st.session_state.nm_data["monthly_tax"]
            monthly_tax = st.session_state.nm_data["monthly_tax"]

        is_monthly_ins = st.toggle(
            "Annual/Monthly",
            key="temp_nm_is_monthly_ins",
            on_change=lambda: (update_nm_data("is_monthly_ins"), update_nm_insurance_values("toggle"))
        )

        if is_monthly_ins:
            monthly_ins = st.number_input(
                "**Monthly Insurance ($)**",
                min_value=0.0001,
                step=10.0,
                key="temp_nm_monthly_ins",
                on_change=lambda: update_nm_insurance_values("monthly")
            )
            
            # Force update the annual insurance value
            st.session_state.nm_data["annual_ins"] = st.session_state["temp_nm_monthly_ins"] * 12
            st.session_state["temp_nm_annual_ins"] = st.session_state.nm_data["annual_ins"]
            insurance = st.session_state.nm_data["annual_ins"]
        else:
            insurance = st.number_input(
                "**Annual Insurance ($)**",
                min_value=0.0001,
                step=100.0,
                key="temp_nm_annual_ins",
                on_change=lambda: update_nm_insurance_values("annual")
            )
            
            # Force update the monthly insurance value
            st.session_state.nm_data["monthly_ins"] = st.session_state["temp_nm_annual_ins"] / 12
            st.session_state["temp_nm_monthly_ins"] = st.session_state.nm_data["monthly_ins"]
            monthly_ins = st.session_state.nm_data["monthly_ins"]

    ###########################################################
    # Display Metrics Section
    ###########################################################

    st.write("")
    calc_col1, calc_col2, calc_col3 = st.columns([4, 2, 4])

    with calc_col2:
        # Initialize calculation flag if it doesn't exist
        if "show_new_mortgage_calcs" not in st.session_state:
            st.session_state.show_new_mortgage_calcs = False

        if st.button("**Calculate**", key="calculate_new_mortgage"):

            # 1. update all data from temp widgets to permanent storage
            # 2. run any necessary calculations
            # 3. store variables in CurrentMortgage class
            # 4. activate session_state.show_new_mortgage_calcs

            new_mortgage_run_calcs()

    #####################################################################################
    # tabbed metrics vs visualizations
    #####################################################################################

    metrics, payment, amort, growth, interest_breakdown, timeline = st.tabs(["Calculations","Payment Breakdown","Amortization","Equity Growth","Interest Analysis","Mortgage Timeline"])

    with metrics:
        if st.session_state.show_new_mortgage_calcs:
            try:
                # Attempt to get the current mortgage object
                # Either from the local variable (if just calculated) or from session state (if returning to page)
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        # No valid mortgage object found
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()  # Stop execution here to prevent errors
                    
                buff3, mid, buff4 = st.columns([6, 18, 6])

                with mid:
                    st.write("")
                    st.header("&ensp;:green[**Mortgage Calculations**]")

                loan_col, payment_col, other = st.columns([4,4,4])

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

                with other:
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
                    st.metric(
                        "**Est. Closing Costs (3%):**",
                        value=f"${NewMort.closing_costs:,.2f}"
                    )
                    st.write("")
                    st.metric(
                        "**Est. Initial Investment:**",
                        value=f"${NewMort.initial_investment:,.2f}"
                    )

                # Save to session state for use in other pages
                st.session_state["new_mortgage"] = NewMort

            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

    # Rest of your code for other tabs remains unchanged
    with payment:
        if st.session_state.show_new_mortgage_calcs:
            try:
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()
                create_single_mortgage_payment_breakdown(NewMort)
            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

    with amort:
        if st.session_state.show_new_mortgage_calcs:
            try:
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()
                create_single_mortgage_amortization_chart(NewMort)
            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

    with growth:
        if st.session_state.show_new_mortgage_calcs:
            try:
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()
                create_equity_growth_chart(NewMort)
            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

    with interest_breakdown:
        if st.session_state.show_new_mortgage_calcs:
            try:
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()
                create_interest_principal_ratio_chart(NewMort)
            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

    with timeline:
        if st.session_state.show_new_mortgage_calcs:
            try:
                if 'NewMort' not in locals():
                    if "new_mortgage" in st.session_state and st.session_state.new_mortgage is not None:
                        NewMort = st.session_state.new_mortgage
                    else:
                        st.warning("Please click Calculate to update the metrics.")
                        st.stop()
                create_mortgage_timeline_chart(NewMort)
            except NameError:
                st.warning("Please click Calculate to update the metrics.")
                st.stop()

with refinance:
    # Helper functions for refinance tab
    def update_rf_data(field):
        st.session_state.rf_data[field] = st.session_state[f"temp_rf_{field}"]

    def update_rf_tax_values(source):
        if source == "monthly":
            st.session_state.rf_data["monthly_tax"] = st.session_state["temp_rf_monthly_tax"]
            st.session_state.rf_data["annual_tax"] = st.session_state.rf_data["monthly_tax"] * 12
            st.session_state["temp_rf_annual_tax"] = st.session_state.rf_data["annual_tax"]
        elif source == "annual":
            st.session_state.rf_data["annual_tax"] = st.session_state["temp_rf_annual_tax"]
            st.session_state.rf_data["monthly_tax"] = st.session_state.rf_data["annual_tax"] / 12
            st.session_state["temp_rf_monthly_tax"] = st.session_state.rf_data["monthly_tax"]
        elif source == "toggle":
            if st.session_state.rf_data["is_monthly_tax"]:
                st.session_state["temp_rf_monthly_tax"] = st.session_state.rf_data["monthly_tax"]
            else:
                st.session_state["temp_rf_annual_tax"] = st.session_state.rf_data["annual_tax"]

    def update_rf_insurance_values(source):
        if source == "monthly":
            st.session_state.rf_data["monthly_ins"] = st.session_state["temp_rf_monthly_ins"]
            st.session_state.rf_data["annual_ins"] = st.session_state.rf_data["monthly_ins"] * 12
            st.session_state["temp_rf_annual_ins"] = st.session_state.rf_data["annual_ins"]
        elif source == "annual":
            st.session_state.rf_data["annual_ins"] = st.session_state["temp_rf_annual_ins"]
            st.session_state.rf_data["monthly_ins"] = st.session_state.rf_data["annual_ins"] / 12
            st.session_state["temp_rf_monthly_ins"] = st.session_state.rf_data["monthly_ins"]
        elif source == "toggle":
            if st.session_state.rf_data["is_monthly_ins"]:
                st.session_state["temp_rf_monthly_ins"] = st.session_state.rf_data["monthly_ins"]
            else:
                st.session_state["temp_rf_annual_ins"] = st.session_state.rf_data["annual_ins"]

    st.write("Configure your refinance scenario below. This will use your current property value and loan balance.")
    st.write("")
    
    col1, buff1, col2, buff2, col3 = st.columns([5, 0.5, 8, 0.5, 6])

    # Left column - basic loan details
    with col1:
        st.write("")
        st.write("")
        
        rate = st.number_input(
            "**New Interest Rate (%)**",
            min_value=0.0001,
            step=0.005,
            format="%0.3f",
            key="temp_rf_rate",
            on_change=lambda: update_rf_data("rate"),
            help="Interest rate for the new refinanced loan"
        )
        
        st.write("")
        
        term = st.number_input(
            "**New Loan Term (years)**",
            min_value=1,
            key="temp_rf_term",
            on_change=lambda: update_rf_data("term"),
            help="Length of the new loan term"
        )
        
        st.write("")
        
        current_balance = st.number_input(
            "**Current Loan Balance ($)**",
            min_value=0.0,
            step=1000.0,
            key="temp_rf_current_loan_balance",
            on_change=lambda: update_rf_data("current_loan_balance"),
            help="Your current mortgage balance that will be paid off"
        )

    # Middle column - property and cash out
    with col2:
        st.write("")
        st.write("")
        
        current_value = st.number_input(
            "**Current Property Value ($)**",
            min_value=0.0001,
            step=5000.0,
            key="temp_rf_current_property_value",
            on_change=lambda: update_rf_data("current_property_value"),
            help="Current estimated value of your property"
        )
        
        st.write("")
        
        cash_out = st.number_input(
            "**Cash Out Amount ($)**",
            min_value=0.0,
            step=1000.0,
            key="temp_rf_cash_out_amount",
            on_change=lambda: update_rf_data("cash_out_amount"),
            help="Additional cash to borrow (0 for rate-and-term refinance)"
        )
        
        st.write("")
        
        closing_cost_pct = st.number_input(
            "**Closing Costs (%)**",
            min_value=1.0,
            max_value=10.0,
            step=0.1,
            format="%.1f",
            key="temp_rf_closing_cost_percentage",
            on_change=lambda: update_rf_data("closing_cost_percentage"),
            help="Estimated closing costs as percentage of new loan amount"
        )
        
        st.write("")
        
        sqft = st.number_input(
            "**Square Footage**",
            min_value=0.0001,
            step=100.0,
            key="temp_rf_sqft",
            on_change=lambda: update_rf_data("sqft"),
            help="Property square footage (typically same as current)"
        )

    # Right column - taxes and insurance
    with col3:
        st.write("")
        
        is_monthly_tax = st.toggle(
            "Annual/Monthly Tax",
            key="temp_rf_is_monthly_tax",
            on_change=lambda: (update_rf_data("is_monthly_tax"), update_rf_tax_values("toggle"))
        )

        if is_monthly_tax:
            monthly_tax = st.number_input(
                "**Monthly Tax ($)**",
                min_value=0.0,
                step=10.0,
                key="temp_rf_monthly_tax",
                on_change=lambda: update_rf_tax_values("monthly")
            )
            st.session_state.rf_data["annual_tax"] = st.session_state["temp_rf_monthly_tax"] * 12
            tax = st.session_state.rf_data["annual_tax"]
        else:
            tax = st.number_input(
                "**Annual Tax ($)**",
                min_value=0.0,
                step=100.0,
                key="temp_rf_annual_tax",
                on_change=lambda: update_rf_tax_values("annual")
            )
            st.session_state.rf_data["monthly_tax"] = st.session_state["temp_rf_annual_tax"] / 12

        is_monthly_ins = st.toggle(
            "Annual/Monthly Ins",
            key="temp_rf_is_monthly_ins",
            on_change=lambda: (update_rf_data("is_monthly_ins"), update_rf_insurance_values("toggle"))
        )

        if is_monthly_ins:
            monthly_ins = st.number_input(
                "**Monthly Insurance ($)**",
                min_value=0.0,
                step=10.0,
                key="temp_rf_monthly_ins",
                on_change=lambda: update_rf_insurance_values("monthly")
            )
            st.session_state.rf_data["annual_ins"] = st.session_state["temp_rf_monthly_ins"] * 12
            insurance = st.session_state.rf_data["annual_ins"]
        else:
            insurance = st.number_input(
                "**Annual Insurance ($)**",
                min_value=0.0,
                step=100.0,
                key="temp_rf_annual_ins",
                on_change=lambda: update_rf_insurance_values("annual")
            )
            st.session_state.rf_data["monthly_ins"] = st.session_state["temp_rf_annual_ins"] / 12
        
        st.write("")
        
        prin = st.number_input(
            "**Extra Monthly Principal ($)**",
            min_value=0.0,
            step=100.0,
            key="temp_rf_prin",
            on_change=lambda: update_rf_data("prin")
        )
        
        prepay = st.number_input(
            "**Prepay Periods (months)**",
            min_value=0,
            step=1,
            key="temp_rf_prepay",
            on_change=lambda: update_rf_data("prepay")
        )

    ###########################################################
    # Calculate Button and Results
    ###########################################################
    
    st.write("")
    calc_col1, calc_col2, calc_col3 = st.columns([4, 2, 4])

    with calc_col2:
        if "show_refinance_calcs" not in st.session_state:
            st.session_state.show_refinance_calcs = False

        if st.button("**Calculate Refinance**", key="calculate_refinance"):
            refinance_run_calcs()

    ###########################################################
    # Display Refinance Results
    ###########################################################

    metrics, payment, amort, growth, interest_breakdown, timeline = st.tabs([
        "Calculations", "Payment Breakdown", "Amortization", 
        "Equity Growth", "Interest Analysis", "Mortgage Timeline"
    ])

    with metrics:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                    
                buff3, mid, buff4 = st.columns([6, 18, 6])

                with mid:
                    st.write("")
                    st.header("&ensp;:green[**Refinance Calculations**]")

                loan_col, payment_col, other = st.columns([4, 4, 4])

                with loan_col: 
                    st.subheader("**Loan Metrics:**", divider="green")
                    st.metric(
                        "**New Loan Amount:**",
                        value=f"${RefinanceScen.loan_amount:,.2f}"
                    )
                    st.metric(
                        "**Loan-to-Value Ratio:**",
                        value=f"{RefinanceScen.loan_to_value:.1%}"
                    )
                    st.metric(
                        "**Equity After Refinance:**",
                        value=f"${RefinanceScen.equity_after_refinance:,.2f}"
                    )

                with payment_col:
                    st.subheader("**Payment Metrics:**", divider="green")
                    st.metric(
                        "**New Monthly Payment:**",
                        value=f"${RefinanceScen.total_pmt:,.2f}"
                    )
                    st.metric(
                        "**Estimated Monthly PMI:**",
                        value=f"${RefinanceScen.monthly_pmi:,.2f}"
                    )
                    st.metric(
                        "**PMI Payment Months:**",
                        value=f"{RefinanceScen.pmi_periods_remaining()}"
                    )

                with other:
                    st.subheader("**Financial Impact:**", divider="green")
                    st.metric(
                        "**Closing Costs:**",
                        value=f"${RefinanceScen.closing_costs:,.2f}"
                    )
                    if RefinanceScen.cash_out_amount > 0:
                        st.metric(
                            "**Net Cash to You:**",
                            value=f"${RefinanceScen.net_cash_to_borrower:,.2f}"
                        )
                    st.metric(
                        "**Property Value/SqFt:**",
                        value=f"${RefinanceScen.price_per_sqft:,.0f}"
                    )

                # Save to session state for comparison
                st.session_state["refinance_scenario"] = RefinanceScen

            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()

    # Other tabs use the same visualization functions as new mortgage
    with payment:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                create_single_mortgage_payment_breakdown(RefinanceScen)
            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()

    with amort:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                create_single_mortgage_amortization_chart(RefinanceScen)
            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()

    with growth:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                create_equity_growth_chart(RefinanceScen)
            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()

    with interest_breakdown:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                create_interest_principal_ratio_chart(RefinanceScen)
            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()

    with timeline:
        if st.session_state.show_refinance_calcs:
            try:
                if 'RefinanceScen' not in locals():
                    if "refinance_scenario" in st.session_state and st.session_state.refinance_scenario is not None:
                        RefinanceScen = st.session_state.refinance_scenario
                    else:
                        st.warning("Please click Calculate Refinance to update the metrics.")
                        st.stop()
                create_mortgage_timeline_chart(RefinanceScen)
            except NameError:
                st.warning("Please click Calculate Refinance to update the metrics.")
                st.stop()