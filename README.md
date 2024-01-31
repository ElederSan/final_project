# Customer Reviews Analysis

## Overview

This repository contains data and analysis tools for understanding customer sentiments and reviews. The dataset comprises reviews of products/services from various customers, providing valuable insights for business decision-making.

## Dataset Information

We use different datasets scraped from Trustpilot (only for learning purposes)

- **Columns:**
  - `review_id`: Unique identifier for each review
  - `review_title`: Title of the review
  - `review_date`: Date when the review was posted
  - `review_rating`: Rating given by the customer (1 to 5)
  - `review_content`: Detailed content of the review
  - `review_location`: Location of the reviewer

## Analysis Tools

### 1. Sentiment Analysis
- Understand sentiments associated with each review.
- Identify positive and negative trends over time.

### 2. Geographical Analysis
- Explore variations in ratings and sentiments based on reviewer locations.

### 3. Product-specific Insights
- Analyze sentiments related to specific products for product improvement.

### 4. Customer Support Evaluation
- Assess customer satisfaction with support services through reviews.

### 5. Delivery and Return Analysis
- Examine sentiments related to delivery and return experiences.

## App features:

- App contains a performance dashboard, containing the breakdown of reviews for the specific company, in this case Expondo (my company)
- It also has a sentiment comparison tool, which allows to compare side by side the performance between our customer and the main competitors. This tool works dynamically,allowing to scrape reviews from other competitors or upload a csv file with reviews from other tools.
- The last tab encourages the customers to provide feedback on neutral reviews, which are the most missleading, which are then collected via email. This data shall help process a reinforcement training, to improve the performance of our models.

## Business Questions

1.How is customer satisfaction trending based on review ratings and sentiments?
2.What are the geographical variations in average ratings and sentiments?
3. Which sentiments are commonly associated with specific products in customer reviews?
4. What is the overall sentiment regarding delivery services, and are there country-specific patterns?
5. How does our average review rating compare with competitors in the industry?


## How to Use

1. Clone the repository to your local machine.
2. Explore the Jupyter Notebooks for detailed analyses.
3. Customize analyses based on your specific business questions.
4. Contribute by adding new analyses or improving existing ones.

