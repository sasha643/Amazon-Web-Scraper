import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from urllib.parse import urlparse, parse_qs
valid_data = []

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
    number = st.number_input('Enter how many pages you want to extract: ')
    URL = st.text_input('Enter the url of the page: ')
    #count = 0
    if st.button('Enter'):
        if number and URL is not None:
            parsed_url = urlparse(URL)
            query_params = parse_qs(parsed_url.query)
            if 'qid' in query_params:
                qid = query_params['qid'][0]
            for i in range(int(number)):
                #print(i)
                url = 'https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid={}&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'.format(i,i,qid)
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
                        valid_data.append(amazon_df)
                        #print(type(amazon_df))
                        #amazon_df = np.arange(1,len(final)+1)
                        #amazon_df.to_csv("new.csv", header=True, index=False)
                    except:
                        continue
            if valid_data:
                amazon_df = pd.concat(valid_data)

                # Display success message
                st.success('Data fetched successfully')
            
                # Display download button
                st.download_button("Download CSV", amazon_df.to_csv(index=False), file_name="saaman.csv", mime="text/csv")
            else:
                st.error('No valid data found.')


        else:
            st.warning('Enter all detals!')
    #https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1693161254&sprefix=ba%2Caps%2C283&ref=sr_pg_1
