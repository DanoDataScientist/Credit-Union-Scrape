import requests
from bs4 import BeautifulSoup 
import pandas as pd

# Create empty lists that will be populated with the requested parameters.
names = []
headquarters = []
date_established = []
assets = []
loans = []
deposits = []
capital = []
insured = []

# Create a for loop for the number of pages on the website.
for page_number in range(1,518):
    page = requests.get(f'https://www.bestcashcow.com/credit-unions/page-{page_number}')
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    
    table = soup.find('table', {'class': 'colorstables rate bank_savings_rates table1'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    
    # Loop through all the credit unions in the table.
    for row in rows:
        # Finds the credit union name.
        names.append(row.find('td').find('a').text)
        # Finds the headquarter location.
        headquarters.append(row.find_all('td')[1].text.replace('\xa0',''))
        # Finds the date established.
        date_established.append(row.find_all('td')[2].text)
        # Finds the assets.
        assets.append(row.find_all('td')[3].text)
        
        # Some of the information is on a seperate page, requiring another GET request.
        page_link = row.find('a').get('href')
        info_page = requests.get(f'{page_link}')
        info_content = info_page.content
        info_soup = BeautifulSoup(info_content, 'html.parser')
        info_table = info_soup.find('table', {'class': 'full_table bank_financial_details'})
        info_body = info_table.find('tbody')
        info_rows = info_body.find_all('tr')
        
        # Finds if the union is NCUA insured.
        insured.append(info_rows[0].find_all('td')[1].text)
        # Finds the the amount of loans.
        loans.append(info_rows[4].find_all('td')[1].text)
        # Finds the amount of deposits.
        deposits.append(info_rows[5].find_all('td')[1].text)
        # Finds the amount of capital.
        capital.append(info_rows[6].find_all('td')[1].text)
        
# Creates a Pandas dataframe of all the data.        
credit_data = pd.DataFrame({
    'Name': names,
    'Headquarters': headquarters,
    'Assets': assets,
    'Loans': loans,
    'Deposits': deposits,
    'Capital': capital,
    'NCUA Insured': insured
})
# Reorder the columns.
credit_data = credit_data[['Name', 'Headquarters', 'Assets', 'Loans', 'Deposits', 'Capital', 'NCUA Insured']]

# Converts the dataframe to a csv file.
credit_data.to_csv('Credit Data.csv')

