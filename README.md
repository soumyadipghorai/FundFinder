# FundFinder

**FundFinder** is a powerful and intuitive Streamlit app designed to help investors select the best mutual funds by providing detailed comparisons and insights. The app scrapes mutual fund data from the internet, calculates returns before and after taxes, and compares funds based on their performance and expense ratios. It also visualizes the data to aid in making informed investment decisions.

## Features

- **Fund Data Scraping**: Automatically fetch mutual fund details from the internet.
- **Return Calculations**: Compute actual returns before and after taxes.
- **Expense Ratio Comparison**: Compare different funds based on their expense ratios.
- **Interactive Visualization**: Plot charts to visualize fund performance and comparisons.
- **User-Friendly Interface**: Built with Streamlit for a seamless user experience.

## Installation

To set up FundFinder, you need to have Python and Streamlit installed. Follow these steps to get started:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/FundFinder.git
   cd FundFinder
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

2. **Interact with the App**:
   - **Fund Selection**: Browse through the list of mutual funds.
   - **View Fund Details**: See detailed information about each fund.
   - **Compare Funds**: Analyze and compare different funds based on returns and expense ratios.
   - **Visualize Data**: View charts that illustrate fund performance.

## Project Structure

```
|---_temp 
|   |-- condfig.py
|
|--- data 
|   |-- mutual_fund_data.py
|
|--- notebooks 
|   |-- test.ipynb
|
|--- scrap 
|   |-- scrape.py
|
|--- utils 
|   |-- calculate_return.py
|
|--- app.py 
|--- .gitignore 
|--- LICENSE
|--- README.md 
|--- requirements.txt
```

## Requirements

- Python 3.7 or higher
- Streamlit
- pandas
- numpy
- requests (for web scraping)
- BeautifulSoup (for parsing HTML)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or feedback, please reach out to [work.soumyadipghorai@gmail.com](mailto:work.soumyadipghorai@gmail.com).

---

Happy Investing!
```

### Notes:
- Adjust the repository URL in the `Clone the Repository` section to your actual GitHub repository URL.
- Update the email address and other personal information as needed.
- Ensure that `requirements.txt` includes all necessary libraries for your app.

This `README.md` provides a comprehensive guide to setting up and using your FundFinder app.