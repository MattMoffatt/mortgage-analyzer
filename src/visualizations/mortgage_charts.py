import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from src.models.mortgage_classes import CurrentMortgage, NewMortgageScenario

#######################################################################
# Comparison visualizations (combination of Streamlit native and Altair)
#######################################################################

def create_monthly_payment_comparison(current_mortgage, new_mortgage):
    """
    Creates a bar chart comparing the monthly payments of both mortgages.
    Uses Matplotlib for more control over styling with a dark theme.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
    """
    # Prepare the data
    categories = ["Principal & Interest", "Taxes", "Insurance", "PMI", "Extra Principal", "Total Payment"]
    current_values = [
        current_mortgage.principal_and_interest,
        current_mortgage.monthly_tax,
        current_mortgage.monthly_ins,
        current_mortgage.monthly_pmi,
        current_mortgage.extra_principal,
        current_mortgage.total_pmt
    ]
    new_values = [
        new_mortgage.principal_and_interest,
        new_mortgage.monthly_tax,
        new_mortgage.monthly_ins,
        new_mortgage.monthly_pmi,
        new_mortgage.extra_principal,
        new_mortgage.total_pmt
    ]
    
    # Set up the matplotlib figure with dark theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0E1117')
    ax.set_facecolor('#0E1117')
    
    # Define bar positions
    x = np.arange(len(categories))
    width = 0.35
    
    # Create the bars
    rects1 = ax.bar(x - width/2, current_values, width, label='Current', color='#87CEFA')  # Light blue
    rects2 = ax.bar(x + width/2, new_values, width, label='New', color='#1E90FF')   # Darker blue
    
    # Add labels, title and custom x-axis tick labels
    ax.set_xlabel('Payment Components', color='white', fontsize=14, fontweight='bold')
    ax.set_ylabel('Amount ($)', color='white', fontsize=14, fontweight='bold')
    ax.set_title('Monthly Payment Comparison', color='white', fontsize=18, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right', color='white', fontsize=12)
    
    # Make y-axis ticks larger and bolder
    ax.tick_params(axis='y', colors='white', labelsize=12)
    
    # Add horizontal gridlines only
    ax.grid(axis='y', linestyle='--', alpha=0.4, color='#888888')
    
    # Add value labels on top of bars - make them larger and with shadow effect for visibility
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            # Add a slight shadow/outline effect for better visibility
            for xoffset, yoffset in [(-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)]:
                ax.annotate(f'${height:,.0f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(xoffset, 3 + yoffset),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            color='black', fontsize=11, alpha=0.7)
            
            # Main label
            ax.annotate(f'${height:,.0f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        color='white', fontsize=11, fontweight='bold')
    
    add_labels(rects1)
    add_labels(rects2)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'${int(x):,}'))
    
    # Remove all spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add a legend with border - make it larger and more visible
    legend = ax.legend(framealpha=0.9, facecolor='#0E1117', edgecolor='#888888', 
                       labelcolor='white', fontsize=12, frameon=True)
    
    # Adjust layout
    fig.tight_layout()
    
    # Display the chart
    st.pyplot(fig)
    
    # Calculate differences
    differences = [n - c for n, c in zip(new_values, current_values)]
    
    # Add a descriptive table for exact values
    st.write("Monthly Payment Breakdown (exact values):")
    
    # Create table data
    table_data = pd.DataFrame({
        "Component": categories,
        "Current": [f"${v:,.2f}" for v in current_values],
        "New": [f"${v:,.2f}" for v in new_values],
    })
    
    # Add formatted differences with indicators
    indicators = []
    for diff in differences:
        if diff > 0:
            indicator = "‼️"  # For increases
        elif diff < 0:
            indicator = "✅"  # For decreases
        else:
            indicator = "😐"  # For no change
        
        indicators.append(f"${diff:,.2f} {indicator}")
    
    table_data["Difference"] = indicators
    
    # Display the table
    st.table(table_data)

def create_amortization_comparison(current_mortgage, new_mortgage):
    """
    Creates a line chart comparing the loan balances over time.
    Streamlit's line chart works well for this visualization.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
    """
    # Get amortization schedules
    current_schedule = current_mortgage.amortization_schedule()
    new_schedule = new_mortgage.amortization_schedule()
    
    # Calculate years for display
    current_schedule["Year"] = (current_schedule["month"] / 12).apply(lambda x: round(x, 1))
    new_schedule["Year"] = (new_schedule["month"] / 12).apply(lambda x: round(x, 1))
    
    # Make sure we have same length if possible
    max_years = max(current_schedule["Year"].max(), new_schedule["Year"].max())
    
    # Create the comparison dataframe with fixed points
    years = np.arange(0, max_years + 0.1, 0.1)
    comparison_df = pd.DataFrame(index=years)
    
    # Handle duplicates by aggregating (taking the last value for each Year)
    current_data = current_schedule.groupby("Year")["balance"].last()
    new_data = new_schedule.groupby("Year")["balance"].last()
    
    # Reindex to match our comparison dataframe's index
    current_data = current_data.reindex(years, method='ffill')
    new_data = new_data.reindex(years, method='ffill')
    
    # Add the data to the comparison dataframe
    comparison_df["Current Mortgage"] = current_data
    comparison_df["New Mortgage"] = new_data
    
    # Display chart
    st.line_chart(comparison_df)
    
    # Show key details
    current_years = current_mortgage.periods_remaining / 12
    new_years = new_mortgage.periods_remaining / 12
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Mortgage Term", f"{current_years:.1f} years")
    with col2:
        st.metric("New Mortgage Term", f"{new_years:.1f} years")

def create_equity_buildup_chart(current_mortgage, new_mortgage, years=30):
    """
    Creates a line chart showing equity buildup over time for both mortgages.
    Streamlit's line chart works well for this visualization.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
        years (int): Number of years to project
    """
    # Create data points for each year
    equity_data = pd.DataFrame(index=range(years + 1))
    
    # Calculate equity for current mortgage
    equity_data["Current Mortgage"] = [current_mortgage.estimate_equity_at_year(year) for year in range(years + 1)]
    
    # Calculate equity for new mortgage
    equity_data["New Mortgage"] = [new_mortgage.estimate_equity_at_year(year) for year in range(years + 1)]
    
    # Display chart
    st.subheader("Equity Buildup Over Time (3% Annual Appreciation)")
    st.line_chart(equity_data)
    
    # Show key details
    five_year_current = current_mortgage.estimate_equity_at_year(5)
    five_year_new = new_mortgage.estimate_equity_at_year(5)
    
    ten_year_current = current_mortgage.estimate_equity_at_year(10)
    ten_year_new = new_mortgage.estimate_equity_at_year(10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("5-Year Equity (Current)", f"${five_year_current:,.2f}")
        st.metric("10-Year Equity (Current)", f"${ten_year_current:,.2f}")
    
    with col2:
        st.metric("5-Year Equity (New)", f"${five_year_new:,.2f}")
        st.metric("10-Year Equity (New)", f"${ten_year_new:,.2f}")

def create_interest_paid_comparison(current_mortgage, new_mortgage):
    """
    Creates a bar chart comparing total interest paid over the life of the loans.
    Streamlit's bar chart works well for this visualization.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
    """
    # Calculate total interest for current mortgage
    current_schedule = current_mortgage.amortization_schedule()
    current_total_interest = current_schedule["interest"].sum()
    current_total_principal = current_mortgage.loan_amount
    
    # Calculate total interest for new mortgage
    new_schedule = new_mortgage.amortization_schedule()
    new_total_interest = new_schedule["interest"].sum()
    new_total_principal = new_mortgage.loan_amount
    
    # Create DataFrame for the chart
    data = pd.DataFrame({
        "Total Interest": [current_total_interest, new_total_interest]
    }, index=["Current Mortgage", "New Mortgage"])
    
    # Display chart
    st.subheader("Total Interest Paid Over Life of Loan")
    st.bar_chart(data)
    
    # Show exact values and difference
    interest_diff = new_total_interest - current_total_interest
    interest_diff_perc = (interest_diff - current_total_interest) / current_total_interest * 100
    interest_string_higher = f"{interest_diff_perc:.2f}% higher"
    interest_string_lower = f"{interest_diff_perc:.2f}% lower"
    
    interest_delta = interest_string_higher if interest_diff > 0 else interest_string_lower

    interest_diff_postive_string = f"+${abs(interest_diff):,.2f}"
    interest_diff_negative_string = f"-${abs(interest_diff):,.2f}"

    current_ratio = current_total_interest / current_total_principal
    new_ratio = new_total_interest / new_total_principal
    ratio_diff = new_ratio - current_ratio
    ratio_diff_perc = ratio_diff / current_ratio * 100
    ratio_string_higher = f"{ratio_diff_perc:.2f}% higher"
    ratio_string_lower = f"{ratio_diff_perc:.2f}% lower"

    ratio_delta = ratio_string_higher if ratio_diff > 0 else ratio_string_lower

    ratio_diff_postive_string = f"+{abs(ratio_diff):.2f}x"
    ratio_diff_negative_string = f"-{abs(ratio_diff):.2f}x"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Mortgage Interest", f"${current_total_interest:,.2f}")
        st.write("")
        st.metric(
        "Current Interest to Principal Ratio", 
        f"{current_ratio:.2f}x",
        help="For every $1 of principal paid, you will have paid this much in interest"
        )
    with col2:
        st.metric("New Mortgage Interest", f"${new_total_interest:,.2f}")
        st.write("")
        st.metric(
        "New Interest to Principal Ratio", 
        f"{new_ratio:.2f}x",
        help="For every $1 of principal paid, you will have paid this much in interest"
        )
    with col3:
        st.metric(
            "Difference", 
            f"{interest_diff_postive_string if interest_diff > 0 else interest_diff_negative_string}",
            interest_delta, 
            delta_color="inverse"
        )
        st.metric(
            "Difference", 
            f"{ratio_diff_postive_string if ratio_diff > 0 else ratio_diff_negative_string}", 
            ratio_delta, 
            delta_color="inverse"
        )

def create_loan_term_comparison(current_mortgage, new_mortgage):
    """
    Creates a horizontal bar chart comparing the loan terms.
    This visualization requires more customization, so using Matplotlib via Streamlit.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
    """
    # Get end dates
    current_end = dt.strptime(current_mortgage.end_date, "%m/%d/%Y")
    new_end = dt.strptime(new_mortgage.end_date, "%m/%d/%Y")
    
    # Calculate years remaining for display
    current_years = current_mortgage.periods_remaining / 12
    new_years = new_mortgage.periods_remaining / 12
    
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Create the horizontal bar chart
    y_pos = [0, 1]
    years = [current_years, new_years]
    labels = ["Current Mortgage", "New Mortgage"]
    
    # Create bars with colors that match the theme
    bars = ax.barh(y_pos, years, height=0.6, color=['#8A2BE2', '#32CD32'])
    
    # Add labels and values on the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width + 0.5
        end_date = current_end if i == 0 else new_end
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
                f"{width:.1f} years (ends {end_date.strftime('%m/%d/%Y')})", 
                va='center')
    
    # Set chart properties
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Years Remaining')
    ax.set_title('Loan Term Comparison')
    
    # Display in Streamlit
    st.pyplot(fig)

def create_breakeven_chart(current_mortgage, new_mortgage):
    """
    Creates a line chart showing the cumulative cost difference between mortgages.
    This requires custom calculations and annotations, using Matplotlib.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
    """
    # Define time period (10 years is usually sufficient to find breakeven)
    months = 10 * 12
    
    # Calculate monthly costs for each mortgage
    cumulative_data = []
    
    # Assume closing costs for new mortgage (typically 2-5% of loan amount)
    closing_costs = new_mortgage.loan_amount * 0.03  # 3% of loan amount as closing costs
    
    cumulative_difference = closing_costs  # Start with closing costs as initial difference
    
    for month in range(0, months + 1):
        # Monthly payment for current mortgage
        current_payment = current_mortgage.total_pmt
        
        # Monthly payment for new mortgage
        new_payment = new_mortgage.total_pmt
        
        # Monthly savings or cost (positive means current is more expensive)
        monthly_difference = current_payment - new_payment
        
        # Accumulate the difference (only after month 0)
        if month > 0:
            cumulative_difference -= monthly_difference
        
        # Get the year for display
        year = month / 12
        
        cumulative_data.append({
            "Month": month,
            "Year": year,
            "Cumulative Difference": cumulative_difference
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(cumulative_data)
    
    # Find breakeven point (if it exists)
    breakeven_point = None
    for i in range(1, len(df)):
        if (df.iloc[i-1]["Cumulative Difference"] > 0 and df.iloc[i]["Cumulative Difference"] <= 0) or \
           (df.iloc[i-1]["Cumulative Difference"] <= 0 and df.iloc[i]["Cumulative Difference"] > 0):
            # Linear interpolation for more accurate breakeven point
            y1 = df.iloc[i-1]["Cumulative Difference"]
            y2 = df.iloc[i]["Cumulative Difference"]
            x1 = df.iloc[i-1]["Year"]
            x2 = df.iloc[i]["Year"]
            
            # Solving for x where y = 0
            breakeven_point = x1 - y1 * (x2 - x1) / (y2 - y1)
            break
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the line
    ax.plot(df["Year"], df["Cumulative Difference"], color='#FF4500', linewidth=2)
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.7)
    
    # Add breakeven point if it exists
    if breakeven_point is not None and breakeven_point <= 10:
        ax.plot([breakeven_point], [0], 'ro', markersize=8)
        ax.annotate(f'Breakeven: {breakeven_point:.2f} years',
                    xy=(breakeven_point, 0),
                    xytext=(breakeven_point + 0.5, -closing_costs/4),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'${int(x):,}'))
    
    # Set labels and title
    ax.set_xlabel('Years')
    ax.set_ylabel('Cost Difference ($)')
    ax.set_title('Refinance Breakeven Analysis (including ~3% closing costs)')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add explanation of the chart
    ax.text(0.5, -closing_costs * 0.8, 
            'Above line (positive): Cost of refinancing\nBelow line (negative): Savings from refinancing',
            horizontalalignment='center', fontsize=9)
    
    # Set axis limits
    ax.set_xlim(0, 10)
    
    # Display in Streamlit
    st.pyplot(fig)
    
    # Add explanation text
    if breakeven_point is not None and breakeven_point <= 10:
        st.info(f"💡 With estimated closing costs of ${closing_costs:,.2f} (3% of new loan amount), "
                f"you would break even after **{breakeven_point:.2f} years** "
                f"({int(breakeven_point * 12)} months).")
    elif breakeven_point is not None:
        st.warning(f"⚠️ With estimated closing costs of ${closing_costs:,.2f}, "
                   f"you would break even after {breakeven_point:.2f} years. "
                   f"This is beyond the 10-year period shown on the chart.")
    else:
        st.warning("⚠️ Based on the payment difference, you may not break even within a reasonable timeframe.")

def create_mortgage_comparison_dashboard(current_mortgage, new_mortgage):
    """
    Creates a key metrics comparison table.
    
    Args:
        current_mortgage (CurrentMortgage): Current mortgage object
        new_mortgage (NewMortgageScenario): New mortgage scenario object
        
    Returns:
        pandas.DataFrame: Comparison table data
    """
    # Calculate key metrics
    metrics = {
        "Monthly Payment": {
            "Current": current_mortgage.total_pmt,
            "New": new_mortgage.total_pmt,
            "Difference": new_mortgage.total_pmt - current_mortgage.total_pmt,
            "Format": "${:,.2f}",
            "Better": "lower"
        },
        "Principal & Interest": {
            "Current": current_mortgage.principal_and_interest,
            "New": new_mortgage.principal_and_interest,
            "Difference": new_mortgage.principal_and_interest - current_mortgage.principal_and_interest,
            "Format": "${:,.2f}",
            "Better": "lower"
        },
        "Property Value": {
            "Current": current_mortgage.price,
            "New": new_mortgage.price,
            "Difference": new_mortgage.price - current_mortgage.price,
            "Format": "${:,.2f}",
            "Better": "higher"
        },
        "Loan Balance": {
            "Current": current_mortgage.loan_amount,
            "New": new_mortgage.loan_amount,
            "Difference": new_mortgage.loan_amount - current_mortgage.loan_amount,
            "Format": "${:,.2f}",
            "Better": "lower"
        },
        "Equity": {
            "Current": current_mortgage.equity_value,
            "New": new_mortgage.price - new_mortgage.loan_amount,
            "Difference": (new_mortgage.price - new_mortgage.loan_amount) - current_mortgage.equity_value,
            "Format": "${:,.2f}",
            "Better": "higher"
        },
        "Interest Rate": {
            "Current": current_mortgage.rate,
            "New": new_mortgage.rate,
            "Difference": new_mortgage.rate - current_mortgage.rate,
            "Format": "{:.3f}%",
            "Better": "lower"
        },
        "Loan Term Remaining": {
            "Current": current_mortgage.periods_remaining / 12,
            "New": new_mortgage.periods_remaining / 12,
            "Difference": (new_mortgage.periods_remaining / 12) - (current_mortgage.periods_remaining / 12),
            "Format": "{:.1f} years",
            "Better": "context"
        },
        "Monthly PMI": {
            "Current": current_mortgage.monthly_pmi,
            "New": new_mortgage.monthly_pmi,
            "Difference": new_mortgage.monthly_pmi - current_mortgage.monthly_pmi,
            "Format": "${:,.2f}",
            "Better": "lower"
        },
        "PMI Periods Remaining": {
            "Current": current_mortgage.pmi_periods_remaining(),
            "New": new_mortgage.pmi_periods_remaining(),
            "Difference": new_mortgage.pmi_periods_remaining() - current_mortgage.pmi_periods_remaining(),
            "Format": "{:,.0f} months",
            "Better": "lower"
        }
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(metrics).T.reset_index()
    df.columns = ["Metric", "Current", "New", "Difference", "Format", "Better"]
    
    return df

#######################################################################
# Single mortgage visualizations (using native Streamlit charts)
#######################################################################

def create_single_mortgage_payment_breakdown(mortgage):
    """
    Creates a pie chart showing the breakdown of a single mortgage's monthly payment.
    Uses matplotlib's pie chart via st.pyplot with dark theme styling.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
    """
    # Create data for the payment breakdown
    payment_data = {}
    
    # Add standard components
    payment_data["Principal & Interest"] = mortgage.principal_and_interest
    payment_data["Property Tax"] = mortgage.monthly_tax
    payment_data["Insurance"] = mortgage.monthly_ins
    
    # Add PMI if it exists
    if mortgage.monthly_pmi > 0:
        payment_data["PMI"] = mortgage.monthly_pmi
    
    # Add extra principal if it exists
    if mortgage.extra_principal > 0:
        payment_data["Extra Principal"] = mortgage.extra_principal
    
    # Display the pie chart using matplotlib
    st.subheader("Monthly Payment Breakdown")
    
    # Calculate percentages for display
    total = sum(payment_data.values())
    
    # Create the pie chart with matplotlib
    plt.style.use('dark_background')  # Set dark theme
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0E1117')  # Match Streamlit's dark background
    
    # Define vibrant colors that stand out on dark background
    colors = ["#8A2BE2", "#00CED1", "#FF6347", "#32CD32", "#FFD700"]
    
    # Create labels with values and percentages
    labels = [f"{k}: ${v:.2f} ({v/total*100:.1f}%)" for k, v in payment_data.items()]
    
    # Create the pie chart
    wedges, texts = ax.pie(
        payment_data.values(),
        labels=None,  # We'll add custom legend instead
        autopct=None,
        startangle=90,
        colors=colors[:len(payment_data)],
        wedgeprops={'edgecolor': '#1E1E1E'}  # Add dark edge for contrast
    )
    
    # Add a circle at the center to make it look like a donut chart
    centre_circle = plt.Circle((0, 0), 0.5, fc='#0E1117')  # Dark center
    ax.add_patch(centre_circle)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Add title inside the donut
    ax.text(0, 0, f"Total\n${total:.2f}", ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')  # White text
    
    # Add a custom legend with white text
    legend = ax.legend(
        wedges,
        labels,
        title="Payment Components",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    
    # Style the legend text to be white
    legend.get_title().set_color('white')
    for text in legend.get_texts():
        text.set_color('white')
    
    # Style the figure
    ax.set_facecolor('#0E1117')  # Background color for the plot area
    
    # Display the chart
    st.pyplot(fig)
    
    # Reset style for other plots
    plt.style.use('default')
    
    # Show total as a metric
    st.metric("Total Monthly Payment", f"${total:.2f}")
    
    # Display as a table too (for exact values)
    breakdown_df = pd.DataFrame({
        "Amount": list(payment_data.values()),
        "Percentage": [f"{v/total*100:.1f}%" for v in payment_data.values()]
    }, index=list(payment_data.keys()))
    
    st.write("Payment Components:")
    breakdown_df["Amount"] = breakdown_df["Amount"].apply(lambda x: f"${x:.2f}")
    st.table(breakdown_df)

def create_single_mortgage_amortization_chart(mortgage):
    """
    Creates charts showing the amortization schedule for a single mortgage.
    Uses Streamlit's native charts for simplicity.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
    """
    # Get amortization schedule
    schedule = mortgage.amortization_schedule()
    
    # Add year column for improved readability
    schedule["Year"] = (schedule["month"] / 12).apply(lambda x: round(x, 1))
    
    # Create balance chart
    st.subheader("Loan Balance Over Time")
    
    # Set year as index for the line chart
    balance_data = schedule.set_index("Year")[["balance"]]
    balance_data.columns = ["Loan Balance"]
    st.line_chart(balance_data)
    
    # Create principal vs interest chart
    st.subheader("Principal vs Interest Payments")
    
    # Group by year for clarity
    yearly_data = schedule.groupby(schedule["month"] // 12)[["principal", "interest"]].sum()
    # Keep the index numerical (add 1 to make it 1-based rather than 0-based)
    yearly_data.index = yearly_data.index + 1
    yearly_data.columns = ["Principal", "Interest"]
    
    st.bar_chart(yearly_data)
    
    # Calculate totals
    total_principal = schedule["principal"].sum()
    total_interest = schedule["interest"].sum()
    
    # Show totals
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Principal Paid", f"${total_principal:,.2f}")
    
    with col2:
        st.metric("Total Interest Paid", f"${total_interest:,.2f}")
    
    with col3:
        st.metric(
            "Interest to Principal Ratio", 
            f"{total_interest / total_principal:.2f}x",
            help="For every $1 of principal paid, you will have paid this much in interest"
        )

def create_equity_growth_chart(mortgage, years=30):
    """
    Creates a line chart showing equity growth for a single mortgage.
    Uses Streamlit's native line chart for simplicity.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
        years: Number of years to project
    """
    # Create data for equity growth
    equity_data = []
    loan_paydown_data = []
    appreciation_data = []
    
    # Get starting values
    starting_balance = mortgage.loan_amount
    starting_value = mortgage.price
    
    for year in range(years + 1):
        # Calculate equity components
        remaining_balance = mortgage._calculate_remaining_balance_at_year(year)
        future_value = mortgage.estimate_value_at_year(year)
        
        # Calculate the components
        loan_paydown = starting_balance - remaining_balance
        appreciation = future_value - starting_value
        equity = future_value - remaining_balance
        
        # Store the data
        equity_data.append(equity)
        loan_paydown_data.append(loan_paydown)
        appreciation_data.append(appreciation)
    
    # Create DataFrame for the chart
    df = pd.DataFrame({
        "Total Equity": equity_data,
        "Loan Paydown": loan_paydown_data,
        "Home Appreciation": appreciation_data
    }, index=range(years + 1))
    
    # Display the chart
    st.subheader("Equity Growth Over Time (3% Annual Appreciation)")
    st.line_chart(df)
    
    # Show key milestones
    year_5_equity = mortgage.estimate_equity_at_year(5)
    year_10_equity = mortgage.estimate_equity_at_year(10)
    year_30_equity = mortgage.estimate_equity_at_year(30)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("5-Year Equity", f"${year_5_equity:,.2f}")
    
    with col2:
        st.metric("10-Year Equity", f"${year_10_equity:,.2f}")

    with col3:
        st.metric("30-Year Equity", f"${year_30_equity:,.2f}")
    
def create_interest_principal_ratio_chart(mortgage):
    """
    Creates a horizontal bar chart showing interest vs. principal over the loan term.
    Uses matplotlib through Streamlit with dark theme styling.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
    """
    # Get amortization schedule
    schedule = mortgage.amortization_schedule()
    
    # Calculate totals
    total_interest = schedule["interest"].sum()
    total_principal = mortgage.loan_amount
    total_paid = total_interest + total_principal
    
    # Set dark theme
    plt.style.use('dark_background')
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 4), facecolor='#0E1117')
    
    # Create horizontal bars
    y_pos = [0, 1]
    values = [total_principal, total_interest]
    labels = ["Principal", "Interest"]
    colors = ["#8A2BE2", "#FF6347"]  # Purple for principal, red-orange for interest
    
    # Create the bars
    bars = ax.barh(y_pos, values, height=0.5, color=colors)
    
    # Add labels and percentages
    for i, bar in enumerate(bars):
        width = bar.get_width()
        percentage = (width / total_paid) * 100
        label_x_pos = width / 2
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
                f"${width:,.2f} ({percentage:.1f}%)", 
                ha='center', va='center', color='white', fontweight='bold')
    
    # Set chart properties
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, color='white')
    ax.set_xlabel('Amount ($)', color='white')
    ax.set_title(f'Total Principal vs. Interest Paid Over Loan Term (${total_paid:,.2f})', 
                 color='white', fontsize=14)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'${int(x):,}'))
    
    # Customize grid and background
    ax.set_facecolor('#0E1117')  # Dark background
    ax.tick_params(colors='white')  # White tick labels
    ax.spines['bottom'].set_color('#666666')
    ax.spines['top'].set_color('#666666')
    ax.spines['right'].set_color('#666666')
    ax.spines['left'].set_color('#666666')
    
    # Display in Streamlit
    st.pyplot(fig)
    
    # Reset style for other plots
    plt.style.use('default')
    
    # Show interest to principal ratio
    st.metric(
        "Interest to Principal Ratio", 
        f"{total_interest / total_principal:.2f}x",
        help="For every $1 of principal paid, you will have paid this much in interest"
    )

