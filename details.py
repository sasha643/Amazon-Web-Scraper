import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Read the CSV file
df = pd.read_csv('data.csv')

# Create a list to store the scraped data
data_list = []
M = []

for url in df['URL']:
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the product details section
        product_details = soup.find("ul", {"class": "a-unordered-list a-vertical a-spacing-mini"})

        # Extract the manufacturer information using regular expressions
        product_text = soup.find("div", {"id": "detailBullets_feature_div"}).text
        text = product_text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        combined_text = '\n'.join(lines)
        text = combined_text.replace(':','') 
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = '\n'.join(cleaned_lines)
        cleaned_text = cleaned_text.replace(" ", "").replace("\n", "")
        manufacturer_match = re.search(r"Manufacturer‏‎(.*?)ASIN", cleaned_text)
        if manufacturer_match:
            manufacturer = manufacturer_match.group(1)
        else:
            manufacturer = 'Not found'

        # Extract the ASIN number using regular expressions
        asin_match = re.search(r"ASIN‏‎(.*?)Itemmodelnumber", cleaned_text)
        if asin_match:
            asin = asin_match.group(1)
        else:
            asin = 'Not found'

        data_list.append({
            'URL': url,
            'Manufacturer': manufacturer,
            'ASIN': asin,
            'Product details': product_details.text.strip()
        })

        M.append(data_list[0]['URL'])
        if len(M) == 5:
            break
        
    except:
        continue


# Create a DataFrame from the data
amazon_df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
amazon_df.to_csv("Product_data.csv", header=True, index=False)
