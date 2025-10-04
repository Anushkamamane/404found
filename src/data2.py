import praw
import pandas as pd
import os

# --- CONFIGURATION ---
CLIENT_ID = "tfWEwTSTTSr0WbBpfjEBgw"
CLIENT_SECRET = "q0c7NUTsgR4zQ_RM8TwZln9kNU1DOw"
USER_AGENT = "TataHarrierSentimentBot"
SUBREDDITS = ["Tata_Safari" ,"TataMotors", "cars", "IndiaCars","CarReviewsIndia","SUVIndia","IndianRoadTrips", "CarsIndia", "CarTalk", "AutoIndia", "Tata_Harrier"]
KEYWORDS = ["harrier", "safari"]
OUTPUT_CSV = "data/reddit_comments.csv"

# --- Initialize PRAW ---
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    check_for_async=False
)

all_results = []

def keyword_in_text(text):
    text_lower = text.lower()
    return any(word in text_lower for word in KEYWORDS)

for sub in SUBREDDITS:
    try:
        subreddit = reddit.subreddit(sub)
        # Try both new and hot to catch as many posts as possible
        for post in subreddit.new(limit=100):
            found_in_post = keyword_in_text(post.title) or keyword_in_text(post.selftext)
            if found_in_post:
                all_results.append({
                    "type": "post",
                    "subreddit": sub,
                    "post_id": post.id,
                    "post_title": post.title,
                    "content": post.selftext,
                    "comment": "",
                    "url": post.url
                })
            # Scan all comments in the post
            post.comments.replace_more(limit=0)
            for comment in post.comments.list():
                if keyword_in_text(comment.body):
                    all_results.append({
                        "type": "comment",
                        "subreddit": sub,
                        "post_id": post.id,
                        "post_title": post.title,
                        "content": post.selftext,
                        "comment": comment.body,
                        "url": post.url
                    })
        print(f"Scanned subreddit: {sub}. Matches so far: {len(all_results)}")
    except Exception as e:
        print(f"Skipped subreddit {sub} due to error: {e}")

if not all_results:
    print("No posts or comments found with keywords! Try increasing limits/subreddits.")
else:
    # Save as DataFrame
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df = pd.DataFrame(all_results)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} matched posts/comments to {OUTPUT_CSV}")
