import requests
import numpy as np
from config import COMPARE_URL, HEADERS

def compute_compatibility(entity_ids_a, entity_ids_b, top_n_summary=5):
    if not entity_ids_a or not entity_ids_b:
        print("Not Entity")
        return {"score": 0.0, "summary": []}

    params = {
        "a.signal.interests.entities": ",".join(entity_ids_a),
        "b.signal.interests.entities": ",".join(entity_ids_b)
    }

    r = requests.get(COMPARE_URL, headers=HEADERS, params=params)
    if r.status_code != 200:
        print("Status error", r.status_code)
        return {"score": 0.0, "summary": []}

    tags = r.json().get("results", {}).get("tags", [])
    if not tags:
        print("Not tags")
        return {"score": 0.0, "summary": []}

    similarities, weights = [], []
    tag_details = []

    for tag in tags:
        score = tag.get("query", {}).get("score")
        popularity = tag.get("popularity")
        if score is None or popularity is None:
            continue

        similarities.append(score * popularity)
        weights.append(popularity)

        tag_details.append({
            "name": tag["name"],
            "similarity": round(score, 3)
        })

    if not weights or sum(weights) == 0:
        print("Not weights")
        return {"score": 0.0, "summary": []}

    overall_score = float(np.sum(similarities) / np.sum(weights))
    top_tags = sorted(tag_details, key=lambda x: x["similarity"], reverse=True)[:top_n_summary]

    return {
        "score": round(overall_score, 3),
        "summary": [t["name"] for t in top_tags]
    }
