import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL of the first page
url = "http://books.toscrape.com/catalogue/page-1.html"

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
print(response.status_code)  # 200 means success

# Preview the HTML content
print(response.text[:500])  # print first 500 characters


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

print(data[:3])  # print first 3 entries

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
