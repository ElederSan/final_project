import streamlit as st
from st_pages import add_page_title, hide_pages
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from streamlit_extras.let_it_rain import rain
import random

st.image("Logo.jpg", width=300)

data = pd.read_excel("amazon_neutral.xlsx",engine='openpyxl')
df = data.sample(5)
df = data

# Streamlit app
st.header("Help us train :weight_lifter: our models and get 10% off your monthly price")
st.image("blank_space.jpg",width=600)

st.subheader('Review Sentiment Analyzer')

def send_email(reviews):
    # Configure your email server details
    email_address = 'sentimentsurvey55@gmail.com'  # Replace with your Gmail address
    app_password = 'wdnp tuyl cycr crxa'  # Replace with the actual App Password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, app_password)

    # Email content
    subject = 'User Feedback'
    body = '\n'.join([f"{i + 1}. {review}" for i, review in enumerate(reviews)])

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = 'sentimentsurvey55@gmail.com'  # Replace with your destination email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    server.sendmail(email_address, msg['To'], msg.as_string())
    server.quit()


# Display reviews with horizontal radio buttons for sentiment selection
for i in range(5):
    st.subheader(f'Review {i + 1}: {df["review_content"][i]}')
    sentiment_options = ['😃 positive', '😐 neutral', '😟 negative']
    selected_sentiment = st.radio(f'Select sentiment for Review {i + 1}:', sentiment_options, key=f'sentiment_{i}')
    sentiments_mapping = {'😃 positive': 'positive', '😐 neutral': 'neutral', '😟 negative': 'negative'}
    df.at[i, 'Sentiment'] = sentiments_mapping[selected_sentiment]

#Button to submit and send email
if st.button('Submit Feedback'):
   st.write('Sending feedback...')
    #selected_reviews = df[df['Sentiment'] != '']['review_content'].tolist()
   selected_reviews = df.dropna(subset=['Sentiment'])['review_content'].tolist()
   if selected_reviews:
        send_email(selected_reviews)
        st.success('Feedback submitted successfully!')
        st.success('Remember, La kappa te CAPA.')  # Display the additional message
else:
    st.warning('Please select sentiments for all reviews before submitting.')


# Display the DataFrame
st.dataframe(df)

