import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
import numpy as np
import os
from src.genai_sales_analysis import analyze_negative_comments

TEXTS = {
    "en": {
        "title": "Tata Motors YouTube Comments Sentiment Analysis",
        "show_raw": "Show raw data",
        "sentiment_dist": "Sentiment Distribution",
        "sentiment_pie": "Sentiment Distribution Pie Chart",
        "emotion_dist": "Emotion Distribution (Donut Chart)",
        "no_emotion": "No emotion data found or file missing.",
        "sentiment_percent": "Sentiment Distribution (%)",
        "product_analysis": "Product-Specific Sentiment Analysis",
        "analyze_product": "Analyze product:",
        "sentiment_counts": "Sentiment counts for",
        "total_comments": "Total comments:",
        "sample_positive": "Sample Positive Comments",
        "sample_negative": "Sample Negative Comments",
        "common_words": "Most Common Words in Positive Comments",
        "filter_sentiment": "Filter Comments by Sentiment",
        "select_sentiment": "Select sentiment",
        "showing_comments": "Showing {count} comments with sentiment: {sentiment}",
        "genai_analysis": "GenAI Sales Analysis",
        "genai_spinner": "Analyzing with GPT-4, please wait...",
        "genai_subheader": "GenAI Sales Strategy Suggestions"
    },
    "hi": {
        "title": "टाटा मोटर्स यूट्यूब टिप्पणियों भावना विश्लेषण",
        "show_raw": "कच्चा डेटा दिखाएँ",
        "sentiment_dist": "भावना वितरण",
        "sentiment_pie": "भावना वितरण पाई चार्ट",
        "emotion_dist": "भावना वितरण (डोनट चार्ट)",
        "no_emotion": "भावना डेटा नहीं मिला या फ़ाइल गायब है।",
        "sentiment_percent": "भावना वितरण (%)",
        "product_analysis": "उत्पाद-विशिष्ट भावना विश्लेषण",
        "analyze_product": "उत्पाद का विश्लेषण करें:",
        "sentiment_counts": "भावना गणना",
        "total_comments": "कुल टिप्पणियाँ:",
        "sample_positive": "सकारात्मक टिप्पणियों के उदाहरण",
        "sample_negative": "नकारात्मक टिप्पणियों के उदाहरण",
        "common_words": "सकारात्मक टिप्पणियों में सबसे सामान्य शब्द",
        "filter_sentiment": "भावना द्वारा टिप्पणियाँ फ़िल्टर करें",
        "select_sentiment": "भावना चुनें",
        "showing_comments": "{sentiment} भावना की {count} टिप्पणियाँ दिखा रहा है",
        "genai_analysis": "GenAI बिक्री विश्लेषण",
        "genai_spinner": "GPT-4 से विश्लेषण हो रहा है, कृपया प्रतीक्षा करें...",
        "genai_subheader": "GenAI बिक्री रणनीति सुझाव"
    }
}

def most_common_words(comments, top_n=10):
    all_words = []
    stopwords = set([
        'the','and','a','an','in','is','it','of','for','to','i','so','very',
        'with','this','that','on','its','but','at','as','are','be','my','you'
    ])
    for c in comments:
        words = re.findall(r'\b\w+\b', str(c).lower())
        filtered = [w for w in words if w not in stopwords]
        all_words.extend(filtered)
    return Counter(all_words).most_common(top_n)

def youtube_dashboard(lang="en"):
    texts = TEXTS[lang]

    st.title(texts["title"])

    sentiment_path = "notebooks/data/comments_sentiment_analysis.csv"
    df_sentiment = pd.read_csv(sentiment_path)

    emotion_path = "notebooks/data/comments_emotion_analysis.csv"
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

    COMMENT_COL = None
    for col in ["text", "comment", "message"]:
        if col in df_sentiment.columns:
            COMMENT_COL = col
            break
    if COMMENT_COL is None:
        st.error("No valid comment/text column found in sentiment CSV.")
        return

    if st.checkbox(texts["show_raw"]):
        st.dataframe(df_sentiment)

    st.subheader(texts["sentiment_dist"])
    sent_counts = df_sentiment['predicted_sentiment'].value_counts()
    st.bar_chart(sent_counts)

    st.subheader(texts["sentiment_pie"])
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader(texts["emotion_dist"])
    if df_emotion is not None:
        emotion_cols = [col for col in df_emotion.columns if col not in ['index', COMMENT_COL]]
        emotion_sums = df_emotion[emotion_cols].sum()
        labels = emotion_sums.index.tolist()
        sizes = emotion_sums.values.tolist()

        threshold = 0.01
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
            autotext.set_fontsize(7)
        for text in texts_:
            text.set_fontsize(8)
        st.pyplot(fig2)
    else:
        st.info(texts["no_emotion"])

    st.write(texts["sentiment_percent"])
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader(texts["product_analysis"])
    product = st.selectbox(texts["analyze_product"], ["All", "Safari", "Harrier"])

    if product != "All":
        mask = df_sentiment[COMMENT_COL].str.contains(product, case=False, na=False)
        prod_df = df_sentiment[mask]
        prod_counts = prod_df['predicted_sentiment'].value_counts()
        st.write(f"{texts['sentiment_counts']} {product}:")
        st.bar_chart(prod_counts)
        st.write(f"{texts['total_comments']} {len(prod_df)}")

        st.write(f"{texts['sample_positive']} ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Positive"][COMMENT_COL].head())

        st.write(f"{texts['sample_negative']} ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Negative"][COMMENT_COL].head())

        st.write(f"{texts['common_words']} ({product}):")
        st.write(most_common_words(prod_df[prod_df['predicted_sentiment'] == "Positive"][COMMENT_COL]))

    st.subheader(texts["filter_sentiment"])
    selected_sentiment = st.selectbox(texts["select_sentiment"], sorted(df_sentiment['predicted_sentiment'].unique()))
    filtered = df_sentiment[df_sentiment['predicted_sentiment'] == selected_sentiment]
    st.write(texts["showing_comments"].format(count=len(filtered), sentiment=selected_sentiment))
    if 'author' in df_sentiment.columns and 'sentiment_score' in df_sentiment.columns:
        st.dataframe(filtered[['author', COMMENT_COL, 'sentiment_score']])
    else:
        st.dataframe(filtered)

    if selected_sentiment.strip().lower() == "negative":
        if st.button(texts["genai_analysis"]):
            with st.spinner(texts["genai_spinner"]):
                sales_advice = analyze_negative_comments(filtered)
            st.subheader(texts["genai_subheader"])
            for strategy in sales_advice:
                st.write(f"- {strategy}")
