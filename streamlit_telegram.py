import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.genai_sales_analysis import analyze_negative_comments


def telegram_dashboard():
    st.title("Tata Motors Telegram Comments Sentiment Analysis")

    data_path = "notebooks/data/tatamotors_telegram_sentiment.csv"
    df = pd.read_csv(data_path)

    if st.checkbox("Show raw data"):
        st.write(df)

    st.subheader("Sentiment Distribution")
    sent_counts = df['sentiment'].value_counts()
    st.bar_chart(sent_counts)

    st.subheader("Sentiment Distribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.0f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    st.write("Sentiment Distribution (%)")
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", sorted(df['sentiment'].unique()))
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['message', 'language', 'translated_message']]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    st.dataframe(filtered[preview_cols])

    # Add GenAI analysis button only if sentiment is Negative
      # Add GenAI analysis button for negative comments
    if selected_sentiment == "Negative":
        if st.button("GenAI Sales Analysis"):
            sales_advice = analyze_negative_comments(filtered)
            st.subheader("GenAI Sales Strategy Suggestions")
            for strategy in sales_advice:
                st.write(f"- {strategy}")
