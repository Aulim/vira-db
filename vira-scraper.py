import cloudscraper
import hashlib
import datetime
import pandas as pd
from bs4 import BeautifulSoup

URL_LIST = [
    # ('dummy.html', 'notebook')
    ('http://viraindo.com/notebook.html', 'notebook')
]

def safe_cast(val, to_type=None, default=None):
    try:
        if to_type is not None:
            return to_type(val)
        else:
            return val
    except Exception:
        return default

def scrape_data(url, category=""):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
    res = scraper.get(url)
    if res.status_code != 200:
        print(f'Failed to get {url}')
        return
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('tr')
    fetch_date = datetime.datetime.now().strftime("%Y-%m-%d")
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
                listing['date'] = fetch_date
                listings.append(listing)

    return listings

def save_to_csv(items, category):
    if len(items) > 0:
            save_fname = 'data/viraindo_'+ category + '.csv'
            pd.DataFrame(items).to_csv(save_fname, ',', mode='a', index=False)

if __name__ == '__main__':
    for url, category in URL_LIST:
        items = scrape_data(url, category)
        print(len(items))
        for item in items[:5]:
            print(item)

        save_to_csv(items, category)