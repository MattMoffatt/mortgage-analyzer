import streamlit as st

st.header("&ensp;&ensp;&ensp;&ensp;&ensp;:dollar::house: Mortgage Calculator App :house::dollar:", divider="violet")

st.subheader("This app helps you compare your current mortgage to new mortgage \
scenarios you are pursuing.")

st.subheader("&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;Navigation:", divider="grey")

col1, col2 = st.columns([2, 5])

# Initialize session state for mortgage objects
if "current_mortgage" not in st.session_state:
    st.session_state.current_mortgage = None
if "new_mortgage" not in st.session_state:
    st.session_state.new_mortgage = None

with col1:
    st.page_link("pages/01_💸_Current_Mortgage.py", label="💸 Current Mortgage")
    st.write("")
    st.page_link("pages/02_🆕_New_Scenario.py", label="🆕 New_Scenario")
    st.write("")
    st.page_link("pages/03_📈_Comparison.py", label="📈 Comparison")

with col2:
    st.write("input your current mortgage details")
    st.write("")
    st.write("select number of new mortgages (1-3) to review and input details")
    st.write("")
    st.write("review comparisons between current and new scenarios")

st.write("")
st.write("")
st.write("")
st.write("")

# &ensp; arguments added to center the link on the page

st.link_button("Original Repo Link", "https://github.com/MattMoffatt/mortgage-analyzer")

