import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from src.genai_sales_analysis import analyze_negative_comments

def telegram_dashboard():
    st.title("Tata Motors Telegram Comments Sentiment Analysis")

    sentiment_path = "notebooks/data/tatamotors_telegram_sentiment.csv"
    emotion_path = "notebooks/data/tatamotors_telegram_emotion.csv"
    keyword_path = "notebooks/data/telegram_trending_keywords.csv"
    df = pd.read_csv(sentiment_path)
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

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

    st.subheader("Emotion Distribution (Donut Chart)")
    if df_emotion is not None:
        # NRC columns are all except index/message
        cols_exclude = ['index', 'message']
        emotion_cols = [col for col in df_emotion.columns if col not in cols_exclude]
        emotion_sums = df_emotion[emotion_cols].sum()
        labels = emotion_sums.index.tolist()
        sizes = emotion_sums.values.tolist()
        threshold = 0.01
        total = np.sum(sizes)
        big_labels, big_sizes, small_total = [], [], 0
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
            startangle=90, colors=colors, textprops={'fontsize': 8}
        )
        centre_circle = plt.Circle((0, 0), 0.7, fc='white')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')
        for autotext in autotexts:
            autotext.set_fontsize(7)
        for text in texts:
            text.set_fontsize(8)
        st.pyplot(fig2)
    else:
        st.info("No emotion data found or invalid file.")

    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", sorted(df['sentiment'].unique()))
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['message', 'language', 'translated_message']]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    st.dataframe(filtered[preview_cols])

    st.subheader("Trending Keywords & Topics")
    df_keywords = pd.read_csv(keyword_path)
    keyword_html = ""
    for _, row in df_keywords.iterrows():
        keyword_html += (
            f"<span style='background:#def6e2;font-size:18px;border-radius:20px;padding:8px 20px;display:inline-block;"
            f"margin:8px 12px 4px 0;box-shadow:0 2px 6px #e6ebe9;'>"
            f"<b>{row['keyword']}</b> <span style='color:#44685b;'>{row['Total']}</span></span>"
        )
    st.markdown(
        f"<div style='display:flex;flex-wrap:wrap;'>{keyword_html}</div>", unsafe_allow_html=True
    )

    if selected_sentiment == "Negative":
        if st.button("GenAI Sales Analysis"):
            sales_advice = analyze_negative_comments(filtered)
            st.subheader("GenAI Sales Strategy Suggestions")
            for strategy in sales_advice:
                st.write(f"- {strategy}")

# In your main file, call telegram_dashboard()
