import pandas as pd
import os

def save_to_csv(df, filename="data/comments.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} comments to {filename}")
