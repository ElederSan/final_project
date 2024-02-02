import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import matplotlib.pyplot as plt

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

# Streamlit setup
st.title("Trustpilot Review Scraper")

# File upload using Streamlit's file_uploader

# Input fields for scraping parameters
st.sidebar.subheader("Scraping Parameters")
url = st.sidebar.text_input("Trustpilot URL", "https://www.trustpilot.com/review/example")
from_page = st.sidebar.number_input("From Page", min_value=1, value=1)
to_page = st.sidebar.number_input("To Page", min_value=from_page, value=from_page)

# Button to trigger scraping function
if st.sidebar.button("Scrape Trustpilot Reviews"):
    st.info("Scraping in progress. Please wait...")
        
    # Call the scraping function with user input
    scraped_data = scrape_trustpilot_reviews(url, from_page, to_page)
    # Display the scraped data outside the if block
    #st.header("Scraped Data")
    st.write(scraped_data)  # This line might need to be adjusted based on the structure of your code
    st.success("Scraping completed successfully!")
else:
    st.warning("Please provide a valid url or upload a CSV file .")

uploaded_file = st.file_uploader('Upload your file here')

if uploaded_file:
    #st.header('Data Statistics')
    df = pd. read_csv(uploaded_file)

    st.write(df.describe())

    #st.header('Data Header')
    st.write(df.head())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plotting the first subplot
    ax1.plot(df['review_date'], df['review_rating'])
    ax1.set_xlabel('review_date')
    ax1.set_ylabel('review_rating')
    ax1.set_title('First Subplot')

    # Plotting the second subplot
    ax2.plot(df['review_date'], df['review_rating'])
    ax2.set_xlabel('review_date')
    ax2.set_ylabel('review_rating')
    ax2.set_title('Second Subplot')

    # Display the figure in Streamlit
    st.pyplot(fig)