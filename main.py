from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except:
            price = ""

    return price[1:]

def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

if __name__ == '__main__':
    d = {"URL": [], "Product Name":[], "price(Rs)":[], "rating":[], "reviews":[]}
    for i in range(1,21):
        #print(i)
        url = 'https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1692795295&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'.format(i,i)
        #print(url)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
        webpage = requests.get(url, headers=headers)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
        
        #print(links[5].get('href'))

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
                links_list.append(link.get('href'))
        
        # Loop for extracting product details from each link 
        for link in links_list:
            try:
                #print(link)
                new_webpage = requests.get("https://www.amazon.in" + link, headers=headers)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to display all necessary product information
                d['URL'].append("https://www.amazon.in" + link)
                d['Product Name'].append(get_title(new_soup))
                d['price(Rs)'].append(get_price(new_soup))
                d['rating'].append(get_rating(new_soup))
                d['reviews'].append(get_review_count(new_soup))

            
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['Product Name'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['Product Name'])
                amazon_df.to_csv("data.csv", header=True, index=False)

            except:
                continue
