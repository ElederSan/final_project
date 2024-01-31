from pathlib import Path
import streamlit as st
from st_pages import Page, add_page_title, show_pages, show_pages_from_config

st.image("Logo.jpg", width=300)

# Add a header with text and a button
st.write("Welcome to my multipage app!")



# Your existing code for declaring pages
with st.echo("below"):
    from st_pages import Page, add_page_title, show_pages

    "## Declaring the pages in your app:"
    show_pages(
        [
            Page("multipage_app2.py", "Home", "🏠"),
            Page("example_one.py", "Why sentiment analysis"),
            Page("example_two.py", "Pricing"),
            #Page("example_three.py", "Example Three"),
            #Page("example_three.py"),
            #Page("example_five.py", "Benchmarkt"),
            Page("example_six.py", "Benchmarkt"),
            Page("example_seven.py", "Performance Dashboard"),
            Page("example_eight.py", "Sentiment comparison"),
            Page("example_four.py", "Help us to help you!"),
        ]
    )
