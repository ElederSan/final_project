import streamlit as st
from st_pages import add_page_title, hide_pages
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sample DataFrame
data = {
    'Review': ['Great product!', 'Not satisfied with the service.', 'Average experience.',
               'Amazing support!', 'Could be better.'],
    'Sentiment': ['','','','','']  # Initialize with empty strings
}

df = pd.DataFrame(data)

# Streamlit app
st.header('Review Sentiment Analyzer')

# Function to send emails
def send_email(reviews):
    # Configure your email server details
    email_address = 'your_email@gmail.com'
    password = 'your_email_password'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, password)

    # Email content
    subject = 'User Feedback'
    body = '\n'.join([f"{i + 1}. {review}" for i, review in enumerate(reviews)])

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = 'destination_email@example.com'  # Replace with your destination email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    server.sendmail(email_address, msg['To'], msg.as_string())
    server.quit()

# Display reviews with horizontal radio buttons for sentiment selection
for i in range(5):
    st.subheader(f'Review {i + 1}: {df["Review"][i]}')
    sentiment_options = ['😃 positive', '😐 neutral', '😟 negative']
    selected_sentiment = st.radio(f'Select sentiment for Review {i + 1}:', sentiment_options, key=f'sentiment_{i}')
    sentiments_mapping = {'😃 positive': 'positive', '😐 neutral': 'neutral', '😟 negative': 'negative'}
    df.at[i, 'Sentiment'] = sentiments_mapping[selected_sentiment]

# Button to submit and send email
if st.button('Submit Feedback'):
    st.write('Sending feedback...')
    selected_reviews = df[df['Sentiment'] != '']['Review'].tolist()
    if selected_reviews:
        send_email(selected_reviews)
        st.success('Feedback submitted successfully!')
    else:
        st.warning('Please select sentiments for all reviews before submitting.')

# Display the DataFrame
#st.dataframe(df)


