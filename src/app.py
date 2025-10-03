import pandas as pd
from collections import Counter
import re

# Load CSV with at least a 'comment' and 'sentiment' (optional: 'translated_comment') column
df = pd.read_csv("notebooks/data/reddit_comments_sentiment.csv")

def most_common_words(comments, top_n=10):
    all_words = []
    stopwords = set([
        'the','and','a','an','in','is','it','of','for','to','i','so','very',
        'with','this','that','on','its','but','at','as','are','be','my','you'
    ])
    for comment in comments:
        words = re.findall(r'\b\w+\b', str(comment).lower())
        filtered_words = [w for w in words if w not in stopwords]
        all_words.extend(filtered_words)
    return Counter(all_words).most_common(top_n)

def sentiment_analysis_over_keyword(df, keyword):
    # Filter for comments mentioning the keyword (in comment or translated_comment)
    contains_keyword = df['comment'].str.contains(keyword, case=False, na=False)
    if 'translated_comment' in df.columns:
        contains_keyword = contains_keyword | df['translated_comment'].str.contains(keyword, case=False, na=False)
    filtered_df = df[contains_keyword]

    pos = filtered_df[filtered_df['sentiment'] == "Positive"]['comment'].tolist()
    neg = filtered_df[filtered_df['sentiment'] == "Negative"]['comment'].tolist()
    neu = filtered_df[filtered_df['sentiment'] == "Neutral"]['comment'].tolist()
    total = len(filtered_df)
    pos_percent = (len(pos) / total) * 100 if total else 0
    neg_percent = (len(neg) / total) * 100 if total else 0
    neu_percent = (len(neu) / total) * 100 if total else 0

    return {
        "comments": filtered_df['comment'].tolist(),
        "positive_comments": pos,
        "negative_comments": neg,
        "neutral_comments": neu,
        "positive_percent": pos_percent,
        "negative_percent": neg_percent,
        "neutral_percent": neu_percent,
        "total": total
    }

# Analyze Safari
safari_sentiment = sentiment_analysis_over_keyword(df, "safari")
print("===== Tata Motors Safari Sentiment Analysis =====")
print(f"Total Comments: {safari_sentiment['total']}")
print(f"Positive: {len(safari_sentiment['positive_comments'])} ({safari_sentiment['positive_percent']:.2f}%)")
print(f"Negative: {len(safari_sentiment['negative_comments'])} ({safari_sentiment['negative_percent']:.2f}%)")
print(f"Neutral : {len(safari_sentiment['neutral_comments'])} ({safari_sentiment['neutral_percent']:.2f}%)\n")
print("Sample Positive Comments (Safari):")
for c in safari_sentiment['positive_comments'][:5]:
    print("-", c)
print("\nSample Negative Comments (Safari):")
for c in safari_sentiment['negative_comments'][:5]:
    print("-", c)
print("\nMost Common Positive Words (Safari):")
print(most_common_words(safari_sentiment['positive_comments']))

# Analyze Harrier
harrier_sentiment = sentiment_analysis_over_keyword(df, "harrier")
print("\n===== Tata Motors Harrier Sentiment Analysis =====")
print(f"Total Comments: {harrier_sentiment['total']}")
print(f"Positive: {len(harrier_sentiment['positive_comments'])} ({harrier_sentiment['positive_percent']:.2f}%)")
print(f"Negative: {len(harrier_sentiment['negative_comments'])} ({harrier_sentiment['negative_percent']:.2f}%)")
print(f"Neutral : {len(harrier_sentiment['neutral_comments'])} ({harrier_sentiment['neutral_percent']:.2f}%)\n")
print("Sample Positive Comments (Harrier):")
for c in harrier_sentiment['positive_comments'][:5]:
    print("-", c)
print("\nSample Negative Comments (Harrier):")
for c in harrier_sentiment['negative_comments'][:5]:
    print("-", c)
print("\nMost Common Positive Words (Harrier):")
print(most_common_words(harrier_sentiment['positive_comments']))
