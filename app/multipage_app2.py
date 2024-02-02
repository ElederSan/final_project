from pathlib import Path
from turtle import width
import streamlit as st
from st_pages import Page, add_page_title, show_pages, show_pages_from_config

st.image("Logo.jpg", width=300)


top_row = st.container()
second_row = st.container()
third_row = st.container()
fourth_row = st.container()
fifth_row = st.container()


with top_row:
    st.image("blank_space.jpg",width=600)
    st.image("who_are_we.jpg",width=1900)
    st.image("blank_space.jpg",width=600)
with second_row:
    st.image("powering.jpg",width=1900)
    st.image("blank_space.jpg",width=600)
    st.image("ironsentiment_offer.jpg",width = 1900)
with third_row:
    st.image("blank_space.jpg",width =600)
with fourth_row:
    st.image("blank_space.jpg",width =1900)
    st.image("questions_to_answer.jpg",width=1900)

with fifth_row:
    st.image("blank_space.jpg",width=1900)
    st.image("blank_space.jpg",width=1900)
    st.image("blank_space.jpg",width=1900)
    st.image("blank_space.jpg",width=1900)
    st.image("blank_space.jpg",width=1900)
    st.image("blank_space.jpg",width=1900)














































































# Add a header with text and a button
#st.write("Welcome to my multipage app!")



# Your existing code for declaring pages
with st.echo("below"):
    from st_pages import Page, add_page_title, show_pages

    #"## Declaring the pages in your app:"
    show_pages(
        [
            Page("multipage_app2.py", "Home"),
            Page("why_sentiment.py", "Why sentiment analysis"),
            Page("pricing.py", "Pricing"),
            #Page("example_three.py", "Example Three"),
            #Page("example_three.py"),
            #Page("example_five.py", "Benchmarkt"),
            #Page("example_six.py", "Benchmarkt"),
            Page("performance_dashboard.py", "Performance Dashboard"),
            Page("sentiment_comparison.py", "Sentiment comparison"),
            Page("help_us.py", "Help us to help you!"),
        ]
    )
