import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def reddit_dashboard():
    st.title("Tata Motors Reddit Comments Sentiment Analysis")

    data_path = "notebooks/data/reddit_comments_sentiment.csv"
    df = pd.read_csv(data_path)

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

    st.write("Sentiment Distribution (%)")
    st.write((sent_counts / sent_counts.sum()) * 100)

    st.subheader("Filter Comments by Sentiment")
    selected_sentiment = st.selectbox("Select sentiment", df['sentiment'].unique())
    filtered = df[df['sentiment'] == selected_sentiment]
    preview_cols = [col for col in filtered.columns if col in ['comment', 'language', 'translated_comment']]
    st.write(f"Showing {len(filtered)} comments with sentiment: {selected_sentiment}")
    st.dataframe(filtered[preview_cols])
