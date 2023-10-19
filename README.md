# Amazon Web Scraper

1. main.py
   
This Python script scrapes product information from Amazon, including product name, price, rating, and review count. It also saves the data to a CSV file for further analysis.

## Prerequisites

Before running the script, make sure you have the following libraries installed:

- `bs4` (Beautiful Soup): For web scraping.
- `requests`: For making HTTP requests.
- `pandas`: For data manipulation and storage.
- `numpy`: For data handling.
- `re`: For regular expressions.
- 
You can install these libraries using `pip`:

```bash
pip install beautifulsoup4 requests pandas numpy.

##Usage

Clone this repository or download the main.py script.
You can change the range of the loop at line 72 to adjust number of pages whose data you want to scrape.

##Output

The script will generate a CSV file named data.csv, containing the following columns:

URL: The URL of the product.
Product Name: The name of the product.
price(Rs): The product's price in Indian Rupees.
rating: The product's rating.
reviews: The number of reviews for the product.

2. details.py

This Python script scrapes Amazon product details, including the manufacturer, ASIN (Amazon Standard Identification Number), and product details from a list of product URLs stored in a CSV file.

##Usage

Clone this repository or download the details.py script.
Use the CSV file named data.csv that was generated from main.py. It contains a column labeled URL with the Amazon product URLs you want to scrape.
You can change the len(M) in line 37 to adjust number of product details you want.

##Output

The script will generate a CSV file named Product_data.csv, containing the following columns:

URL: The URL of the product.
Manufacturer: The manufacturer of the product.
ASIN: The Amazon Standard Identification Number.
Product details: The product details section from the Amazon page.

data.csv and Product_data.csv are uploaded for reference.
