import streamlit as st 
import pandas as pd 
from utils.calculate_return import CalculateReturns

st.title("Mutual Fund List") 
st.write("Filter and find the best mutual funds tailored to your investment preferences.")
st.write("")

df = pd.read_csv('data/mutual_fund_data.csv')
df.dropna(inplace=True)
fixed_items = ['return_before_tax_deduction', 'return_atfer_tax_deduction', 'fund_name']
removed_items = ['fund_manager_name','fund_manager_teneur','fund_manager_experience','fund_manager_prev_funds','fund_manager_prev_total_funds']

col1, col2 = st.columns(2)
with col1 :
    s_type = st.radio(label="Enter investment type", options=['SIP', "Lumpsum"])
    risk_type = st.selectbox("Risk Type",df['risk'].unique())
    principle = st.slider("Select deposit amount", step = 500, min_value = 500, max_value = 100000 if s_type == "SIP" else 100000*1000) 
with col2 :
    fund_type = st.selectbox("Fund Type",df['fund_type'].unique())
    num_years = st.slider("Select number of years", step = 1, min_value = 1, max_value = 100) 
    selected_columns = st.multiselect(label="Select features", options= list(
        filter(lambda x: x not in fixed_items+removed_items, list(df.columns))
    ))
    
income_before_tax, income_after_tax = [], []
df = df[(df.risk == risk_type) & (df.fund_type == fund_type)]
for i in range(len(df)) : 
    obj = CalculateReturns(
        Principle = principle, returns = df.iloc[i]['overall_return'], expense_ratio = df.iloc[i]['expense_ratio'], 
        num_years = num_years, investment_type = s_type
    )
    return_after_tax, return_before_tax = obj.calculate_tax()
    income_after_tax.append(return_after_tax)
    income_before_tax.append(return_before_tax)

df['return_atfer_tax_deduction'] = income_after_tax
df['return_before_tax_deduction'] = income_before_tax

st.text("")
st.text("")
to_drop = list(filter(lambda x : x not in selected_columns+fixed_items, list(df.columns)))
df.drop(to_drop, axis = 1, inplace = True)
st.dataframe(df, use_container_width=True)