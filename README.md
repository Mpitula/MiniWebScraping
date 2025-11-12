## 🕸️ Web Scraping Project
# 📘 Overview

This project is a Python-based web scraper designed to extract key product information such as:

🏷️ Title

⭐ Rating

💰 Price

🗣️ Number of Reviews

It can be used to gather data from e-commerce websites for analysis, price comparison, or machine learning model training.

# 🧰 Tech Stack

Python 3.8+

Libraries:

requests – for making HTTP requests

beautifulsoup4 – for parsing and extracting HTML data

(Optional) pandas – for saving results to CSV or Excel

# ⚙️ Installation

Clone the repository

git clone https://github.com/yourusername/webscraping-project.git
cd webscraping-project


Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt

# 📄 Example Script
import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com/s?k=laptop"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

products = []

for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
    title = item.h2.text.strip() if item.h2 else "N/A"
    rating = item.find("span", class_="a-icon-alt")
    price = item.find("span", class_="a-price-whole")
    reviews = item.find("span", {"class": "a-size-base"})

    products.append({
        "Title": title,
        "Rating": rating.text.strip() if rating else "N/A",
        "Price": price.text.strip() if price else "N/A",
        "Reviews": reviews.text.strip() if reviews else "N/A"
    })

for p in products:
    print(p)

# 📦 Output Example
[
  {
    "Title": "Acer Aspire 5 Laptop",
    "Rating": "4.3 out of 5 stars",
    "Price": "549",
    "Reviews": "1,243"
  },
  {
    "Title": "HP Pavilion x360",
    "Rating": "4.1 out of 5 stars",
    "Price": "699",
    "Reviews": "987"
  }
]

# 💾 Exporting Data (Optional)

You can easily save the scraped data to a CSV file:

import pandas as pd
df = pd.DataFrame(products)
df.to_csv("products.csv", index=False)

 # ⚠️ Disclaimer

This project is for educational purposes only.
Always check a website’s robots.txt file and terms of service before scraping.
Avoid scraping sites that prohibit automated access or may block your IP.

# 🧑‍💻 Author

Alone Mpitula
📧 Alonemapitlula@gmail.com
