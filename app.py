import streamlit as st
import pandas as pd
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- App title ---
st.title("📰 News Sentiment Analyzer")

# --- Get user input ---
api_key = st.text_input("Enter your News API key")
query = st.text_input("Enter a topic (e.g. AI, Politics, Sports):")

if st.button("Analyze News"):
    if not api_key or not query:
        st.warning("Please enter both API key and topic.")
    else:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey=be0238a91b7f6382dc296c4c273af92b"
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            st.error("No news found or invalid API key.")
        else:
            articles = data["articles"]
            analyzer = SentimentIntensityAnalyzer()

            news_data = []
            for article in articles[:20]:  # analyze top 20 articles
                title = article["title"]
                description = article["description"] or ""
                score = analyzer.polarity_scores(description)
                compound = score['compound']

                if compound >= 0.05:
                    sentiment = "Positive"
                elif compound <= -0.05:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

                news_data.append({
                    "Title": title,
                    "Description": description,
                    "Sentiment": sentiment
                })

            df = pd.DataFrame(news_data)
            st.dataframe(df)

            # --- Sentiment summary chart ---
            st.subheader("Sentiment Distribution")
            st.bar_chart(df["Sentiment"].value_counts())
