import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

#username: 93000499897
#password: Easton1

# initialize an empty dataframe
df = pd.DataFrame(columns=["name","price"])
names = np.array([])
prices = np.array([])

# catalog pages

catalog = ["https://order.tupperware.com/sf/app/tsf$search_item_results.main_page",
           "https://order.tupperware.com/sf/app/tsf$search_item_results.main_page"]

# get items from sales classes
sales_class_url = catalog[0]
sales_class_items = requests.get(sales_class_url, auth=('93000499897', 'Easton1'))
soup = BeautifulSoup(sales_class_items.content,"html.parser")

print(soup.prettify())

for i in range(0,len(soup.find_all("tr"))):
    name = soup.find_all("li",class_="item")[i].find_all("h2", class_="product-name")[0].get_text()
    names = np.append(names, name)
    price = soup.find_all("li",class_="item")[i].find_all("span", class_="price")[0].get_text()
    prices = np.append(prices, price)

df.name = names
df.price = prices
