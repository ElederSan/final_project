import streamlit as st
from st_pages import add_page_title
import pandas as pd

st.set_page_config(layout='wide')
st.image("Logo.jpg", width=300)

top_row = st.container()
second_row = st.container()
third_left_column,third_middle_column, third_right_column = st.columns(3)
fifth_row = st.container()
fourth_row = st.container()


with top_row:
    st.header("Customer feedback is worth millions....we only charge you a small fee :sunglasses:!")
    #st.image('pricing_example.jpg',width=1200)

with second_row:
    st.image('blank_space.jpg',width=1200)
    
with third_left_column:
    st.image('basic_pricing.jpg',width=500)

with third_middle_column:
    st.image('company_pricing.jpg',width=500)

with third_right_column:
    st.image('premium_pricing.jpg',width=500)

with fifth_row:
    st.image('blank_space.jpg',width=1200)
    st.header("You're in good company:")
    st.subheader("IronSentiment is trusted by over 300 companies in Germany and growing every day")
    st.image('blank_space.jpg',width=1200)

    st.image("companies_logos.jpg",width=2000)

with fourth_row:
    st.image('blank_space.jpg',width=1200)
    st.image('app_features.jpg',width=1900)
