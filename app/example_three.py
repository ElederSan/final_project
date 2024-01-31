import time # for simulating a real-time data, time loop          
import numpy as np     
import pandas as pd # read csv, df manipulation                 
import plotly.express as px # interactive charts              
import streamlit as st # data web application development

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    page_icon="Active",
    layout="wide",
)

def get_data(file_path):
    # Your data loading code here, using the provided file path
    data = pd.read_csv(file_path)
    return data

data = get_data("expondo_reviews_since_2023.csv")

# dashboard title                   
#st.title("Real-Time Dashboard")

# top-level filters          
# review_date = st.selectbox("Select the status", pd.unique(data["review_date"]))
# Assuming data is your DataFrame
# Assuming data is your DataFrame
# Top-level filters
review_date_options = ['Clear Selection'] + list(pd.unique(data["review_date"]))
review_date = st.selectbox("Select the date", review_date_options)

# Check if the user selected "Clear Selection"
if review_date == 'Clear Selection':
    st.info("Selection cleared. No specific date filter applied.")
else:
    # Filter data based on the selected review date
    filtered_data = data[data["review_date"] == review_date]
    st.success(f"Filtering by date: {review_date}")

# create columns              
kpi1, kpi2 = st.columns(2)                

# fill the column with respect to the KPIs
num_reviews = data['review_id'].nunique()      
#kpi1.metric         
kpi1 = st.metric(
    label="Number of reviews",
    value=num_reviews,
    delta=num_reviews - 10
)         

# kpi2.metric           
kpi2 = st.metric(
    label="Number of reviews",
    value=num_reviews,
    delta=num_reviews - 10
)            


# create columns for the chars             
# create columns for the chars   

data['review_date'] = pd.to_datetime(data['review_date'])
reviews_per_date = data.groupby('review_date').size().reset_index(name='num_reviews')

avg_rating_per_month = (
    data.groupby(data['review_date'].dt.to_period("M"))['review_rating']
    .mean()
    .round(1)
    .reset_index())

# Convert 'review_date' to datetime
avg_rating_per_month['review_date'] = pd.to_datetime(avg_rating_per_month['review_date'].astype(str))

# Sort the DataFrame by 'review_date' in chronological order
avg_rating_per_month = avg_rating_per_month.sort_values('review_date')

# Convert 'review_date' back to string for plotting (optional)
avg_rating_per_month['review_date'] = avg_rating_per_month['review_date'].dt.strftime('%Y-%m')


fig_col1, fig_col2 = st.columns(2)                           


with fig_col1:                  
    st.markdown ("### Chart 1")                     
    fig1= px.line(reviews_per_date, x='review_date', y='num_reviews', markers=True, line_shape='linear')
    fig1.update_layout(title_text='Number of Reviews per Review Date',
    xaxis_title='Review Date',
    yaxis_title='Number of Reviews',
    showlegend=False)            
    st.write(fig1)            

with fig_col2:                    
    st.markdown ("### Chart 2")          
    fig2 = px.line(avg_rating_per_month, x='review_date', y='review_rating', markers=True, line_shape='linear')
    fig2.update_layout(title_text='Average review rating per month',
    xaxis_title='Review Date',
    yaxis_title='Avg review rating per month',
    showlegend=False)          
    st.write(fig2)                


