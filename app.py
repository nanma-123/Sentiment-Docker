import streamlit as st
import pandas as pd
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px

st.title("📰 News Sentiment Analyzer (VADER)")

topic = st.text_input("Enter a news topic:", "Artificial Intelligence")

if st.button("Analyze Sentiment"):
    st.write(f"Fetching news for: **{topic}** ...")

    url = f"https://gnews.io/api/v4/search?q={topic}&lang=en&country=in&max=5&apikey=YOUR_API_KEY"
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

        st.subheader("Results")
        st.dataframe(articles)

        # --- FIXED PART: Ensure all 3 bars appear ---
        sentiment_counts = articles["sentiment"].value_counts().reindex(
            ["POSITIVE", "NEGATIVE", "NEUTRAL"], fill_value=0
        )

        fig = px.bar(
            sentiment_counts,
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            color=sentiment_counts.index,
            title="Sentiment Distribution",
            labels={"x": "Sentiment", "y": "Count"}
        )
        st.plotly_chart(fig)

    else:
        st.error("No news found or invalid API key.")
