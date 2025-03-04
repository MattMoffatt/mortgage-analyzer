import sys
import datetime as dt
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st

#Session state intitializations to persist data across the pages of the app.

#current_mortgage and new_mortgage classes will be created through the inputs
#from users of the app and used for comparisons in page 3 "📈 Comparison".

# Initialize session state for mortgage objects
if "current_mortgage" not in st.session_state:
    st.session_state.current_mortgage = None
if "new_mortgage" not in st.session_state:
    st.session_state.new_mortgage = None

# Initialize Current Mortgage inputs
if "cm_rate" not in st.session_state: 
    st.session_state.cm_rate = 5.5
if "cm_balance" not in st.session_state: 
    st.session_state.cm_balance = 300000.0
if "cm_origin" not in st.session_state: 
    st.session_state.cm_origin = 350000.0
if "cm_start_date" not in st.session_state: 
    st.session_state.cm_start_date = dt.datetime.now()
if "cm_sqft" not in st.session_state: 
    st.session_state.cm_sqft = 2000.0
if "cm_ppsqft" not in st.session_state: 
    st.session_state.cm_ppsqft = 170.0
if "cm_pmt" not in st.session_state: 
    st.session_state.cm_pmt = 1500.0
if "cm_pmi" not in st.session_state: 
    st.session_state.cm_pmi = 50.0
if "cm_term" not in st.session_state: 
    st.session_state.cm_term = 30

# tax can be annual or monthly
if "cm_is_monthly_tax_flag" not in st.session_state:
    st.session_state.cm_is_monthly_tax = False
if "cm_tax_annual" not in st.session_state: 
    st.session_state.cm_tax_annual = 2600.0
if "cm_tax_monthly" not in st.session_state: 
    st.session_state.cm_tax_monthly = st.session_state.cm_tax_annual / 12

# insurance can be annual or monthly
if "cm_is_monthly_ins_flag" not in st.session_state:
    st.session_state.cm_is_monthly_ins = False
if "cm_ins_annual" not in st.session_state: 
    st.session_state.cm_ins_annual = 2200.0
if "cm_ins_monthly" not in st.session_state:
    st.session_state.cm_ins_monthly = st.session_state.cm_ins_annual / 12

if "cm_prin" not in st.session_state: 
    st.session_state.cm_prin = 0.0
if "cm_prepay" not in st.session_state: 
    st.session_state.cm_prepay = 0


# Initialize New Mortgage inputs
if "nm_rate" not in st.session_state: 
    st.session_state.nm_rate = 5.5
if "nm_price" not in st.session_state: 
    st.session_state.nm_price = 300000.0
if "nm_sqft" not in st.session_state: 
    st.session_state.nm_sqft = 2000.0
if "nm_pmi" not in st.session_state: 
    st.session_state.nm_pmi = 50.0
if "nm_term" not in st.session_state: 
    st.session_state.nm_term = 30
if "nm_downpayment" not in st.session_state: 
    st.session_state.nm_downpayment = 60000.0
if "nm_downpayment_percent" not in st.session_state: 
    st.session_state.nm_downpayment_percent = 20.0
if "nm_is_not_percent" not in st.session_state: 
    st.session_state.nm_is_not_percent = False
if "nm_tax" not in st.session_state: 
    st.session_state.nm_tax = 2600.0
if "nm_insurance" not in st.session_state: 
    st.session_state.nm_insurance = 2200.0
if "nm_prin" not in st.session_state: 
    st.session_state.nm_prin = 0.0
if "nm_prepay" not in st.session_state: 
    st.session_state.nm_prepay = 0

home = st.Page("pages/00_🏡_Home_Page_(pun_intended).py")
pg1 = st.Page("pages/01_💸_Current_Mortgage.py")
pg2 = st.Page("pages/02_🆕_New_Scenario.py")
pg3 = st.Page("pages/03_📈_Comparison.py")

nav = st.navigation([home, pg1, pg2, pg3])

nav.run()