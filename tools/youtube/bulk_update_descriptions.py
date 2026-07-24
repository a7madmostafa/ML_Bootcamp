"""
Bulk update YouTube video descriptions using YouTube Data API v3.

Setup:
1. Go to https://console.cloud.google.com/
2. Create a project (or select existing)
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop App type)
5. Download credentials.json to this folder
6. pip install -r requirements.txt
7. Run: python bulk_update_descriptions.py

Usage:
  # Preview changes (dry run):
  python bulk_update_descriptions.py --csv videos.csv --dry-run

  # Apply changes:
  python bulk_update_descriptions.py --csv videos.csv

  # Export current descriptions to CSV:
  python bulk_update_descriptions.py --export --channel-id CHANNEL_ID

  # Use find/replace mode (updates all videos matching a pattern):
  python bulk_update_descriptions.py --find "old text" --replace "new text" --channel-id CHANNEL_ID
"""

import argparse
import csv
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
QUOTA_COST_PER_UPDATE = 50
DAILY_QUOTA_LIMIT = 10000


def get_authenticated_service():
    """Authenticate and return a YouTube API service object."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Error: {CREDENTIALS_FILE} not found.")
                print("Download credentials from Google Cloud Console:")
                print("  https://console.cloud.google.com/apis/credentials")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def get_upload_playlist_id(youtube, channel_id):
    """Get the uploads playlist ID for a channel."""
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()

    if not response.get("items"):
        print(f"Error: Channel {channel_id} not found.")
        sys.exit(1)

    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_all_video_ids(youtube, playlist_id):
    """Get all video IDs from a playlist (handles pagination)."""
    video_ids = []
    request = youtube.playlistItems().list(
        part="snippet", playlistId=playlist_id, maxResults=50
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)

    return video_ids


def get_video_details(youtube, video_ids):
    """Get current title and description for a list of video IDs (batch of 50)."""
    results = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        request = youtube.videos().list(
            part="snippet", id=",".join(batch), maxResults=50
        )
        response = request.execute()
        for item in response["items"]:
            results[item["id"]] = {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "categoryId": item["snippet"].get("categoryId", "28"),
                "tags": item["snippet"].get("tags", []),
            }
    return results


def update_video_description(youtube, video_id, title, description, category_id, tags):
    """Update a single video's description."""
    body = {
        "id": video_id,
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
        },
    }
    if tags:
        body["snippet"]["tags"] = tags

    request = youtube.videos().update(part="snippet", body=body)
    return request.execute()


def export_to_csv(youtube, channel_id, output_file):
    """Export all video descriptions to a CSV file."""
    print(f"Fetching videos for channel {channel_id}...")
    playlist_id = get_upload_playlist_id(youtube, channel_id)
    video_ids = get_all_video_ids(youtube, playlist_id)
    print(f"Found {len(video_ids)} videos.")

    print("Fetching video details...")
    details = get_video_details(youtube, video_ids)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["video_id", "title", "description"])
        for vid in video_ids:
            d = details.get(vid, {})
            writer.writerow([vid, d.get("title", ""), d.get("description", "")])

    print(f"Exported {len(video_ids)} videos to {output_file}")


def find_and_replace(youtube, channel_id, find_text, replace_text, dry_run=False):
    """Find and replace text in all video descriptions."""
    playlist_id = get_upload_playlist_id(youtube, channel_id)
    video_ids = get_all_video_ids(youtube, playlist_id)
    details = get_video_details(youtube, video_ids)

    updated = 0
    for vid, d in details.items():
        old_desc = d["description"]
        if find_text in old_desc:
            new_desc = old_desc.replace(find_text, replace_text)
            if dry_run:
                print(f"[DRY RUN] Would update {vid}:")
                print(f"  Old: ...{old_desc[max(0, old_desc.index(find_text)-30):old_desc.index(find_text)+len(find_text)+30]}...")
                print(f"  New: ...{new_desc[max(0, new_desc.index(replace_text)-30):new_desc.index(replace_text)+len(replace_text)+30]}...")
            else:
                try:
                    update_video_description(
                        youtube, vid, d["title"], new_desc, d["categoryId"], d.get("tags")
                    )
                    print(f"Updated {vid}")
                    updated += 1
                    time.sleep(0.5)
                except HttpError as e:
                    print(f"Error updating {vid}: {e}")

    print(f"\n{'Would update' if dry_run else 'Updated'} {updated} videos")


