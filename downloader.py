import subprocess
import json
import random
import os
import concurrent.futures
import re

channels = [
    "https://www.youtube.com/@ibekeigh/shorts",
    "https://www.youtube.com/@TechJoyce/shorts",
    "https://www.youtube.com/@LawByMike/shorts",
    "https://www.youtube.com/@makhirtech/shorts",
    "https://www.youtube.com/@TechBitsCentral/shorts",
    "https://www.youtube.com/@MONEYTALKSWIRELESS/shorts",
    "https://www.youtube.com/@Simotxt/shorts",
    "https://www.youtube.com/@Potemer/shorts",
    "https://www.youtube.com/@PMdamian/shorts",
    "https://www.youtube.com/@SuperMeme99/shorts",
    "https://www.youtube.com/@Sleenty/shorts",
    "https://www.youtube.com/@zhiphyr/shorts",
    "https://www.youtube.com/@NutshellAnimations/shorts",
    "https://www.youtube.com/@coldmangoo/shorts"
]

json_path = "videos/downloaded_urls.json"

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        downloaded_data = json.load(f)
else:
    downloaded_data = []

downloaded_urls = set(entry["url"] for entry in downloaded_data)

if not os.path.exists("yt-dlp.exe"):
    print("❌ yt-dlp.exe not found!")
    exit(1)

def get_random_video_info(channel):
    try:
        result = subprocess.run(
            ["yt-dlp.exe", "--flat-playlist", "--dump-single-json", channel],
            capture_output=True, text=True, check=True
        )
        playlist = json.loads(result.stdout)
        entries = playlist.get("entries", [])
        if not entries:
            return None

        random_entry = random.choice(entries)
        video_id = random_entry["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        meta_result = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "%(title)s|%(channel)s", video_url],
            capture_output=True, text=True, check=True
        )
        title, channel_name = meta_result.stdout.strip().split("|", 1)

        return {
            "url": video_url,
            "title": title,
            "channel": channel_name
        }
    except Exception as e:
        print(f"⚠️ Error getting video from {channel}: {str(e)}")
        return None

def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', "_", text)

def download_video(video_info):
    try:
        # Download video in mp4 format, best quality
        output_template = "%(title)s-%(id)s.%(ext)s"
        completed = subprocess.run(
            ["yt-dlp", "-f", "best[ext=mp4]/best", "-o", output_template, video_info["url"]],
            capture_output=True, text=True, check=True
        )

        # Expected filename based on the same pattern yt-dlp uses
        video_id = video_info["url"].split("=")[-1]
        expected_filename = f"{sanitize(video_info['title'])}-{video_id}.mp4"
        
        # Check if file exists
        if not os.path.exists(expected_filename):
            print(f"⚠️ Warning: Expected file '{expected_filename}' not found, skipping")
            return None  # Return None to skip this file

        print(f"✅ Downloaded: {video_info['title']} by {video_info['channel']}")
        return {
            "url": video_info["url"],
            "title": video_info["title"],
            "channel": video_info["channel"],
            "file": expected_filename
        }
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download {video_info['url']}: {str(e)}")
        return None

def worker():
    attempts = 0
    max_attempts = 30
    
    while attempts < max_attempts:
        channel = random.choice(channels)
        info = get_random_video_info(channel)
        
        if info and info["url"] not in downloaded_urls:
            result = download_video(info)
            
            if result:  # Only save if download was successful and file exists
                # Lock for thread-safe append and write
                downloaded_urls.add(result["url"])
                downloaded_data.append(result)
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(downloaded_data, f, indent=4, ensure_ascii=False)
                return result
                
        attempts += 1
        
    print(f"⚠️ Worker exceeded {max_attempts} attempts without finding a valid video")
    return None

def main():
    max_workers = 10  # 10 videos downloading concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker) for _ in range(max_workers)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    print(f"🎉 Done! {len(downloaded_data)} total videos saved in {json_path}.")

if __name__ == "__main__":
    main()
