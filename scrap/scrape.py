import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 
from _temp.config import HEADERS, FUND_LIST_URL

def preprocess_value(value) : 
    return value.replace(",", "") if not (isinstance(value, float) and np.isnan(value)) else None

parent_df = []
for i in tqdm(range(1, 106+1)) : 
    url = FUND_LIST_URL.format(page_number = i) 
    fund_list_page = requests.get(url, headers = HEADERS)
    fund_list_page_htmlcontent = fund_list_page.content
    fund_list_page_soup = BeautifulSoup(fund_list_page_htmlcontent, 'html.parser')

    table_rows = fund_list_page_soup.find_all('tr', {'class' : "f22Card"})
    for tr in tqdm(table_rows) : 
        mutual_fund_url = "https://groww.in/"+tr.find('a')['href']
        mututal_fund_page = requests.get(mutual_fund_url, headers = HEADERS)
        mututal_fund_page_htmlcontent = mututal_fund_page.content
        mututal_fund_page_soup = BeautifulSoup(mututal_fund_page_htmlcontent, 'html.parser')


        try :
            fund_name = mututal_fund_page_soup.find('h1', {'class' : 'mfh239SchemeName displaySmall'}).text
            
            expense_ratio = mututal_fund_page_soup.find('h3', {'class' : 'ot654subHeading bodyLargeHeavy'}).text.split(':')[1].strip()
            expense_ratio = float(expense_ratio[:-1]) if expense_ratio != 'NA' else None
            
            tables = pd.read_html(mutual_fund_url)
            
            nav = preprocess_value(tables[0].iloc[0, -1][1:])
            nav = float(nav) if nav else None
            
            fund_size = preprocess_value(tables[1].iloc[1, -1]) 
            fund_size = float(fund_size.replace("Cr", "")[1:]) if fund_size else None
            
            overall_return = preprocess_value(tables[2].iloc[0, -1])
            overall_return = overall_return[:-1] if overall_return else None
            try : 
                rank = preprocess_value(tables[6].iloc[0, -1])
                AUM = preprocess_value(tables[6].iloc[1, -1]) 
            except : 
                rank = preprocess_value(tables[5].iloc[0, -1]) 
                AUM = preprocess_value(tables[5].iloc[1, -1])

            rank = int(rank.split(' ')[0][1:]) if rank else None
            AUM = float(AUM.replace('Cr', "")[1:]) if AUM else None
                
            parent_df.append([
                fund_name, expense_ratio, nav, fund_size, overall_return, rank, AUM
            ])
        except Exception as e : 
            print(mutual_fund_url, e)
            
df = pd.DataFrame(parent_df, columns = [
    "fund_name", "expense_ratio", "nav", "fund_size", "overall_return", "rank", "AUM"
])

df.to_csv('data/mutual_fund_data.csv', index= False, encoding='utf-8')