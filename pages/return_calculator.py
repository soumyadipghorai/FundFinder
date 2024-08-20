import streamlit as st 
from utils.calculate_return import CalculateReturns

st.title("Calculate returns") 
st.write("Enter mutual fund details to compute expected returns with accurate tax and expense deductions.")
st.write("")
col1, col2 = st.columns(2)
with col1 :
    p = st.number_input(label="Enter principle amount", min_value = 0)
    r = st.number_input(label="Enter returns of the fund", min_value = 0.000001, max_value = 100.0)
    n = st.number_input(label="Enter number of years", min_value = 0)
with col2 :
    s = st.number_input(label="Enter stamp duty of the fund", min_value = 0.0, max_value = 100.0)
    e = st.number_input(label="Enter expense ratio of the fund", min_value = 0.0, max_value = 100.0)
    s_type = st.radio(label="Enter investment type", options=['SIP', "Lumpsum"])
    
submit_button = st.button(label='submit')
if submit_button : 
    st.markdown("#### Results ")
    obj = CalculateReturns(
        Principle = p, returns = r, expense_ratio = e, 
        stamp_duty = s, num_years = n, investment_type = s_type
    )
    after_tax, before_tax = obj.calculate_tax()
    col1, col2 = st.columns(2)
    with col1 : 
        st.warning("Return after tax deduction : " + str(after_tax))
    with col2 :
        st.success("Return before tax deduction : " + str(before_tax)) 