import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.genai_sales_analysis import analyze_negative_comments
import os

def reddit_dashboard():
    st.title("Tata Motors Reddit Comments Sentiment Analysis")

    sentiment_path = "notebooks/data/reddit_comments_sentiment.csv"
    emotion_path = "notebooks/data/reddit_comments_sentiment_emotion.csv"
    df = pd.read_csv(sentiment_path)

    # Load emotion CSV if available
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

    if st.checkbox("Show raw data"):
        st.write(df)

    st.subheader("Sentiment Distribution")
    sent_counts = df['sentiment'].value_counts()
    st.bar_chart(sent_counts)

    st.subheader("Sentiment Distribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("Emotion Distribution (Donut Chart)")
    if df_emotion is not None and 'emotion' in df_emotion.columns:
        emotion_counts = df_emotion['emotion'].value_counts()
        labels = emotion_counts.index.tolist()
        sizes = emotion_counts.values.tolist()

        # Collapse very small emotions into 'Other'
        threshold = 0.015
        total = np.sum(sizes)
        big_labels, big_sizes = [], []
        small_total = 0
        for l, s in zip(labels, sizes):
            if s / total > threshold:
                big_labels.append(l)
                big_sizes.append(s)
            else:
                small_total += s
        if small_total > 0:
            big_labels.append('Other')
            big_sizes.append(small_total)

        colors = plt.cm.Set3.colors[:len(big_labels)]

        fig2, ax2 = plt.subplots()
        wedges, texts, autotexts = ax2.pie(
            big_sizes, labels=big_labels, autopct='%1.1f%%', pctdistance=0.85,
            startangle=90, colors=colors, textprops={'fontsize': 8}  # label font smaller
        )
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')

        # Set even smaller font for percentage annotations:
        for autotext in autotexts:
            autotext.set_fontsize(5)
        for text in texts:
            text.set_fontsize(4)

        st.pyplot(fig2)
    else:
        st.info("No emotion data found in emotion CSV.")

    st.write("Sentiment Distribution (%)")
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", sorted(df['sentiment'].unique()))
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['comment', 'language', 'translated_comment']]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    st.dataframe(filtered[preview_cols])

    # GenAI analysis button for Negative sentiment only
    if selected_sentiment == "Negative":
        if st.button("GenAI Sales Analysis"):
            with st.spinner("Analyzing with GPT-4, please wait..."):
                sales_advice = analyze_negative_comments(filtered)
            st.subheader("GenAI Sales Strategy Suggestions")
            for strategy in sales_advice:
                st.write(f"- {strategy}")
