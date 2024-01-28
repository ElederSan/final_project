import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# First tab

# Your main content goes here...
# Create a selectbox to choose between tabs
selected_tab = st.sidebar.radio("Select Tab", ["About us", "Sentiment what is","Pricing","Company performance","Benchmark",])

# Conditionally show content based on the selected tab
if selected_tab == "About us":
    st.title('Tab 1:Trustpilot review and sentiment analysis')
    st.text('This is a web app to explore the sentiment. ')

    uploaded_file = st.file_uploader('Upload your file here')

    if uploaded_file:
        st.header('Data Statistics')
        df = pd. read_csv(uploaded_file, sep=';')

        st.write(df.describe())

        st.header('Data Header')
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



elif selected_tab == "Sentiment what is":
    st.title("Tab 2: Additional Content")
    # Additional content for Tab 2...

elif selected_tab == "Pricing":
    st.title("Tab 3: Additional Content")
    # Additional content for Tab 2...

elif selected_tab == "Benchmark":
    st.title("Tab 4: More Content")
    # More content for Tab 3...



