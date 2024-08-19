import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np  
from dotenv import main
from tqdm import tqdm 
import os 
from _temp.config import HEADERS, FUND_LIST_URL

_ = main.load_dotenv(main.find_dotenv())
BASE_URL = os.getenv("BASE_URL")

class Updatedata : 
    def __init__(self, bar_obj, parent_list: list = [], start: int = 1, end: int = 106, save_location: str = "") -> None : 
        self.bar_obj =bar_obj
        self.parent_list = parent_list
        self.start = start
        self.end = end
        self.save_location = save_location

    def __preprocess_value(self, value) : 
        return value.replace(",", "") if not (isinstance(value, float) and np.isnan(value)) else None
    
    def __update_data(self) :
        self.parent_df = []
        for i in tqdm(range(self.start, self.end+1)) :  
            url = BASE_URL+FUND_LIST_URL.format(page_number = i) 
            fund_list_page = requests.get(url, headers = HEADERS)
            fund_list_page_htmlcontent = fund_list_page.content
            fund_list_page_soup = BeautifulSoup(fund_list_page_htmlcontent, 'html.parser')

            table_rows = fund_list_page_soup.find_all('tr', {'class' : "f22Card"})
            for j in tqdm(range(len(table_rows))) :   
                curr, total = (i - self.start)*15 + j, (self.end+1)*15 - (self.start*15)
                self.bar_obj.progress(curr/total, text="Updating Dataset. Please wait.")
                mutual_fund_url = BASE_URL+table_rows[j].find('a')['href']
                mututal_fund_page = requests.get(mutual_fund_url, headers = HEADERS)
                mututal_fund_page_htmlcontent = mututal_fund_page.content
                mututal_fund_page_soup = BeautifulSoup(mututal_fund_page_htmlcontent, 'html.parser')


                try :
                    fund_name = mututal_fund_page_soup.find('h1', {'class' : 'mfh239SchemeName displaySmall'}).text

                    fund_details_list = mututal_fund_page_soup.find_all('div', {'class' : 'mfh239PillsContainer'})
                    fund_details = [div.text.strip() for div in fund_details_list]

                    fund_manager_details = mututal_fund_page_soup.find_all('div', {'class' : 'cur-po fm982AboutFundManager'})
                    fund_manager_name = [div.find('h3').find('div', {'class' : 'fm982PersonName contentPrimary bodyLargeHeavy'}).text.strip() for div in fund_manager_details]
                    fund_manager_teneur = [div.find('h3').find('div', {'class' : 'contentSecondary bodyBase'}).text.strip() for div in fund_manager_details]
                    fund_manager_experience = [[fund.text.strip() for fund in div.find_all('div', {'class' : 'contentPrimary bodyLarge'})] for div in fund_manager_details]
                    fund_manager_also_managed = [[fund.text.strip() for fund in div.find_all('div', {'class' : 'fm982ExpandFundsManaged'})] for div in fund_manager_details]
                    fund_manager_num_funds = [len(div.find_all('div', {'class' : 'fm982ExpandFundsManaged'}) )for div in fund_manager_details]
                    
                    expense_ratio = mututal_fund_page_soup.find('h3', {'class' : 'ot654subHeading bodyLargeHeavy'}).text.split(':')[1].strip()
                    expense_ratio = float(expense_ratio[:-1]) if expense_ratio != 'NA' else None
                    
                    tables = pd.read_html(mutual_fund_url)
                    
                    nav = self.__preprocess_value(tables[0].iloc[0, -1][1:])
                    nav = float(nav) if nav else None
                    
                    fund_size = self.__preprocess_value(tables[1].iloc[1, -1]) 
                    fund_size = float(fund_size.replace("Cr", "")[1:]) if fund_size else None
                    
                    overall_return = self.__preprocess_value(tables[2].iloc[0, -1])
                    overall_return = overall_return[:-1] if overall_return else None
                    try : 
                        rank = self.__preprocess_value(tables[6].iloc[0, -1])
                        AUM = self.__preprocess_value(tables[6].iloc[1, -1]) 
                    except : 
                        rank = self.__preprocess_value(tables[5].iloc[0, -1]) 
                        AUM = self.__preprocess_value(tables[5].iloc[1, -1])

                    rank = int(rank.split(' ')[0][1:]) if rank else None
                    AUM = float(AUM.replace('Cr', "")[1:]) if AUM else None
                        
                    self.parent_df.append([
                        fund_name, expense_ratio, json.dumps(fund_manager_name), 
                        json.dumps(fund_manager_teneur), json.dumps(fund_manager_experience), 
                        json.dumps(fund_manager_also_managed), json.dumps(fund_manager_num_funds), 
                        fund_details[0], fund_details[1], fund_details[2], nav, 
                        fund_size, overall_return, rank, AUM
                    ])
                except Exception as e : 
                    print(mutual_fund_url, e)

        return self.parent_df
    
    def create_dataframe(self) :
        self.__update_data()
        df = pd.DataFrame(self.parent_df, columns = [
            "fund_name", "expense_ratio", 'fund_manager_name', 
            'fund_manager_teneur', 'fund_manager_experience', 
            'fund_manager_prev_funds', 'fund_manager_prev_total_funds', 
            'fund_type', 'category', 'risk', "nav", "fund_size", 
            "overall_return", "rank", "AUM"
        ])

        df.to_csv(self.save_location, index= False, encoding='utf-8')
        # df.to_csv('mutual_fund_data.csv', index= False, encoding='utf-8')
        return 'success'