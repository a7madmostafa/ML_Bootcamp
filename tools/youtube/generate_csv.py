"""Generate the videos CSV with descriptions from README files."""

import re
import csv
import os

REPO_URL = "https://github.com/a7madmostafa/ML_Bootcamp"
LINKEDIN = "https://www.linkedin.com/in/ahmadmmostafa/"
HASHTAGS = "#MachineLearning #Python #DataScience #MLBootcamp"

MODULES = [
    ("01-intro_to_ai_and_data_science", "MLB01 — Intro to AI & Data Science"),
    ("02-python_foundations", "MLB02 — Python Foundations"),
    ("03-python_projects", "MLB03 — Python Projects"),
    ("04-python_web_scraping", "MLB04 — Python Web Scraping"),
    ("05-git_and_github", "MLB05 — Git & GitHub"),
    ("06-python_data_analysis", "MLB06 — Python Data Analysis"),
    ("07-streamlit", "MLB07 — Streamlit"),
    ("08-data_preprocessing_and_feature_engineering", "MLB08 — Data Preprocessing and Feature Engineering"),
    ("09-python_machine_learning", "MLB09 — Python Machine Learning"),
]


def parse_readme(module_dir):
    readme_path = os.path.join(module_dir, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    rows = []
    for line in content.split("\n"):
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) < 4:
            continue
        if cols[0] in ("#", "---", ""):
            continue

        num = cols[0].strip()
        title = cols[1].strip()
        duration = cols[2].strip().strip("`")
        link_match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)", cols[3])
        if not link_match:
            continue
        video_id = link_match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        rows.append({
            "num": num,
            "title": title,
            "duration": duration,
            "video_id": video_id,
            "video_url": video_url,
        })

    return rows


def build_description(module_name, module_dir, videos, idx):
    v = videos[idx]
    folder_link = f"{REPO_URL}/tree/main/{module_dir}"

    prev_line = ""
    if idx > 0:
        prev_v = videos[idx - 1]
        prev_line = f"🔄 Previous: {prev_v['title']} — {prev_v['video_url']}"

    next_line = ""
    if idx < len(videos) - 1:
        next_v = videos[idx + 1]
        next_line = f"➡️ Next: {next_v['title']} — {next_v['video_url']}"

    nav_lines = "\n".join(filter(None, [prev_line, next_line]))

    desc = f"""📚 {module_name} — {v['title']}

In this video, we cover {v['title']} as part of the ML Bootcamp.

🔗 Resources:
• Code & Notes: {folder_link}
• Full Course Repo: {REPO_URL}

⏱️ Duration: {v['duration']}

{nav_lines}

👤 Connect with me:
• LinkedIn: {LINKEDIN}

{HASHTAGS}"""

    return desc


def main():
    all_videos = []

    for module_dir, module_name in MODULES:
        videos = parse_readme(module_dir)
        for idx, v in enumerate(videos):
            desc = build_description(module_name, module_dir, videos, idx)
            all_videos.append({
                "video_id": v["video_id"],
                "title": v["title"],
                "description": desc,
            })

    output_path = os.path.join("tools", "youtube", "videos.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["video_id", "title", "description"])
        writer.writeheader()
        writer.writerows(all_videos)

    print(f"Generated {len(all_videos)} video descriptions -> {output_path}")


if __name__ == "__main__":
    main()
