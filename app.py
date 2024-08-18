import streamlit as st 
from utils.calculate_return import CalculateReturns
from _temp.config import PAGE_CONFIG
import pandas as pd  
from scrap.scrape import Updatedata 
from utils.auth import check_credentials


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.set_page_config(**PAGE_CONFIG)

st.sidebar.markdown("## Controls") 
sidebar_main = st.sidebar.selectbox('Navigation', ['Calculator', 'Mutual Fund List', 'Plot Return', 'Admin'])
sb_button = st.sidebar.button('scrape') 

if sb_button :
    if not st.session_state.authenticated :
        st.success("Already updated") 
    else :
        my_bar = st.sidebar.progress(0, text="Operation in progress. Please wait.")
        obj = Updatedata(bar_obj=my_bar, start=1, end = 106)
        obj.create_dataframe()
        my_bar.empty()

if sidebar_main == "Calculator" :
    st.title("Calculate returns") 
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
        obj = CalculateReturns(
            Principle = p, returns = r, expense_ratio = e, 
            stamp_duty = s, num_years = n, investment_type = s_type
        )
        st.write(obj.calculate_tax())

if sidebar_main == "Mutual Fund List" : 
    st.title("Mutual Fund List") 
    df = pd.read_csv('data/mutual_fund_data.csv')
    df.dropna(inplace=True)
    df.drop(['fund_manager_name','fund_manager_teneur','fund_manager_experience','fund_manager_prev_funds','fund_manager_prev_total_funds'], axis = 1, inplace = True)
    col1, col2 = st.columns(2)
    with col1 :
        s_type = st.radio(label="Enter investment type", options=['SIP', "Lumpsum"])
        risk_type = st.selectbox("Risk Type",df['risk'].unique())
    with col2 :
        category = st.selectbox("Fund Category",df['category'].unique())
        num_years = st.slider("Select number of years", step = 1, min_value = 1, max_value = 100) 
        
    principle = st.slider("Select deposit amount", step = 500, min_value = 500, max_value = 100000 if s_type == "SIP" else 100000*1000) 
        
    income_before_tax, income_after_tax = [], []
    df = df[(df.risk == risk_type) & (df.category == category)]
    for i in range(len(df)) : 
        obj = CalculateReturns(
            Principle = principle, returns = df.iloc[i]['overall_return'], expense_ratio = df.iloc[i]['expense_ratio'], 
            num_years = num_years, investment_type = s_type
        )
        return_before_tax, return_after_tax = obj.calculate_tax()
        income_after_tax.append(return_after_tax)
        income_before_tax.append(return_before_tax)

    df['return_atfer_tax'] = income_after_tax
    df['return_before_tax'] = income_before_tax

    st.dataframe(df, use_container_width=True)

if sidebar_main == "Plot Return" : 
    st.title("Return Charts") 
    df = pd.read_csv('data/mutual_fund_data.csv')
    col1, col2 = st.columns(2)
    with col1 :
        s_type = st.radio(label="Enter investment type", options=['SIP', "Lumpsum"])
        select_fund = st.selectbox("Select Fund Name", options=df['fund_name'])
    with col2 :
        principle = st.slider("Select deposit amount", step = 500, min_value = 500, max_value = 100000 if s_type == "SIP" else 100000*1000) 
        num_years = st.slider("Select number of years", step = 1, min_value = 1, max_value = 100) 
        
    df.dropna(inplace=True)

    parent_list = []
    fund_details = df[df.fund_name == select_fund]
    for i in range(1, num_years+1) : 
        obj = CalculateReturns(
            Principle = principle, returns = fund_details['overall_return'].iloc[0], expense_ratio = fund_details['expense_ratio'].iloc[0], 
            num_years = i, investment_type = s_type
        )
        x, y = obj.calculate_tax()

        if s_type == "SIP" : 
            parent_list.append([principle*12*i, x, y])
        else :
            parent_list.append([principle, x, y])

    processed_df = pd.DataFrame(parent_list, columns=['principle', 'return_after_tax', 'return_before_tax'])
    st.line_chart(processed_df)

if sidebar_main == "Admin" :
    st.title("Admin Log in")

    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login") : 
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")
    else : 
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.success("Log out successful!")