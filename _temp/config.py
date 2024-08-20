HEADERS = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

FUND_LIST_URL = "mutual-funds/filter?q=&fundSize=&pageNo={page_number}&sortBy=3"

PAGE_CONFIG = {
    "page_title": "Fund Finder", 
    "page_icon": "https://fonts.gstatic.com/s/i/materialiconsoutlined/account_balance/v6/24px.svg",          
    "layout": "centered",           
    "initial_sidebar_state": "auto" 
}

FUND_MANAGER_PROMPT = """
### ROLE: 
You are an intelligent Mutual fund expert who can determine pros and cons of mututal fund given some details about the fund. 

### FUND DETAILS:
Given the following mutual fund details:

- **Expense Ratio**: {expense_ratio}%
- **Fund Manager Details**: {fund_manager_details}
- **Avg Fund manager experience**: {avg_fund_manager_experience}
- **Fund Type**: {fund_type}
- **Category**: {category}
- **Risk Level**: {risk}
- **NAV (Net Asset Value)**: {nav}
- **Fund Size**: {fund_size} Cr
- **Overall Return**: {overall_return}%
- **Rank**: {rank}
- **Assets Under Management (AUM)**: {AUM} Cr

### PROMPT 
Please provide a detailed analysis including the pros and cons of investing in this mutual fund.
"""