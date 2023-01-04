import cloudscraper
import datetime
import os
import pandas as pd
from bs4 import BeautifulSoup

URL_LIST = [
    ('dummy.html', 'Notebook'),
    ('dummy_processor.html', 'CPU')
]

def scrape_data(url, category=""):
    # scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
    cwd = os.getcwd()
    os.chdir(cwd)
    html = open(url, "r")
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('tr')
    listings = []
    for row in rows:
        data = row.findAll('td')
        iter_data = iter(data)
        data_cols = list(zip(iter_data, iter_data))
        for columns in data_cols:
            name = ' '.join(columns[0].text.split()).strip()
            price = columns[1].text.replace(".","").strip()
            if price:
                listing = {}
                listing['category'] = category
                listing['name'] = name
                listing['price'] = price
                listings.append(listing)

    return listings

for url, category in URL_LIST:
    items = scrape_data(url, category)
    print(len(items))
    for item in items[:5]:
        print(item)

    if len(items) > 0:
        finish_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        save_fname = 'viraindo_'+ category + "_" + finish_time + '.csv'
        pd.DataFrame(items).to_csv(save_fname, ',', index=False)