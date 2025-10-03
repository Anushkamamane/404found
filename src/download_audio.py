from yt_dlp import YoutubeDL
import os


def download_audio(url, output_path='data/tata_audio.mp3', cookies_path='cookies.txt'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'cookiefile': cookies_path,  # add this line to use cookies
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Audio downloaded to {output_path}")



# Example usage
if __name__ == "__main__":
    video_url = "https://youtu.be/HZwuTVryqcg"  # Your Tata Motors video
    download_audio(video_url)
