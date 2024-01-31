import streamlit as st
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
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.image("Logo.jpg", width=300)
# Set option to display full text in columns

# Function to generate random text
def generate_random_text():
    texts = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        # Add more random text as needed
    ]
    return random.choice(texts)

# Function to generate random images
def generate_random_image():
    images = [
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150/0000FF/808080?text=Image+1",
        "https://via.placeholder.com/150/FF0000/FFFFFF?text=Image+2",
        # Add more image URLs as needed
    ]
    return random.choice(images)
      

def plot_avg_review_month():
    avg_rating_per_month = df.groupby(['month_year_str']).agg({'review_rating': 'mean'}).round(2).reset_index()
    fig = px.area(
        avg_rating_per_month,
        x="month_year_str",
        y="review_rating",
        #color="sentiment",
        markers=True,
        text="review_rating",
        title="Avg. reviews per month since 2023",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

#plot_avg_review_month()()

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
      
    #avg_rating = df['review_rating'].mean().round(2)
    num_reviews = int(df["review_id"].nunique())
    positive_reviews = int(df[df['sentiment'] == 'positive'].shape[0])
    neutral_reviews = int(df[df['sentiment'] == 'neutral'].shape[0])
    negative_reviews = int(df[df['sentiment'] == 'negative'].shape[0])
    avg_reviews_day = round(float(df["review_id"].nunique())/int(df['review_date'].nunique()),2)
    total_countries=int(df["review_location"].nunique())

    col1, col2, col3, col4,col5 = st.columns(5)
    
    create_metric_card(col1, "Total reviews", num_reviews)
    create_metric_card(col2, "Reviews per day", avg_reviews_day)
    create_metric_card(col3, "Positive reviews", positive_reviews)
    create_metric_card(col4, "Neutral reviews", neutral_reviews)
    create_metric_card(col5, "Negative reviews", negative_reviews)
    #create_metric_card(col6, "Total countries", total_countries)
# Display the metric cards
#st.title('Review Metrics')
#plot_metric_cards(df)

def plot_sentiment_time():
    sentiment_reviews_per_month = df.groupby(['month_year_str', 'sentiment']).size().reset_index(name='sentiment_reviews')
    fig = px.line(
        sentiment_reviews_per_month,
        color="sentiment",
        x="month_year_str",
        y="sentiment_reviews",
        color_discrete_map= {'positive': 'green', 'neutral': 'yellow', 'negative': 'red'},
        markers=True,
        #text="sentiment",
        title="Reviews per sentiment",
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
    showlegend=True,
    legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)

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


def plot_top_countries():
    sentiment_counts_per_country = df.groupby(['country_iso3', 'sentiment']).size().reset_index(name='count')
    total_counts = sentiment_counts_per_country.groupby(['country_iso3', 'sentiment'])['count'].sum().reset_index()
    top_countries = total_counts.groupby('country_iso3')['count'].sum().sort_values(ascending=False).head(5).index
    top_countries_df = total_counts[total_counts['country_iso3'].isin(top_countries)]
    top_countries_df=top_countries_df.sort_values(by="count",ascending=False)
    fig = px.bar(top_countries_df, x='count', y='country_iso3', color='sentiment',
                color_discrete_map= {'positive': 'green', 'neutral': 'yellow', 'negative': 'red'},
                title='Sentiment in Top 5 Countries',
                labels={'count': 'Total Count'}
    )
    fig.update_layout(
    showlegend=False,
    legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="left", x=0),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)


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


# Set the width of the containers

container_width = 1000        
width_col1 = 1000
#width_col2 = 10
width_col3= 1000

# Create two columns for placing containers side by side
col1,col3 = st.columns(2)

# Create the first container in the first column
with col1:
    ""
    

#with col2:
    " "

# Create the second container in the second column

################################################

