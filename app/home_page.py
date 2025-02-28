import streamlit as st

home = st.Page("pages/00_🏡_Home_Page_(pun_intended).py")

pg1 = st.Page("pages/01_💸_Current_Mortgage.py")
pg2 = st.Page("pages/02_🆕_New_Scenario.py")
pg3 = st.Page("pages/03_📈_Comparison.py")

nav = st.navigation([home, pg1, pg2, pg3])

nav.run()

