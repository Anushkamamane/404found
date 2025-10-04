import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from src.genai_sales_analysis import analyze_negative_comments

TEXTS = {
    "en": {
        "title": "Tata Motors Telegram Comments Sentiment Analysis",
        "show_raw": "Show raw data",
        "sentiment_dist": "Sentiment Distribution",
        "sentiment_pie": "Sentiment Distribution Pie Chart",
        "sentiment_percent": "Sentiment Distribution (%)",
        "emotion_dist": "Emotion Distribution (Donut Chart)",
        "no_emotion": "No emotion data found or invalid file.",
        "filter_comments": "Filter Comments by Sentiment",
        "select_sentiment": "Select sentiment",
        "showing_comments": "Showing {count} comments with sentiment: {sentiment}",
        "trending_kw": "Trending Keywords & Topics",
        "genai_analysis": "GenAI Sales Analysis",
        "genai_subheader": "GenAI Sales Strategy Suggestions"
    },
    "hi": {
        "title": "टाटा मोटर्स टेलीग्राम टिप्पणियों की भावना विश्लेषण",
        "show_raw": "कच्चा डेटा दिखाएं",
        "sentiment_dist": "भावना वितरण",
        "sentiment_pie": "भावना वितरण पाई चार्ट",
        "sentiment_percent": "भावना वितरण (%)",
        "emotion_dist": "भावना वितरण (डोनट चार्ट)",
        "no_emotion": "भावना डेटा नहीं मिला या फ़ाइल अमान्य है।",
        "filter_comments": "भावना द्वारा टिप्पणियाँ फ़िल्टर करें",
        "select_sentiment": "भावना चुनें",
        "showing_comments": "{sentiment} भावना वाली {count} टिप्पणियाँ दिखा रहा है",
        "trending_kw": "ट्रेंडिंग कीवर्ड और विषय",
        "genai_analysis": "GenAI बिक्री विश्लेषण",
        "genai_subheader": "GenAI बिक्री रणनीति सुझाव"
    }
}

def telegram_dashboard(lang="en"):
    texts = TEXTS.get(lang, TEXTS["en"])

    st.title(texts["title"])

    sentiment_path = "notebooks/data/tatamotors_telegram_sentiment.csv"
    emotion_path = "notebooks/data/tatamotors_telegram_emotion.csv"
    keyword_path = "notebooks/data/telegram_trending_keywords.csv"
    df = pd.read_csv(sentiment_path)
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

    if st.checkbox(texts["show_raw"]):
        st.write(df)

    st.subheader(texts["sentiment_dist"])
    sent_counts = df['sentiment'].value_counts()
    st.bar_chart(sent_counts)

    st.subheader(texts["sentiment_pie"])
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.0f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    st.write(texts["sentiment_percent"])
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader(texts["emotion_dist"])
    if df_emotion is not None:
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
        wedges, texts_, autotexts = ax2.pie(
            big_sizes, labels=big_labels, autopct='%1.1f%%', pctdistance=0.85,
            startangle=90, colors=colors, textprops={'fontsize': 8}
        )
        centre_circle = plt.Circle((0, 0), 0.7, fc='white')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')
        for autotext in autotexts:
            autotext.set_fontsize(7)
        for text in texts_:
            text.set_fontsize(8)
        st.pyplot(fig2)
    else:
        st.info(texts["no_emotion"])

    st.subheader(texts["filter_comments"])
    selected_sentiment = st.selectbox(texts["select_sentiment"], sorted(df['sentiment'].unique()))
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['message', 'language', 'translated_message']]
    st.write(texts["showing_comments"].format(count=len(filtered), sentiment=selected_sentiment))
    st.dataframe(filtered[preview_cols])

    st.subheader(texts["trending_kw"])
    df_keywords = pd.read_csv(keyword_path)
    keyword_html = ""
    for _, row in df_keywords.iterrows():
        keyword_html += (
            f"<span style='background:#def6e2;font-size:18px;border-radius:20px;padding:8px 20px;display:inline-block;"
            f"margin:8px 12px 4px 0;box-shadow:0 2px 6px #e6ebe9;'>"
            f"<b>{row['keyword']}</b> <span style='color:#44685b;'>{row['Total']}</span></span>"
        )
    st.markdown(f"<div style='display:flex;flex-wrap:wrap;'>{keyword_html}</div>", unsafe_allow_html=True)

    if selected_sentiment == "Negative":
        if st.button(texts["genai_analysis"]):
            sales_advice = analyze_negative_comments(filtered)
            st.subheader(texts["genai_subheader"])
            for strategy in sales_advice:
                st.write(f"- {strategy}")
