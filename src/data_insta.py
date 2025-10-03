import instaloader
import pandas as pd
import time

L = instaloader.Instaloader()

# Login or load session
print("Logging in to Instagram...")
try:
    L.load_session_from_file("busyall3")
    print("Session loaded.")
except FileNotFoundError:
    USERNAME = "busyall3"
    PASSWORD = "your_password"
    L.login(USERNAME, PASSWORD)
    L.save_session_to_file("busyall3")

PROFILE_NAME = "tatasafariofficial"
KEYWORDS = ["harrier", "safari"]
OUTPUT_FILE = "notebooks/data/instagram_comments.csv"

profile = instaloader.Profile.from_username(L.context, PROFILE_NAME)
all_comments = []

for idx, post in enumerate(profile.get_posts()):
    if idx >= 20:
        break
    time.sleep(5)
    caption = (post.caption or "").lower()
    try:
        for comment in post.get_comments():
            text = (comment.text or "").lower()
            if any(k in text for k in KEYWORDS) or any(k in caption for k in KEYWORDS):
                all_comments.append({
                    "post_id": post.shortcode,
                    "caption": caption,
                    "comment": comment.text,
                    "username": comment.owner.username,
                    "timestamp": comment.created_at_utc
                })
    except Exception as e:
        print(f"Error fetching comments for post {post.shortcode}: {e}")
        continue

df = pd.DataFrame(all_comments)
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Saved {len(df)} filtered comments to {OUTPUT_FILE}")
