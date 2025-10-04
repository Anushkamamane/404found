import pandas as pd
import os
import csv
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob
from nrclex import NRCLex
from collections import Counter

# --- CONFIG ---
INPUT_CSV = "notebooks/data/reddit_comments.csv"
OUTPUT_CSV = "notebooks/data/reddit_comments_sentiment_emotion.csv"

# Robustly load CSV with quoting
try:
    df = pd.read_csv(INPUT_CSV, sep=',', quoting=csv.QUOTE_ALL, engine='python', on_bad_lines="skip")
except Exception as e:
    print("CSV failed to load:", e)
    raise

print(df.head())

if "comment" not in df.columns:
    raise ValueError("CSV must have a 'comment' column")

# Initialize translator
translator = Translator()

# Prepare lists for new columns
languages = []
translated_texts = []
sentiments = []
emotions = []

for txt in df['comment']:
    try:
        lang = detect(txt)
    except:
        lang = "unknown"
    languages.append(lang)

    if lang == "hi":
        try:
            translated = translator.translate(txt, src='hi', dest='en').text
        except:
            translated = txt
    else:
        translated = txt
    translated_texts.append(translated)

    polarity = TextBlob(translated).sentiment.polarity
    if polarity > 0.1:
        sentiments.append("Positive")
    elif polarity < -0.1:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

    # Emotion detection
    emotion_obj = NRCLex(translated)
    if emotion_obj.top_emotions:
        top_emotion = emotion_obj.top_emotions[0][0]
    else:
        top_emotion = "none"
    emotions.append(top_emotion)

# Add new data to dataframe
df['language'] = languages
df['translated_comment'] = translated_texts
df['sentiment'] = sentiments
df['emotion'] = emotions

# Save results
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved sentiment and emotion analysis results for {len(df)} comments to {OUTPUT_CSV}")

# Emotion count and percentage
emotion_counts = Counter(emotions)
total_emotions = sum(emotion_counts.values())
emotion_percentages = {emo: (count / total_emotions) * 100 for emo, count in emotion_counts.items()}

print("Emotion distribution (counts):")
for emo, count in emotion_counts.items():
    print(f"{emo}: {count}")

print("\nEmotion distribution (percentages):")
for emo, pct in emotion_percentages.items():
    print(f"{emo}: {pct:.2f}%")

# Sentiment count
print("\nSentiment distribution:")
print(df['sentiment'].value_counts())
