import pandas as pd
from textblob import TextBlob
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Load your dataset
df = pd.read_csv("notebooks/data/tatamotors_telegram_sentiment.csv")

# Check the columns present
print("Columns in CSV:", df.columns.tolist())

COMMENT_COL = "message"          # Comment text column
TRUE_LABEL_COL = "sentiment"     # True sentiment labels column

# Define the TextBlob-based sentiment prediction function
def predict_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Predict sentiment using TextBlob
df['predicted_sentiment'] = df[COMMENT_COL].map(predict_sentiment)

# Get true and predicted labels
y_true = df[TRUE_LABEL_COL]
y_pred = df['predicted_sentiment']

# Calculate evaluation metrics
accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