def update_from_csv(youtube, csv_file, dry_run=False):
    """Update video descriptions from a CSV file."""
    videos = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            videos.append(row)

    total = len(videos)
    estimated_cost = total * QUOTA_COST_PER_UPDATE
    print(f"Found {total} videos in CSV")
    print(f"Estimated API quota cost: {estimated_cost} units (daily limit: {DAILY_QUOTA_LIMIT})")

    if estimated_cost > DAILY_QUOTA_LIMIT:
        print(f"\nWarning: This exceeds the daily quota limit of {DAILY_QUOTA_LIMIT} units.")
        print("Only the first ~200 videos will be updated today.")
        proceed = input("Continue? (y/n): ")
        if proceed.lower() != "y":
            return

    updated = 0
    skipped = 0
    errors = 0

    # Fetch current details for all videos in the CSV
    video_ids = [v["video_id"] for v in videos]
    print("Fetching current video details...")
    current_details = get_video_details(youtube, video_ids)

    for v in videos:
        vid = v["video_id"]
        new_desc = v["description"]

        if vid not in current_details:
            print(f"Skipping {vid}: not found")
            skipped += 1
            continue

        d = current_details[vid]
        old_desc = d["description"]

        if old_desc == new_desc:
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY RUN] Would update {vid}")
            print(f"  Title: {d['title']}")
            if len(old_desc) > 100:
                print(f"  Old desc: {old_desc[:100]}...")
            else:
                print(f"  Old desc: {old_desc}")
            if len(new_desc) > 100:
                print(f"  New desc: {new_desc[:100]}...")
            else:
                print(f"  New desc: {new_desc}")
        else:
            try:
                update_video_description(
                    youtube, vid, d["title"], new_desc, d["categoryId"], d.get("tags")
                )
                print(f"Updated {vid}: {d['title']}")
                updated += 1
                time.sleep(0.5)
            except HttpError as e:
                print(f"Error updating {vid}: {e}")
                errors += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")


def main():
    parser = argparse.ArgumentParser(description="Bulk update YouTube video descriptions")
    parser.add_argument("--csv", help="CSV file with video_id and description columns")
    parser.add_argument("--export", action="store_true", help="Export current descriptions to CSV")
    parser.add_argument("--output", default="videos_export.csv", help="Output file for --export (default: videos_export.csv)")
    parser.add_argument("--channel-id", help="YouTube channel ID (required for --export and --find)")
    parser.add_argument("--find", help="Text to find in descriptions (for find/replace mode)")
    parser.add_argument("--replace", help="Text to replace with (for find/replace mode)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")

    args = parser.parse_args()

    if not args.csv and not args.export and not args.find:
        parser.print_help()
        print("\nExamples:")
        print("  python bulk_update_descriptions.py --csv videos.csv --dry-run")
        print("  python bulk_update_descriptions.py --csv videos.csv")
        print("  python bulk_update_descriptions.py --export --channel-id UCxxxxxxx")
        print("  python bulk_update_descriptions.py --find 'old' --replace 'new' --channel-id UCxxxxxxx")
        sys.exit(1)

    youtube = get_authenticated_service()

    if args.export:
        if not args.channel_id:
            print("Error: --channel-id required for --export")
            sys.exit(1)
        export_to_csv(youtube, args.channel_id, args.output)
    elif args.find:
        if not args.channel_id:
            print("Error: --channel-id required for --find")
            sys.exit(1)
        if not args.replace:
            print("Error: --replace required for --find")
            sys.exit(1)
        find_and_replace(youtube, args.channel_id, args.find, args.replace, args.dry_run)
    elif args.csv:
        update_from_csv(youtube, args.csv, args.dry_run)


if __name__ == "__main__":
    main()
