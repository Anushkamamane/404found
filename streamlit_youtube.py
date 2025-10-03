import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

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

    data_path = "notebooks/data/comments_sentiment_analysis.csv"
    df = pd.read_csv(data_path)

    # Optionally show raw data
    if st.checkbox("Show raw data"):
        st.dataframe(df)

    # -- Sentiment distribution
    st.subheader("Sentiment Distribution")
    sent_counts = df['predicted_sentiment'].value_counts()
    st.bar_chart(sent_counts)

    # -- Pie chart
    st.subheader("Sentiment Distribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
    ax.axis('equal')
    st.pyplot(fig)

    # -- Reach (Likes) stats
    st.subheader("Reach (Likes) per Sentiment")
    if 'likes' in df.columns:
        likes_sum = df.groupby('predicted_sentiment')['likes'].sum()
        st.write("Total Likes per Sentiment:")
        st.write(likes_sum)
        likes_avg = df.groupby('predicted_sentiment')['likes'].mean()
        st.write("Average Likes per Comment by Sentiment:")
        st.write(likes_avg)

    # -- Sentiment percent table
    st.write("Sentiment Distribution (%)")
    st.write((sent_counts / sent_counts.sum()) * 100)

    # -- Product-specific sentiment filtering
    st.subheader("Product-Specific Sentiment Analysis")
    product = st.selectbox("Analyze product:", ["All", "Safari", "Harrier"])
    if product != "All":
        mask = df['text'].str.contains(product, case=False, na=False)
        prod_df = df[mask]
        prod_counts = prod_df['predicted_sentiment'].value_counts()
        st.write(f"Sentiment counts for {product}:")
        st.bar_chart(prod_counts)
        st.write(f"Total {product} comments: {len(prod_df)}")
        # Show sample positive/negative comments
        st.write(f"Sample Positive Comments ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Positive"]['text'].head())
        st.write(f"Sample Negative Comments ({product}):")
        st.write(prod_df[prod_df['predicted_sentiment'] == "Negative"]['text'].head())
        st.write(f"Most Common Words in Positive Comments ({product}):")
        st.write(most_common_words(prod_df[prod_df['predicted_sentiment'] == "Positive"]['text']))

    # -- General comment filter by sentiment
    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", df['predicted_sentiment'].unique())
    filtered = df[df['predicted_sentiment'] == selected_sentiment]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    st.dataframe(filtered[['author', 'text', 'sentiment_score']])
