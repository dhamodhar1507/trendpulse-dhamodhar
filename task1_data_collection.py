import os
import json
import time
from datetime import datetime

import requests


# Base URLs for Hacker News API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required request header
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive)
CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm",
        "startup", "app", "apps", "openai", "google", "microsoft", "apple", "meta",
        "programming", "developer", "developers", "github", "linux", "server", "chip", "chips"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election", "climate", "attack", "global",
        "trump", "biden", "china", "russia", "ukraine", "israel", "india", "minister",
        "military", "policy", "court", "nation", "politics", "border"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship",
        "football", "soccer", "cricket", "tennis", "baseball", "match", "coach", "season", "cup"
    ],
    "science": [
        "research", "study", "space", "physics", "biology", "discovery", "nasa", "genome",
        "quantum", "medical", "medicine", "health", "brain", "cancer", "planet",
        "telescope", "scientist", "chemistry", "experiment"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming",
        "tv", "series", "youtube", "disney", "anime", "comic", "actor", "actress", "album", "song"
    ],
}

MAX_IDS_TO_CHECK = 500
MAX_STORIES_PER_CATEGORY = 25


def fetch_top_story_ids():
    """
    Fetch the top story IDs from Hacker News.
    Returns the first 500 IDs, or an empty list if request fails.
    """
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        return story_ids[:MAX_IDS_TO_CHECK]
    except requests.RequestException as error:
        print(f"Failed to fetch top story IDs: {error}")
        return []


def fetch_story_details(story_id):
    """
    Fetch details for a single Hacker News story by ID.
    Returns the story JSON dict, or None if request fails.
    """
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def assign_category(title):
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return "technology"


def collect_stories():
    """
    Collect up to 25 stories per category from the first 500 top stories.
    Wait 2 seconds between each category loop.
    """
    top_story_ids = fetch_top_story_ids()

    if not top_story_ids:
        return []

    collected_stories = []
    category_counts = {category: 0 for category in CATEGORY_KEYWORDS}
    collected_ids = set()

    # First pass: collect matched stories category by category
    for category in CATEGORY_KEYWORDS:
        print(f"Collecting stories for category: {category}")

        for story_id in top_story_ids:
            if category_counts[category] >= MAX_STORIES_PER_CATEGORY:
                break

            if story_id in collected_ids:
                continue

            story = fetch_story_details(story_id)
            if not story:
                continue

            title = story.get("title", "")
            matched_category = assign_category(title)

            if matched_category != category:
                continue

            story_data = {
                "post_id": story.get("id"),
                "title": title,
                "category": matched_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            collected_stories.append(story_data)
            collected_ids.add(story.get("id"))
            category_counts[category] += 1

        time.sleep(2)

    # Second pass: fill remaining slots with fallback technology stories
    for story_id in top_story_ids:
        if len(collected_stories) >= 100:
            break

        if story_id in collected_ids:
            continue

        story = fetch_story_details(story_id)
        if not story:
            continue

        title = story.get("title", "")

        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": "technology",
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", ""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        collected_stories.append(story_data)
        collected_ids.add(story.get("id"))

    return collected_stories


def save_to_json(stories):
    """
    Save collected stories into data/trends_YYYYMMDD.json
    """
    os.makedirs("data", exist_ok=True)

    file_name = f"trends_{datetime.now().strftime('%Y%m%d')}.json"
    file_path = os.path.join("data", file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(stories, json_file, indent=4, ensure_ascii=False)
        print(f"Collected {len(stories)} stories. Saved to {file_path}")
    except OSError as error:
        print(f"Failed to save JSON file: {error}")


def main():
    """
    Main function to collect stories and save them.
    """
    stories = collect_stories()
    save_to_json(stories)


if __name__ == "__main__":
    main()