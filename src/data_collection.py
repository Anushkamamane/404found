from googleapiclient.discovery import build
import pandas as pd

def get_comments(video_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            "author": comment['authorDisplayName'],
            "text": comment['textDisplay'],
            "likes": comment['likeCount'],
            "date": comment['publishedAt']
        })
    return pd.DataFrame(comments)
