# import libraries 
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv 
import os.path
import pandas as pd

# set up headers
header = ['Title', 'Price', 'Date']

# writing headers to the CSV file in "w+" mode
filename = 'AmazonWebScraperDataset.csv'
if not os.path.isfile(filename):
    with open(filename, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# global variable to count lines
line_count = 0

def priceTracker():
    global line_count
    try:
        # connect to website and pull in data
        URL = 'https://www.amazon.com/SAMSUNG-Inch-Internal-MZ-77E1T0B-AM/dp/B08QBJ2YMG/ref=sr_1_3?keywords=ssd+1tb&sr=8-3'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        page = requests.get(URL, headers=headers, cookies={'__hs_opt_out': 'no'})
        soup1 = BeautifulSoup(page.content, "lxml")
        soup2 = BeautifulSoup(soup1.prettify(), "lxml")
        title = soup2.find(id='productTitle').get_text()
        price = soup2.find('span', attrs={'class':'a-offscreen'}).text.strip()
        
        # format
        price = price.strip()[1:]
        title = title.strip()

        today = datetime.date.today()
        
        data = [title, price, today]

        with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
            line_count += 1
            if line_count > 100: # stop at 100 lines of data
                print("Scraped 100 lines. Exiting...")
                exit()

        dataf = pd.read_csv('AmazonWebScraperDataset.csv')
        print(dataf)

    except Exception as e:
        print("An error occurred while scraping data: ", e)

# Runs priceTracker after a set time and inputs data into your CSV
while(True):
    priceTracker()
    time.sleep(86400)
