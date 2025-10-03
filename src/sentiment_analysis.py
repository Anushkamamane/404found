from textblob import TextBlob

def analyze_sentiment(df):
    df['sentiment'] = df['text'].apply(
        lambda x: 'Positive' if TextBlob(x).sentiment.polarity > 0 else 'Negative'
    )
    return df
