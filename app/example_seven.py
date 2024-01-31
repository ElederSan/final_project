import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
import datetime as dt
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from functions_for_app import *

plt.style.use("ggplot")
#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.image("Logo.jpg", width=300)
#st.title("Expondo Review dashboard")
#st.markdown("_Prototype v0.4.1_")

#with st.sidebar:
#    uploaded_file = st.file_uploader("Choose a file")

#if uploaded_file is None:
#    st.info(" Upload a file through config", icon="ℹ️")
#    st.stop()



#######################################
# DATA LOADING
#######################################



@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df

df = load_data("expondo_reviews_since_2023.csv")
df['sentiment'] = df.apply(get_sentiment, axis=1)
df['review_date'] = pd.to_datetime(df['review_date'])
df['month_year'] = df['review_date'].dt.to_period("M")
df['month_year_str'] = df['month_year'].dt.strftime('%Y-%m')
country_dict = pd.read_excel("country_dict.xlsx")

df_merged = pd.merge(df, country_dict[['Alpha-2 code', 'Alpha-3 code']], left_on='review_location', right_on='Alpha-2 code', how='left')

# Drop the redundant column
df_merged.drop(columns=['Alpha-2 code'], inplace=True)

# Rename the merged column to 'country_iso3'
df_merged.rename(columns={'Alpha-3 code': 'country_iso3'}, inplace=True)

df = df_merged.drop_duplicates()
df = df.reset_index()




#######################################
# VISUALIZATION METHODS
#######################################
    
def plot_number_reviews(df):
    reviews_month = df.groupby(["month_year_str", "review_rating"]).size().reset_index(name='num_reviews')
    fig = px.bar(
        reviews_month,
        x="month_year_str",
        y="num_reviews",
        color="review_rating",  # Optional: Color by review rating
        text="num_reviews",
        title="Reviews per month since 2023",
    )
    fig.update_traces(textposition="auto")
    st.plotly_chart(fig, use_container_width=True)

# Assuming 'df' is your DataFrame containing the reviews
# Add the necessary data loading steps if not already loaded
# ...

# Assuming 'df' has the necessary columns like 'month_year_str' and 'review_rating'
#plot_number_reviews(df)



def plot_avg_review_month():
    avg_rating_per_month = df.groupby(['month_year_str']).agg({'review_rating': 'mean'}).round(2).reset_index()
    fig = px.area(
        avg_rating_per_month,
        x="month_year_str",
        y="review_rating",
        #color="review_rating",
        markers=True,
        text="review_rating",
        title="Avg. reviews per month since 2023",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

#plot_avg_review_month()()

def plot_location_avg_review():
    
    avg_rating_per_location = df.groupby('review_location').agg({'review_rating': ['mean', 'count']}).round(2)
    avg_rating_per_location.columns = ['avg_rating', 'num_reviews']
    # Sort the DataFrame by the number of reviews in descending order
    avg_rating_per_location = avg_rating_per_location.sort_values(by='num_reviews', ascending=False)
    top_10_locations = avg_rating_per_location.nlargest(10, 'num_reviews').sort_values(by='num_reviews', ascending=False)

    fig = px.bar(
        top_10_locations,
        y=top_10_locations.index,  # Assuming 'location' is the index
        x="avg_rating",  # Assuming this is the column with average ratings
        color="num_reviews",  # You can use color to represent the number of reviews
        text="avg_rating",  # Display the average rating as text on the bars
        title="Top 10 Locations by Average Ratings (sorted by number of reviews)",
        
    )
    fig.update_traces(textposition="outside")  # Adjust the text position for better visibility
    fig.update_layout(xaxis_categoryorder='total ascending')   # Sort the bars by the number of reviews
    st.plotly_chart(fig, use_container_width=True)

# plot_location_avg_review()

def color_based_on_rating(avg_rating):
    if 1 < avg_rating < 3:
        return 'red'
    elif 3 <= avg_rating < 4:
        return 'yellow'
    elif avg_rating >= 4:
        return 'green'
    else:
        return 'gray'  # You can set a default color for other cases

def plot_gauge(df, rating_column='review_rating'):
    # Calculate the overall average review rating
    avg_rating = df[rating_column].mean().round(2)
    # Set parameters for the gauge chart
    indicator_number = avg_rating
    indicator_color = color_based_on_rating(avg_rating)
    indicator_suffix = ''
    indicator_title = 'Average Review Rating'
    max_bound = 5.0  # Assuming the ratings are on a scale from 0 to 5, adjust based on your data

    # Create the gauge chart
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )

    # Adjust layout settings
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

# Assuming 'df' is your DataFrame containing the 'review_rating' column
# Call the function with the DataFrame and column name
#plot_gauge(df, rating_column='review_rating')

# Function to create metric cards
def create_metric_card(column, label, value, delta=None):
    metric_card = column.metric(
        label=label,
        value=value,
        delta=None,
    )
    return metric_card

# Function to generate all metric cards
def plot_metric_cards(df):
      
    avg_rating = round(df['review_rating'].mean(),2)
    num_reviews = int(df["review_id"].nunique())
    avg_reviews_day = round(float(df["review_id"].nunique())/int(df['review_date'].nunique()),2)
    total_countries=int(df["review_location"].nunique())

    col1, col2, col3, col4 = st.columns(4)
    
    create_metric_card(col1, "Number of reviews", num_reviews)
    create_metric_card(col2, "Avg reviews", avg_rating)
    create_metric_card(col3, "Avg reviews per day", avg_reviews_day)
    create_metric_card(col4, "Total countries", total_countries)


