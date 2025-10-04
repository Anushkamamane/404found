import pandas as pd
from textblob import TextBlob
from nrclex import NRCLex

df = pd.read_csv("notebooks/data/comments.csv")
print("Columns in CSV:", df.columns.tolist())  # DEBUG: see available columns

# Find your actual comment text column
COMMENT_COL = None
for col in ["comment", "text", "message", "body"]:
    if col in df.columns:
        COMMENT_COL = col
        break
if COMMENT_COL is None:
    raise Exception("No text/comment column found in CSV. Columns present: " + str(df.columns.tolist()))

KEYWORDS = ["safari", "harrier"]

# Filter for Tata Safari/Harrier comments (also check translated column if present)
mask = df[COMMENT_COL].str.contains('|'.join(KEYWORDS), case=False, na=False)
if "translated_comment" in df.columns:
    mask = mask | df["translated_comment"].str.contains('|'.join(KEYWORDS), case=False, na=False)
filtered = df[mask].copy()

# Sentiment analysis only
def sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.1:
        sentiment_value = "Positive"
    elif polarity < -0.1:
        sentiment_value = "Negative"
    else:
        sentiment_value = "Neutral"
    return sentiment_value

filtered['sentiment'] = filtered[COMMENT_COL].map(sentiment)
filtered.to_csv("comments_sentiment_analysis.csv", index=False)

# NRC emotions full scores into a new DataFrame
emotion_rows = []
emotion_categories = ['fear', 'anger', 'anticipation', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy']
for idx, row in filtered.iterrows():
    text = row[COMMENT_COL]
    nrc = NRCLex(str(text))
    scores = nrc.raw_emotion_scores
    total = sum(scores.values()) if scores else 1
    norm_scores = {emo: scores.get(emo, 0) / total if total > 0 else 0 for emo in emotion_categories}
    out_row = {'index': idx, COMMENT_COL: text}
    out_row.update(norm_scores)
    emotion_rows.append(out_row)

emotions_df = pd.DataFrame(emotion_rows)
emotions_df.to_csv("comments_emotion_analysis.csv", index=False)

print("\nSentiment analysis saved to: comments_sentiment_analysis.csv")
print("Full NRC emotion scores saved to: comments_emotion_analysis.csv")
