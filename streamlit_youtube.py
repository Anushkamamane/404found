import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
import numpy as np
import os
from src.genai_sales_analysis import analyze_negative_comments


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


def youtube_dashboard():
    st.title("Tata Motors YouTube Comments Sentiment Analysis")

    # Load sentiment data
    sentiment_path = "notebooks/data/comments_sentiment_analysis.csv"
    df_sentiment = pd.read_csv(sentiment_path)

    # Load emotion data
    emotion_path = "notebooks/data/comments_emotion_analysis.csv"
    df_emotion = pd.read_csv(emotion_path) if os.path.exists(emotion_path) else None

    # Detect the comment column
    COMMENT_COL = None
    for col in ["text", "comment", "message"]:
        if col in df_sentiment.columns:
            COMMENT_COL = col
            break
    if COMMENT_COL is None:
        st.error("No valid comment/text column found in sentiment CSV.")
        return

    if st.checkbox("Show raw data"):
        st.dataframe(df_sentiment)

    # Sentiment distribution bar chart
    st.subheader("Sentiment Distribution")
    sent_counts = df_sentiment['predicted_sentiment'].value_counts()
    st.bar_chart(sent_counts)

    # Sentiment pie chart
    st.subheader("Sentiment Distribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    # Emotion donut chart
    st.subheader("Emotion Distribution (Donut Chart)")
    if df_emotion is not None:
        # Assume emotion columns are all except 'index' and comment text column (if any)
        emotion_cols = [col for col in df_emotion.columns if col not in ['index', COMMENT_COL]]
        emotion_sums = df_emotion[emotion_cols].sum()
        labels = emotion_sums.index.tolist()
        sizes = emotion_sums.values.tolist()

        # Group small slices into "Other"
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
        wedges, texts, autotexts = ax2.pie(
            big_sizes, labels=big_labels, autopct='%1.1f%%', pctdistance=0.85,
            startangle=90, colors=colors, textprops={'fontsize': 8}
        )
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2.gca().add_artist(centre_circle)
        ax2.axis('equal')
        for autotext in autotexts:
            autotext.set_fontsize(7)
        for text in texts:
            text.set_fontsize(8)
        st.pyplot(fig2)
    else:
        st.info("No emotion data found or file missing.")

    st.write("Sentiment Distribution (%)")
    st.write((sent_counts / sent_counts.sum()) * 100)

    # Product-specific sentiment analysis
    st.subheader("Product-Specific Sentiment Analysis")
    product = st.selectbox("Analyze product:", ["All", "Safari", "Harrier"])

    if product != "All":
        mask = df_sentiment[COMMENT_COL].str.contains(product, case=False, na=False)
        prod_df = df_sentiment[mask]
        prod_counts = prod_df['predicted_sentiment'].value_counts()
        st.write(f"Sentiment counts for {product}:")
        st.bar_chart(prod_counts)
        st.write(f"Total {product} comments: {len(prod_df)}")

        st.write(f"Sample Positive Comments ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Positive"][COMMENT_COL].head())

        st.write(f"Sample Negative Comments ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Negative"][COMMENT_COL].head())

        st.write(f"Most Common Words in Positive Comments ({product}):")
        st.write(most_common_words(prod_df[prod_df['predicted_sentiment'] == "Positive"][COMMENT_COL]))

    # Filter by sentiment
    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", sorted(df_sentiment['predicted_sentiment'].unique()))
    filtered = df_sentiment[df_sentiment['predicted_sentiment'] == selected_sentiment]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    if 'author' in df_sentiment.columns and 'sentiment_score' in df_sentiment.columns:
        st.dataframe(filtered[['author', COMMENT_COL, 'sentiment_score']])
    else:
        st.dataframe(filtered)

    # GenAI analysis button for negative sentiment only
    if selected_sentiment.strip().lower() == "negative":
        if st.button("GenAI Sales Analysis"):
            with st.spinner("Analyzing with GPT-4, please wait..."):
                sales_advice = analyze_negative_comments(filtered)
            st.subheader("GenAI Sales Strategy Suggestions")
            for strategy in sales_advice:
                st.write(f"- {strategy}")

# Call youtube_dashboard() in your Streamlit main script
