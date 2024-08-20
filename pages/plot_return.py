import streamlit as st 
import pandas as pd 
from utils.calculate_return import CalculateReturns
from utils.generate_response import GenerateResponse

st.title("Interactive Charts") 
st.write("Plot return charts and receive AI-generated pros and cons for informed investment decisions.")
st.write("")

df = pd.read_csv('data/mutual_fund_data.csv')
col1, col2 = st.columns(2)
with col1 :
    s_type = st.radio(label="Enter investment type", options=['SIP', "Lumpsum"])
    select_fund = st.selectbox("Select Fund Name", options=df['fund_name'])
with col2 :
    principle = st.slider(
        "Select deposit amount", step = 500, min_value = 500, 
        max_value = 100000 if s_type == "SIP" else 100000*1000
    ) 
    num_years = st.slider("Select number of years", step = 1, min_value = 1, max_value = 100) 
    
df.dropna(inplace=True)

parent_list = []
fund_details = df[df.fund_name == select_fund]
for i in range(1, num_years+1) : 
    obj = CalculateReturns(
        Principle = principle, returns = fund_details['overall_return'].iloc[0], 
        expense_ratio = fund_details['expense_ratio'].iloc[0], 
        num_years = i, investment_type = s_type
    )
    x, y = obj.calculate_tax()

    if s_type == "SIP" : 
        parent_list.append([principle*12*i, x, y])
    else :
        parent_list.append([principle, x, y])

processed_df = pd.DataFrame(parent_list, columns=['principle', 'return_after_tax', 'return_before_tax'])
st.write("")
st.write("")
st.line_chart(processed_df)

######################### AI #########################
st.divider()
st.header("Insights")
st.write("Discover detailed AI-generated pros and cons for your selected mutual funds.")
st.write("")

if fund_details['fund_name'].iloc[0] not in st.session_state : 
    st.session_state[fund_details['fund_name'].iloc[0]] = None
    print('called..................')

    obj = GenerateResponse(
        expense_ratio = fund_details['expense_ratio'].iloc[0], 
        fund_manager_experience = eval(fund_details['fund_manager_experience'].iloc[0]), 
        fund_manager_prev_funds = eval(fund_details['fund_manager_prev_funds'].iloc[0]), 
        fund_type = fund_details['fund_type'].iloc[0], category = fund_details['category'].iloc[0], 
        risk = fund_details['risk'].iloc[0], nav = fund_details['nav'].iloc[0], 
        fund_size = fund_details['fund_size'].iloc[0], overall_return = fund_details['overall_return'].iloc[0], 
        rank = fund_details['rank'].iloc[0], AUM = fund_details['AUM'].iloc[0], 
        fund_manager_prev_total_funds = eval(fund_details['fund_manager_prev_total_funds'].iloc[0])
    )


    output = obj.generate_respone()
    print(output)
    st.session_state[fund_details['fund_name'].iloc[0]] = output

pros = st.session_state[fund_details['fund_name'].iloc[0]]['pros']
cons = st.session_state[fund_details['fund_name'].iloc[0]]['cons']
col1, col2 = st.columns(2)
with col1 :
    st.markdown("### Pros")
    for pro in pros : st.success(pro)
    
with col2 :
    st.markdown("### Cons")
    for con in cons : st.error(con)