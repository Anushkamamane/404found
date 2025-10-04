import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from src.genai_sales_analysis import analyze_negative_comments

# Language dictionary
TEXTS = {
    "en": {
        "title": "Tata Motors Reddit Comments Sentiment Analysis",
        "show_raw": "Show raw data",
        "sentiment_dist": "Sentiment Distribution",
        "sentiment_pie": "Sentiment Distribution Pie Chart",
        "emotion_dist": "Emotion Distribution (Donut Chart)",
        "no_emotion": "No emotion data found in emotion CSV.",
        "sentiment_percent": "Sentiment Distribution (%)",
        "filter_comments": "Filter Comments by Sentiment",
        "select_sentiment": "Select sentiment",
        "showing_comments": "Showing {count} comments with sentiment: {sentiment}",
        "genai_analysis": "GenAI Sales Analysis",
        "genai_subtitle": "GenAI Sales Strategy Suggestions",
        "analyzing": "Analyzing with GPT-4, please wait..."
    },
    "hi": {
        "title": "टाटा मोटर्स रेडिट टिप्पणियों की भावना विश्लेषण",
        "show_raw": "कच्चा डेटा दिखाएँ",
        "sentiment_dist": "भावना वितरण",
        "sentiment_pie": "भावना वितरण पाई चार्ट",
        "emotion_dist": "भावना वितरण (डोनट चार्ट)",
        "no_emotion": "भावना डेटा CSV में नहीं मिला।",
        "sentiment_percent": "भावना वितरण (%)",
        "filter_comments": "भावना के अनुसार टिप्पणियाँ फ़िल्टर करें",
        "select_sentiment": "भावना चुनें",
        "showing_comments": "{count} टिप्पणियाँ दिखा रहा है जिनकी भावना है: {sentiment}",
        "genai_analysis": "GenAI बिक्री विश्लेषण",
        "genai_subtitle": "GenAI बिक्री रणनीति सुझाव",
        "analyzing": "GPT-4 से विश्लेषण किया जा रहा है, कृपया प्रतीक्षा करें..."
    }
}

def reddit_dashboard(lang="en"):
    texts = TEXTS.get(lang, TEXTS["en"])

    st.title(texts["title"])

    sentiment_path = "notebooks/data/reddit_comments_sentiment.csv"
    emotion_path = "notebooks/data/reddit_comments_sentiment_emotion.csv"
    df = pd.read_csv(sentiment_path)
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

    if st.checkbox(texts["show_raw"]):
        st.write(df)

    st.subheader(texts["sentiment_dist"])
    sent_counts = df['sentiment'].value_counts()
    st.bar_chart(sent_counts)

    st.subheader(texts["sentiment_pie"])
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader(texts["emotion_dist"])
    if df_emotion is not None and 'emotion' in df_emotion.columns:
        emotion_counts = df_emotion['emotion'].value_counts()
        labels = emotion_counts.index.tolist()
        sizes = emotion_counts.values.tolist()
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
        wedges, texts_, autotexts = ax2.pie(
            big_sizes, labels=big_labels, autopct='%1.1f%%', pctdistance=0.85,
            startangle=90, colors=colors, textprops={'fontsize': 8}
        )
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')
        for autotext in autotexts:
            autotext.set_fontsize(5)
        for text in texts_:
            text.set_fontsize(4)
        st.pyplot(fig2)
    else:
        st.info(texts["no_emotion"])

    st.write(texts["sentiment_percent"])
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader(texts["filter_comments"])
    selected_sentiment = st.selectbox(texts["select_sentiment"], sorted(df['sentiment'].unique()))
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['comment', 'language', 'translated_comment']]
    st.write(texts["showing_comments"].format(count=len(filtered), sentiment=selected_sentiment))
    st.dataframe(filtered[preview_cols])

    if selected_sentiment == "Negative":
        if st.button(texts["genai_analysis"]):
            with st.spinner(texts["analyzing"]):
                sales_advice = analyze_negative_comments(filtered)
            st.subheader(texts["genai_subtitle"])
            for strategy in sales_advice:
                st.write(f"- {strategy}")
