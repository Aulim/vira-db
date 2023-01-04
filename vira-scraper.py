import cloudscraper
import hashlib
import datetime
import os
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient

URL_LIST = [
    ('dummy.html', 'Notebook'),
    ('dummy_processor.html', 'CPU')
]

DB_URI = 'mongodb://localhost:27017/'

def safe_cast(val, to_type=None, default=None):
    try:
        if to_type is not None:
            return to_type(val)
        else:
            return val
    except Exception:
        return default

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
            name = ' '.join(columns[0].text.split()).replace("Ready Stock", "").strip()
            item_id = hashlib.md5(name.encode()).hexdigest()
            price = columns[1].text.replace(".","").strip()
            price = safe_cast(price, int)
            if price:
                listing = {}
                listing['item_id'] = item_id
                listing['category'] = category
                listing['name'] = name
                listing['price'] = price
                listings.append(listing)

    return listings

def save_to_db(items, category):
    if len(items) > 0:
        with MongoClient(DB_URI) as client:
            coll = client['viraindo'][category]

            if coll.estimated_document_count() > 0:
                print("Data already exists")
            else:
                df = pd.DataFrame(items)
                df = df.drop_duplicates(subset='item_id', keep='first')
                data = df.to_dict(orient='records')
                coll.insert_many(data)

if __name__ == '__main__':
    for url, category in URL_LIST:
        items = scrape_data(url, category)
        print(len(items))
        for item in items[:5]:
            print(item)

        save_to_db(items, category)

        # if len(items) > 0:
        #     finish_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        #     save_fname = 'viraindo_'+ category + "_" + finish_time + '.csv'
        #     pd.DataFrame(items).to_csv(save_fname, ',', index=False)