# Display the metric cards
#st.title('Review Metrics')
#plot_metric_cards(df)


def plot_avg_rating_map(df):
    avg_rating_per_country = df.groupby('country_iso3')['review_rating'].mean().round(2).reset_index()

    fig = px.choropleth(
        avg_rating_per_country,
        locations='country_iso3',
        locationmode='ISO-3',  
        color='review_rating',
        color_continuous_scale='Blues',
        title='Average Rating by Country',
        labels={'review_rating': 'Average Rating'},
        scope='world'  # Adjust the scope based on the countries you have in the data
    )
    
       # Customizing the map appearance
    fig.update_geos(
        showcountries=True,
        countrycolor="lightgrey",
        showcoastlines=True,
        coastlinecolor="white",
        projection_type="natural earth"  # Adjust the projection for a better view
    )

    # Add colorbar title and adjust its position
    fig.update_coloraxes(colorbar_title='Average Rating', colorbar_x=0.02)

    # Update layout for a cleaner appearance
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['1', '2', '3', '4', '5'])
    )

    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Display the plot
#st.title('Review Metrics')
#plot_avg_rating_map(df)

def plot_wordcloud_positive():
    stop_words = set(stopwords.words('english'))

    # Function to get positive and negative words, removing stopwords
    def get_sentiment_words(text):
        sia = SentimentIntensityAnalyzer()
        tokens = word_tokenize(text)
        positive_words = [word.lower() for word in tokens if sia.polarity_scores(word)['compound'] > 0 and word.lower() not in stop_words]
        negative_words = [word.lower() for word in tokens if sia.polarity_scores(word)['compound'] < 0 and word.lower() not in stop_words]
        return positive_words, negative_words

    # Apply the function to your DataFrame
    df['positive_words'], df['negative_words'] = zip(*df['review_content'].astype(str).apply(get_sentiment_words))

    # Join all positive and negative words into two strings
    all_positive_words = ' '.join(df['positive_words'].sum())
    all_negative_words = ' '.join(df['negative_words'].sum())

    # Create word clouds for positive and negative words
    positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_positive_words)
    negative_wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(all_negative_words)

    # Plotly Figure for Positive Words
    positive_fig = px.imshow(positive_wordcloud.to_array(), binary_string=True, title='Positive Words')
    positive_fig.update_layout(title_x=0.5)
    st.plotly_chart(positive_fig)

#plot_wordcloud_positive()


def plot_wordcloud_negative():
    stop_words = set(stopwords.words('english'))

    # Function to get positive and negative words, removing stopwords
    def get_sentiment_words(text):
        sia = SentimentIntensityAnalyzer()
        tokens = word_tokenize(text)
        positive_words = [word.lower() for word in tokens if sia.polarity_scores(word)['compound'] > 0 and word.lower() not in stop_words]
        negative_words = [word.lower() for word in tokens if sia.polarity_scores(word)['compound'] < 0 and word.lower() not in stop_words]
        return positive_words, negative_words

    # Apply the function to your DataFrame
    df['positive_words'], df['negative_words'] = zip(*df['review_content'].astype(str).apply(get_sentiment_words))

    # Join all positive and negative words into two strings
    all_positive_words = ' '.join(df['positive_words'].sum())
    all_negative_words = ' '.join(df['negative_words'].sum())

    # Create word clouds for positive and negative words
    positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_positive_words)
    negative_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Reds_r').generate(all_negative_words)

    # Plotly Figure for Negative Words
    negative_fig = px.imshow(negative_wordcloud.to_array(), binary_string=True, title='Negative Words')
    negative_fig.update_layout(title_x=0.5)
    st.plotly_chart(negative_fig)

#plot_wordcloud_negative()

def plot_donut():
    sentiment_counts = df['sentiment'].value_counts()
    total_reviews = len(df)
    sentiment_percentages = pd.DataFrame(round((sentiment_counts / total_reviews) * 100))
    sentiment_percentages = sentiment_percentages.reset_index()
    sentiment_percentages = sentiment_percentages.rename({'count': 'percentage'})
    fig = px.pie(sentiment_percentages, values='count', names='sentiment', color='sentiment', hole=0.3,
                 color_discrete_map= {'positive': 'green', 'neutral': 'yellow', 'negative': 'red'},
                 title="Percentage per sentiment",
    )
    fig.update_layout(
    showlegend=True,
    legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)


#######################################
# STREAMLIT LAYOUT
#######################################

top_column = st.container()
second_row = st.container()
third_left_column, third_right_column = st.columns(2)
fourth_left_column, fourth_right_column = st.columns(2)
fifth_left_column,fifth_right_column = st.columns(2)

with top_column:
    plot_metric_cards(df)

with second_row:
    plot_number_reviews(df)

with third_left_column:
    plot_gauge(df, rating_column='review_rating')

with third_right_column:
    plot_donut()

with fourth_left_column:
   plot_location_avg_review()

with fourth_right_column:
    plot_avg_rating_map(df)

with fifth_left_column:
    plot_wordcloud_positive()

with fifth_right_column:
    plot_wordcloud_negative()

with st.expander("Data Preview"):
    st.dataframe(df)


