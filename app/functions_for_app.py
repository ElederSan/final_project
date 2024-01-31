import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")

# Function to scrape Trustpilot reviews
@st.cache_data
def scrape_trustpilot_reviews(url, from_page, to_page):
    review_id = []
    review_title = []
    review_date = []
    review_rating = []
    review_content = []
    review_location = []
    page_number = []

    for i in range(from_page, to_page + 1):
        current_url = f"{url}?page={i}&sort=recency"
        response = requests.get(current_url)
        
        if response.status_code != 200:
            print(f"Error fetching page {i}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        for review in soup.find_all('section', class_='styles_reviewsContainer__3_GQw'):
            # review_id
            rev_id = [re.search(r'/reviews/([a-f\d]+)', elem['href']).group(1) for elem in soup.select("div.styles_reviewContent__0Q2Tg a") if elem.parent]
            review_id.extend(rev_id)

            # title
            title = [elem.get_text().replace("\n", "").replace("\t", "") for elem in soup.select("div a h2")]
            review_title.extend(title)

            # date
            date = [
                datetime.strptime(elem.get_text().replace("\n", "").replace("\t", "").replace("Date of experience: ", ""),
                                  "%B %d, %Y").strftime("%d/%m/%Y")
                for elem in soup.select("article section div p.typography_body-m__xgxZ_")
            ]
            review_date.extend(date)

            # rating
            rating = [int(elem['data-service-review-rating']) for elem in
                      soup.select('.styles_reviewHeader__iU9Px[data-service-review-rating]')]
            review_rating.extend(rating)

            # content
            for div_element in soup.find_all('div', class_='styles_reviewContent__0Q2Tg'):
                p_element = div_element.find('p',
                                             class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn',
                                             attrs={'data-service-review-text-typography': 'true'})

                if p_element:
                    review_text = p_element.get_text(strip=True)
                    review_content.append(review_text)
                else:
                    review_content.append("")

            # location
            location = [
                elem.get_text(strip=True)
                for elem in soup.select("article div.typography_appearance-subtle__8_H2l span")
                if elem.find_parent("div", class_="styles_consumerExtraDetails__fxS4S")
            ]
            review_location.extend(location)

            page_number.append(i)

    data = {
        'review_id': review_id,
        'review_title': review_title,
        'review_date': review_date,
        'review_rating': review_rating,
        'review_content': review_content,
        'review_location': review_location,
    }

    data['review_date'] = pd.to_datetime(data['review_date'], format='%d/%m/%Y')

    df = pd.DataFrame(data)
    return df


# File upload using Streamlit's file_uploader

# Input fields for scraping parameters
st.sidebar.subheader("Scraping Parameters")
url = st.sidebar.text_input("Trustpilot URL", "https://www.trustpilot.com/review/example")
from_page = st.sidebar.number_input("From Page", min_value=1, value=1)
to_page = st.sidebar.number_input("To Page", min_value=from_page, value=from_page)

# Button to trigger scraping function
import requests

try:
    if st.sidebar.button("Scrape Trustpilot Reviews"):
        st.info("Scraping in progress. Please wait...")
        
        # Call the scraping function with user input
        scraped_data = scrape_trustpilot_reviews(url, from_page, to_page)
        
        if scraped_data.empty:
            st.warning("No data could be scraped. Please provide a valid URL or upload a CSV file.")
        else:
            # Display the scraped data outside the if block
            st.header('Scraped Data')
            st.write(scraped_data)  # This line might need to be adjusted based on the structure of your code
            st.success("Scraping completed successfully!")

    else:
        st.warning("Please provide a valid URL on the side scraping paramenters or upload a CSV file.")

except requests.exceptions.ConnectionError:
    st.warning("Connection error. Please check your internet connection and try again.")
    st.warning("Alternatively, input a valid URL or upload a CSV file.")


def get_sentiment(row):
    if pd.notna(row['review_rating']) and row['review_rating'] != '':
        try:
            rating = int(row['review_rating'])
            if rating == 1 or rating == 2:
                return "negative"
            elif rating == 3:
                return "neutral"
            elif rating == 4 or rating == 5:
                return "positive"
        except ValueError:
            pass

    if 'review_content' in row.index and pd.notna(row['review_content']):
        # If review_rating is empty or not a valid integer, use TextBlob for sentiment analysis
        analysis = TextBlob(row['review_content'])
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity < 0:
            return "negative"
        else:
            return "neutral"
    
    # If none of the conditions are met, return None or any default value
    return None
