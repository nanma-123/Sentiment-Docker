# app.py
import streamlit as st
import pandas as pd
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.title("📰 News Sentiment Analyzer (VADER)")

topic = st.text_input("Enter a news topic:", "Artificial Intelligence")

if st.button("Analyze Sentiment"):
    st.write(f"Fetching news for: **{topic}** ...")

    url = f"https://gnews.io/api/v4/search?q={topic}&lang=en&country=in&max=5&apikey=be0238a91b7f6382dc296c4c273af92b"
    response = requests.get(url)
    data = response.json()

    if "articles" in data:
        articles = pd.DataFrame(data["articles"])[["title", "description", "url"]]

        analyzer = SentimentIntensityAnalyzer()

        sentiments = []
        for i, row in articles.iterrows():
            text = row["description"] or row["title"]
            score = analyzer.polarity_scores(text)["compound"]
            if score >= 0.05:
                label = "POSITIVE"
            elif score <= -0.05:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            sentiments.append(label)

        articles["sentiment"] = sentiments
        st.dataframe(articles)
        st.bar_chart(articles["sentiment"].value_counts())
    else:
        st.error("No news found or invalid API key.")
