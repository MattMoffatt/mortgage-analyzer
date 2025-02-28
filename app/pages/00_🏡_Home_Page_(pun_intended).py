import streamlit as st



f"""
# :dollar::house: Mortgage Calculator App :house::dollar:

Use this app to help you compare your current mortgage to new mortgage
scenarios you are pursuing.

## &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;Navigation:
"""

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/01_💸_Current_Mortgage.py",label="💸 Current Mortgage")
    st.write("") 
    st.page_link("pages/02_🆕_New_Scenario.py",label="🆕 New_Scenario")
    st.write("") 
    st.page_link("pages/03_📈_Comparison.py",label="📈 Comparison")

with col2:
    st.write("input your current mortgage details\n")
    st.write("select number of new mortgages (1-3) to review and input details\n")
    st.write("review comparisons between current and new scenarios\n")

st.write("")
st.write("")
st.write("")
st.write("")

# &ensp; arguments added to center the link on the page

"""
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;
&ensp;&ensp;
[Original repo link](https://github.com/MattMoffatt/mortgage-analyzer)
"""