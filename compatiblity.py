import requests
import numpy as np
from collections import defaultdict
from config import COMPARE_URL, HEADERS

def compute_compatibility(entity_ids_a, entity_ids_b, top_n_summary=5):
    if not entity_ids_a or not entity_ids_b:
        return {"score": 0.0, "summary": [], "category_scores": {}}

    params = {
        "a.signal.interests.entities": ",".join(entity_ids_a),
        "b.signal.interests.entities": ",".join(entity_ids_b)
    }

    r = requests.get(COMPARE_URL, headers=HEADERS, params=params)
    if r.status_code != 200:
        print("Status error",r.status_code)
        return {"score": 0.0, "summary": [], "category_scores": {}}

    tags = r.json().get("results", {}).get("tags", [])
    if not tags:
        return {"score": 0.0, "summary": [], "category_scores": {}}

    similarities, weights = [], []
    tag_details = []
    category_buckets = defaultdict(list)

    def get_category(tag):
        subtype = tag.get("subtype", "").lower()
        if "music" in subtype: return "Music"
        if "film" in subtype or "tv" in subtype: return "Film/TV"
        if "book" in subtype or "literature" in subtype: return "Books"
        if "brand" in subtype or "fashion" in subtype: return "Brands"
        if "cuisine" in subtype or "dining" in subtype: return "Dining"
        if "travel" in subtype or "hotel" in subtype: return "Travel"
        if "lifestyle" in subtype or "theme" in subtype: return "Lifestyle"
        return "Other"

    for tag in tags:
        score = tag.get("query", {}).get("score")
        popularity = tag.get("popularity")
        if score is None or popularity is None:
            continue

        similarity = score
        weight = popularity
        similarities.append(similarity * weight)
        weights.append(weight)

        category = get_category(tag)
        category_buckets[category].append(similarity)

        tag_details.append({
            "name": tag["name"],
            "similarity": round(similarity, 3),
            "category": category
        })

    if not weights or sum(weights) == 0:
        return {"score": 0.0, "summary": [], "category_scores": {}}

    overall_score = float(np.sum(similarities) / np.sum(weights))
    top_tags = sorted(tag_details, key=lambda x: x["similarity"], reverse=True)[:top_n_summary]
    category_scores = {cat: round(np.mean(vals), 3) for cat, vals in category_buckets.items() if vals}

    return {
        "score": round(overall_score, 3),
        "summary": [t["name"] for t in top_tags],
        "category_scores": category_scores
    }
