import requests
import json
from config import ANALYSIS_URL, HEADERS

def analyze_taste_profile(entity_ids):
    print("Analyzing taste profile via GET:", ANALYSIS_URL)

    if not entity_ids:
        return []

    params = {
        "entity_ids": ",".join(entity_ids),
        "page": 1,
        "take": 20
    }

    try:
        response = requests.get(ANALYSIS_URL, headers=HEADERS, params=params)
        # print("Status:", response.status_code)
        response.raise_for_status()
        data = response.json()

        # Optional: Save full JSON to file for debugging
        with open("ans.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Extract top 5 genre tags by _score
        genre_tags = [
            tag for tag in data.get("results", {}).get("tags", [])
            if "genre" in tag.get("subtype", "").lower()
        ]
        top_genres = sorted(genre_tags, key=lambda t: t["query"].get("_score", 0), reverse=True)[:3]
        return [tag["name"] for tag in top_genres]

    except requests.RequestException as e:
        print("GET analysis request failed:", e)
        return []
