import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# URL of the first page
url = "http://books.toscrape.com/catalogue/page-1.html"

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
print(response.status_code)  # 200 means success

# Preview the HTML content
print(response.text[:500])  # print first 500 characters

# Use requests or urllib to load the HTML content of the target page.Print the HTTP response status and a preview of the HTML.
# Example GET with query params
params = {"category": "travel"}
response = requests.get(url, params=params)
#print("Final URL:", response.url)

# Example POST 
post_url = "https://httpbin.org/post"
payload = {"search": "python books"}
post_response = requests.post(post_url, data=payload)
#print(post_response.json())

soup = BeautifulSoup(response.text, 'lxml')

# Find all book containers
books = soup.find_all("article", class_="product_pod")

# Extract data
data = []
for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.p["class"][1]  # second class contains rating word
    data.append({"title": title, "price": price, "rating": rating})

for product in data:
    print(product)

data = []

for page in range(1, 4):  # scrape first 3 pages
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find_all("article", class_="product_pod")
    
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]
        data.append({"title": title, "price": price, "rating": rating})

print(len(data))  # total number of books scraped




df = pd.DataFrame(data)

# Remove '£' and convert price to float
df['price'] = df['price'].apply(lambda x: float(re.sub(r'[^0-9.]', '', x)))

# Map rating words to numbers
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df['rating'] = df['rating'].map(rating_map)

print(df.head())

df.to_csv("data/books_data.csv", index=False)


driver = webdriver.Chrome()  # Ensure chromedriver is installed
driver.get("http://books.toscrape.com/catalogue/page-1.html")

for _ in range(3):
    products = driver.find_elements(By.CLASS_NAME, "product_pod")
    print("Products on page:", len(products))
    next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a")
    next_btn.click()
    time.sleep(2)
driver.quit()


import re

for d in data:                                      # change the pricing to numerical
    d["price"] = float(re.search(r"\d+\.\d+", d["price"]).group())
rating_map = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

for d in data:                                     #change rating to numerical
    d["rating"] = rating_map.get(d["rating"], 0)


import pandas as pd

df = pd.DataFrame(data)
df.to_csv("data/products.csv", index=False)#Save data to csv file ca;;ed products

print(df.head())
print(df.info())

# Average price per rating
avg_price = df.groupby('rating')['price'].mean()
avg_price.plot(kind='bar', title='Average Price per Rating')
plt.xlabel('Rating')
plt.ylabel('Average Price (£)')
plt.savefig("charts/avg_price_per_rating.png")
plt.show()


# Histogram of prices
plt.hist(df['price'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution of Book Prices')
plt.xlabel('Price (£)')
plt.ylabel('Number of Books')
plt.savefig("charts/price_distribution.png")
plt.show()

api_resp = requests.get("https://httpbin.org/json")
print(api_resp.json())