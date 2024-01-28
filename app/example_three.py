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
st.title("Real-Time Dashboard")

# top-level filters          
# review_date = st.selectbox("Select the status", pd.unique(data["review_date"]))
# Assuming data is your DataFrame
# Assuming data is your DataFrame
review_date_options = pd.unique(data["review_date"])

# Add a "Clear Selection" option to the list of unique values
review_date_options = ['Clear Selection'] + list(review_date_options)

# Display the select box
review_date = st.selectbox("Select the date", review_date_options)

# Check if the user selected "Clear Selection"
if review_date == 'Clear Selection':
    # Handle the case where the user wants to clear the selection
    st.info("Selection cleared. No specific date filter applied.")
else:
    # Handle the case where a specific status is selected
    st.success(f"Filtering by status: {review_date}")
    # Continue with the rest of your code based on the selected filter

st.write(data.head())

# create columns for the chars             
# create columns for the chars             
fig_col1, fig_col2 = st.columns(2)                           


with fig_col1:                  
    st.markdown (“### Chart 1”)                     
    fig1 = px.density_heatmap                     
    {             
    data_frame = df, y =”status_drinking_new”, x = “drinking_habits”            
    }                
    st.write(fig)            

with fig_col2:                    
    st.markdown (“### Chart 2”)          
    fig2 = px.histogram (data_frame = df, x =”status_drinking_new”)                
    st.write(fig2)                        