def create_mortgage_timeline_chart(mortgage):
    """
    Creates a timeline showing key milestones in the mortgage.
    Uses matplotlib through Streamlit with dark theme styling.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
    """
    # Calculate key milestones
    milestones = []
    
    # Get start and end dates
    if hasattr(mortgage, 'loan_begin_date'):
        start_date = mortgage.loan_begin_date
    else:
        # For NewMortgageScenario, use current date
        start_date = dt.now()
    
    # End date is always available
    end_date_str = mortgage.end_date
    end_date = dt.strptime(end_date_str, "%m/%d/%Y")
    
    # Add start and end milestones
    milestones.append({
        "Date": start_date,
        "Year": 0,
        "Event": "Loan Start", 
        "Description": f"Loan amount: ${mortgage.loan_amount:,.2f}"
    })
    
    milestones.append({
        "Date": end_date,
        "Year": (end_date - start_date).days / 365.25,
        "Event": "Loan Payoff", 
        "Description": f"After {mortgage.periods_remaining / 12:.1f} years"
    })
    
    # Calculate when loan is 50% paid off
    half_payoff_period = 0
    running_balance = mortgage.loan_amount
    half_balance = mortgage.loan_amount / 2
    
    schedule = mortgage.amortization_schedule()
    half_paid_row = schedule[schedule["balance"] <= half_balance].iloc[0] if not schedule[schedule["balance"] <= half_balance].empty else None
    
    if half_paid_row is not None:
        half_paid_month = half_paid_row["month"]
        half_paid_years = half_paid_month / 12
        half_paid_date = start_date + relativedelta(months=int(half_paid_month))
        
        milestones.append({
            "Date": half_paid_date,
            "Year": half_paid_years,
            "Event": "50% Paid Off",
            "Description": f"After {half_paid_years:.1f} years"
        })
    
    # Add PMI removal date if applicable
    pmi_periods = mortgage.pmi_periods_remaining()
    if pmi_periods > 0:
        pmi_removal_date = start_date + relativedelta(months=int(pmi_periods))
        pmi_years = pmi_periods / 12
        
        milestones.append({
            "Date": pmi_removal_date,
            "Year": pmi_years,
            "Event": "PMI Removal",
            "Description": f"After {pmi_years:.1f} years"
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(milestones)
    
    # Sort by date
    df = df.sort_values("Date")
    
    # Set dark theme
    plt.style.use('dark_background')
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0E1117')
    
    # Plot each milestone
    colors = {
        "Loan Start": "#32CD32",      # Green
        "50% Paid Off": "#a22be2",    # Purple
        "PMI Removal": "#FF6347",     # Red-orange
        "Loan Payoff": "#4682B4"      # Steel blue
    }
    
    # Create the timeline - use slightly brighter line color for visibility
    ax.plot([0, df["Year"].max()], [0, 0], color='#888888', alpha=0.5, linewidth=2)
    
    # Add each milestone
    for i, row in df.iterrows():
        color = colors.get(row["Event"], "#CCCCCC")  # Brighter default color
        ax.plot([row["Year"], row["Year"]], [-0.1, 0.1], color=color, linewidth=2)
        ax.plot(row["Year"], 0, 'o', markersize=10, color=color)
        
        # Add label and description with white text
        ax.annotate(
            f"{row['Event']}\n{row['Date'].strftime('%m/%d/%Y')}\n{row['Description']}",
            xy=(row["Year"], 0),
            xytext=(row["Year"], 0.2 + i % 2 * 0.2),  # Alternate text positions for readability
            ha='center',
            va='bottom',
            color=color,
            arrowprops=dict(arrowstyle='->', color=color)
        )
    
    # Set chart properties
    ax.set_ylim(-0.5, 1.0)
    ax.set_xlim(-0.5, df["Year"].max() + 0.5)
    ax.set_title('Mortgage Timeline Milestones', color='white', fontsize=14)
    ax.set_xlabel('Years', color='white')
    
    # Hide y-axis
    ax.get_yaxis().set_visible(False)
    
    # Remove spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('#666666')
    
    # Set background color
    ax.set_facecolor('#0E1117')
    
    # Add tick marks in white
    ax.tick_params(axis='x', colors='white')
    
    # Display in Streamlit
    st.pyplot(fig)
    
    # Reset style for other plots
    plt.style.use('default')
    
    # Add text explanation
    st.write("Key milestone dates:")
    for i, row in df.iterrows():
        st.write(f"• **{row['Event']}**: {row['Date'].strftime('%m/%d/%Y')} - {row['Description']}")

def create_single_mortgage_dashboard(mortgage):
    """
    Creates a comprehensive dashboard for a single mortgage with multiple visualizations.
    
    Args:
        mortgage: Either CurrentMortgage or NewMortgageScenario object
    """
    # Payment breakdown
    create_single_mortgage_payment_breakdown(mortgage)
    
    # Amortization
    create_single_mortgage_amortization_chart(mortgage)
    
    # Equity growth
    create_equity_growth_chart(mortgage)
    
    # Interest vs principal
    create_interest_principal_ratio_chart(mortgage)
    
    # Timeline
    create_mortgage_timeline_chart(mortgage)