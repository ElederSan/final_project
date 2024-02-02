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

st.header("Why is review and sentiment analysis so important?")
st.image("blank_space.jpg",width=200)
st.subheader("Sentiment analysis is crucial as it enables businesses to understand and respond to customer emotions, enhancing decision-making and fostering improved products and services.")


top_row = st.container()
second_row = st.container()
third_left,third_middle,third_right = st.columns(3)
fourth_row=st.container()


with top_row:
    st.image("why_sentiment_grey.jpg",width=2000)
    # 

with third_left:
    ""
with third_middle:
    st.header("The cost of losing a customer :chart_with_downwards_trend:")
    st.image("blank_space.jpg",width=300)
    st.video('https://www.youtube.com/watch?v=iR8OxPFvaIc&t=88s')
with third_right:
    ""
with fourth_row:
    st.image("blank_space.jpg",width=600)
    st.image("literature.jpg",width=1900)
