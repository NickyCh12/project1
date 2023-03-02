# Import library
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Define variables and get the website content using "Selenium"
i = 1
w = ExcelWriter('Excel.xlsx', engine='xlsxwriter')
browser = webdriver.Chrome() # open a browser
browser.maximize_window()
browser.get("html_link")
time.sleep(5)

# Load all the available data on the page by pressing spacebar
actions1 = ActionChains(browser)
for a in range(7):
    actions1.send_keys(Keys.SPACE).perform()
    time.sleep(0.5)
time.sleep(3)

# i = how many page we want to scrape
while i <= 27:

# Create dataframe
    data = {
        'date':[],
        'premises':[],
        'floor':[],
        'district':[],
        'price':[],
        'SFA':[],
        'GFA':[]
    }

# Read the page content using "Beautifulsoup"
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

# Get the data we want and assign it into specified column under the dataframe // Input "N/A" if value is not found
    for datetag in soup.select("div.sc-2vbwj7-23"):
        date = datetag.find('div','sc-2vbwj7-5')
        data['date'].append(date.get_text().strip() if date else 'N/A')

    for premisestag in soup.select("div.sc-1u6t046-3"):   
        premises = premisestag.find('div','sc-1u6t046-1').find(string=True, recursive=False)
        data['premises'].append(premises.get_text().strip() if premises else 'N/A')

    for floortag in soup.select("div.sc-2vbwj7-23"):
        floor = floortag.find('div','sc-1u6t046-0 iaXPKR')
        data['floor'].append(floor.get_text().strip() if floor else 'N/A')

    for districttag in soup.select("div.sc-2vbwj7-23"):
        district = districttag.find('span','sc-2vbwj7-2 fdjJsZ')
        data['district'].append(district.get_text().strip() if district else 'N/A')

    for pricetag in soup.select("div.sc-2vbwj7-23"):
        price = pricetag.find('span','sc-hlnw2x-6 kktEPG')
        data['price'].append(price.get_text().strip() if price else 'N/A')

    for tag1 in soup.find_all('div',"sc-2vbwj7-1 dfLNXK"):    
        GFA = tag1.select_one(".sc-1d6dn8u-2:nth-child(2)") #find(text=True, recursive=True)   
        data['GFA'].append(GFA.get_text().strip() if GFA else 'N/A')   

    for tag2 in soup.select(".sc-2vbwj7-23 .sc-1d6dn8u-4"):
        SFA = tag2.find('div','sc-1d6dn8u-1 buFexZ').find(text=True, recursive=False) 
        data['SFA'].append(SFA.get_text().strip() if SFA else 'N/A')

# Assign the dataframe into table using "Panda" // Write the table into an auto-created Excel file. As there are 23 data on each page, the startrow formular is to write content to the next row after each of the appended 23 data.
    rental = pd.DataFrame(data)  
    rental.to_excel(w, startrow=23*(i-1)+1,index=False, header=False)
    i = i + 1 
    
# Find the "Next Page" button on the page and click // Sleep 3 seconds for page loading
    browser.execute_script("document.querySelector(\"#__next > main > div.sc-1jigt1a-1.dlspjX > div > div.rmc-tabs-content-wrap > div.rmc-tabs-pane-wrap.rmc-tabs-pane-wrap-active > div.jqe5tj-3.eqhNgY > div > div.sc-adjhgu-0.bcJKaH.sc-c8n77o-0.iIhHES > ul > li.next > a\").click()")

    time.sleep(3)

# Load all the available data on the page by pressing spacebar // Sleep for 3 seconds for page loading  
    actions1 = ActionChains(browser)
    for a in range(7):
        actions1.send_keys(Keys.SPACE).perform()
        time.sleep(0.5)
    time.sleep(3)

# Save the file
w.save()
