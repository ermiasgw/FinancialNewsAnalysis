# -*- coding: utf-8 -*-
"""clean_data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NtP3W7YFzPOxUgsrUbvh066Ok4IUQXs6

# Download ratings data
"""

import pandas as pd

def download_data():
  data = pd.read_csv("https://www.dropbox.com/scl/fi/t5tdso2dhahny33bzqgnt/raw_analyst_ratings.csv?rlkey=a9gy46ltupqrexj6r6gs3n8f4&st=5zzopfih&dl=1")
  return data

data = download_data()
data.head()

"""# cleaning the data"""

data.columns

"""remove unamed and url columns which are not needed"""

data = data.drop(columns=['url'], axis=1)

data = data.drop(columns=['Unnamed: 0'], axis=1)

data.head()

"""check for data types and correct"""

data.dtypes

data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

data['date']

data = data.dropna()

data

data.dtypes

"""drop rows with not popular symbols"""

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
symbols = tickers['Symbol'].tolist()
data = data[data['stock'].isin(symbols)]
data

"""# Descriptive Statistics

calculate min, median and max length of headlines.
"""

headlines_lengths = data['headline'].str.len()
min_length = headlines_lengths.min()
median_length = headlines_lengths.median()
max_length = headlines_lengths.max()

print("min length = ", min_length)
print("median length = ", median_length)
print("max length = ", max_length)

"""Count the number of articles per publisher to identify which publishers are most active.

"""

articles_per_publisher = data.groupby('publisher').size().reset_index(name='article_count')
articles_per_publisher

"""Analyze the publication dates to see trends over time, such as increased news frequency on particular days or during specific events.

"""

import matplotlib.pyplot as plt

data['month'] = data['date'].dt.strftime('%Y-%m')

# Count the number of articles published each month
articles_per_month = data['month'].value_counts().sort_index()

# Plot the monthly bar chart
plt.figure(figsize=(10, 6))
articles_per_month.plot(kind='bar', color='skyblue')
plt.title('Number of Articles Published Each Month')
plt.xlabel('Month')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

data = data.drop(columns=['month'])

data['year'] = data['date'].dt.year

# Count the number of articles published each year
articles_per_year = data['year'].value_counts().sort_index()

# Plot the yearly bar chart
plt.figure(figsize=(10, 6))
articles_per_year.plot(kind='bar', color='skyblue')
plt.title('Number of Articles Published Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

data = data.drop(columns=['year'])

"""# Text Analysis(Sentiment analysis & Topic Modeling)

Perform sentiment analysis on headlines to gauge the sentiment (positive, negative, neutral) associated with the news.
"""

from textblob import TextBlob

sentiments = []
for headline in data['headline']:
    blob = TextBlob(headline)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    sentiments.append(sentiment)

# Add sentiment column to DataFrame
data['sentiment'] = sentiments
data

"""Use natural language processing to identify common keywords or phrases, potentially extracting topics or significant events (like "FDA approval", "price target", etc.).

"""