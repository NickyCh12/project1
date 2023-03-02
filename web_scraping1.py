# Import library
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from pandas import ExcelWriter

# Define variables and get the website content using selenium
i = 1
w = ExcelWriter('Excel.xlsx',mode='a',engine='openpyxl', if_sheet_exists='overlay')
browser = webdriver.Chrome() # open a browser
browser.get("https://hk.centanet.com/findproperty/en/list/transaction?q=dXQXD7v5cUKT5fwQwIYIlw")

# Click the specific icon to nevagate to the page we want. Sleep for 5 seconds for loading
element1 = browser.find_element(By.CLASS_NAME,'right-icon')
element1.click()
time.sleep(5)

# i = how many pages we want to scrape
while i <= 3:

# Create dataframe
    data = {
    'date':[],
    'premises':[],
    'district':[],
    'price':[],
    'SFA':[],
    'GFA':[]}

# Read the page content using "Beautifulsoup"
    i = i+1
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

# Get the data we want and assign it into specified column under the data frame. Input "N/A" if value is not found
    for datetag in soup.select(".deal-property.list .area-block.hidden-sm-and-down"):
        date = datetag.find('div','data-info')
        data['date'].append(date.get_text().strip() if date else 'N/A')

    for premisestag in soup.select(".deal-property.list .right-block"):
        premises = premisestag.find('h3','title-lg')
        data['premises'].append(premises.get_text().strip() if premises else 'N/A')

    for districttag in soup.select(".deal-property.list .right-block"):
        district = districttag.find('span','adress')
        data['district'].append(district.get_text().strip() if district else 'N/A')

    for pricetag in soup.select(".price-sect:nth-child(1)"):
        price = pricetag.find('div','price')
        data['price'].append(price.get_text().strip() if price else 'N/A')
    
    for tag1 in soup.select("div.areaB > div.area-block:nth-child(3) > div.data-info"):
        GFA = tag1.find('span','hidden-xs-only')
        data['GFA'].append(GFA.get_text().strip() if GFA else 'N/A')

    for tag2 in soup.select("div.areaB > div.area-block:nth-child(2) > div.data-info"):
        SFA = tag2.find('span','hidden-xs-only')
        data['SFA'].append(SFA.get_text().strip() if SFA else 'N/A')

# Assign the dataframe into table using "Panda" 
    rental = pd.DataFrame(data)   

# Write the table into a pre-created Excel file. Write on the last row on the sheet every time.
    rental.to_excel(w, startrow=w.sheets['Sheet1'].max_row,index=False, header=False)     

# Find the "Next Page" button on the page and click. Sleep 3 seconds for page loading      
    element2 = browser.find_element(By.CLASS_NAME,'btn-next')
    element2.click()
    time.sleep(3) # sleep three seconds so page can load

# Save the file
w.save()     