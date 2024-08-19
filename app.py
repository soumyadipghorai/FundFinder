import streamlit as st 
from utils.calculate_return import CalculateReturns
from _temp.config import PAGE_CONFIG
import pandas as pd  
from scrap.scrape import Updatedata 
from utils.auth import check_credentials
from utils.generate_response import GenerateResponse

fund_list = st.Page("pages/fund_list.py", title="Mutual Fund List", icon=":material/list:")
calculator = st.Page("pages/return_calculator.py", title="Calculator", icon=":material/calculate:") 
plot_return = st.Page("pages/plot_return.py", title="Insights.ai", icon=":material/robot_2:") 
admin = st.Page("pages/admin_page.py", title="Admin", icon=":material/person:") 

pg = st.navigation([calculator, fund_list, plot_return, admin])

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.set_page_config(**PAGE_CONFIG)

st.sidebar.markdown("### Update Data")  
st.sidebar.write("Click to scrape and refresh the latest data for accurate and up-to-date information.")
sb_button = st.sidebar.button('scrape') 

if sb_button :
    if not st.session_state.authenticated :
        my_bar = st.sidebar.progress(0, text="Updating the Dataset. Please wait.")
        obj = Updatedata(bar_obj=my_bar, start=1, end = 1, save_location = 'dump/mutual_fund_data.csv')
        obj.create_dataframe()
        my_bar.empty()
        st.success("Dataset updated") 
    else :
        my_bar = st.sidebar.progress(0, text="Updating the Dataset. Please wait.")
        obj = Updatedata(bar_obj=my_bar, start=1, end = 106, save_location = 'data/mutual_fund_data.csv')
        obj.create_dataframe()
        my_bar.empty()

if __name__ == "__main__" :
    pg.run()