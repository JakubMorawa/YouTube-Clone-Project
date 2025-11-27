import requests
import json
from datetime import datetime, timezone

API_KEY = "" #Add in your own API ley

# ---------------------------------------------
# 1. EDIT YOUR VIDEO URL LIST HERE
# ---------------------------------------------
video_urls = [
    "https://www.youtube.com/watch?v=FWSM8pDKYkU",
    "https://youtu.be/Np87z67evwE",
    "https://www.youtube.com/watch?v=2BLRLuczykM",
    "https://www.youtube.com/watch?v=0Xjt5Y9ue18",
    "https://www.youtube.com/watch?v=jAMegKEetx4&pp=ugUEEgJlbg%3D%3D",
    "https://www.youtube.com/watch?v=L1GPLcBqljE",
    "https://www.youtube.com/watch?v=i7aQig-wjYA",
    "https://www.youtube.com/watch?v=gG7uCskUOrA",
    "https://www.youtube.com/watch?v=9gCrxNGSleU",
    "https://www.youtube.com/watch?v=kEB11PQ9Eo8",
    "https://www.youtube.com/watch?v=WMr3-ShzB08", 
    "https://www.youtube.com/watch?v=OR-ADhxY2q4&pp=ugUEEgJlbg%3D%3D",
    "https://www.youtube.com/watch?v=LPZh9BOjkQs&pp=ugUHEgVlbi1VUw%3D%3D",
    "https://www.youtube.com/watch?v=IXBC85SGC0Q",
    "https://www.youtube.com/watch?v=7roi1ThVO34",
    "https://www.youtube.com/watch?v=SmYDGnwg4dA&pp=ugUEEgJlbg%3D%3D"
]
# ---------------------------------------------

def extract_video_id(url):
    """Extract clean YouTube video ID from any URL format."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def format_views(views):
    """Convert 412345 → 412K, 21000000 → 21M, etc."""
    views = int(views)
    if views >= 1_000_000_000:
        return f"{views/1_000_000_000:.1f}B"
    if views >= 1_000_000:
        return f"{views/1_000_000:.1f}M"
    if views >= 1_000:
        return f"{views/1_000:.1f}K"
    return str(views)

def time_ago(upload_date):
    """Convert ISO date to '10 days ago', '4 months ago', etc."""
    upload_dt = datetime.fromisoformat(upload_date.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    diff = now - upload_dt

    seconds = diff.total_seconds()
    days = seconds // 86400

    if days < 1:
        hours = seconds // 3600
        return f"{int(hours)} hours ago"
    if days < 7:
        return f"{int(days)} days ago"
    if days < 30:
        return f"{int(days // 7)} weeks ago"
    if days < 365:
        return f"{int(days // 30)} months ago"
    return f"{int(days // 365)} years ago"

def fetch_video_data(video_id):
    """Call YouTube Data API for one video."""
    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet,statistics&id={video_id}&key={API_KEY}"
    )
    response = requests.get(url).json()

    if "items" not in response or len(response["items"]) == 0:
        return None

    item = response["items"][0]

    title = item["snippet"]["title"]
    channel = item["snippet"]["channelTitle"]
    views = format_views(item["statistics"]["viewCount"])
    uploaded = time_ago(item["snippet"]["publishedAt"])

    return {
        "id": video_id,
        "title": title,
        "channel": channel,
        "stats": f"{views} views • {uploaded}"
    }

def main():
    video_ids = [extract_video_id(url) for url in video_urls]
    video_ids = [vid for vid in video_ids if vid is not None]

    results = []

    print("Fetching data...")
    for vid in video_ids:
        info = fetch_video_data(vid)
        if info:
            results.append(info)

    # ----------------------------
    # Save JSON
    # ----------------------------
    with open("youtubeData.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nDone! Files created:")
    print(" - youtubeData.json")

main()

