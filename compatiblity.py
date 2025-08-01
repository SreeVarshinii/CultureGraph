import requests
import numpy as np
from config import COMPARE_URL, HEADERS,AI_API_KEY

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from textblob import TextBlob

genai.configure(api_key=AI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")

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


def compute_nlp_similarity(a_answers, b_answers):
    similarities = []
    # print("Type : ",type(a_answers),type(b_answers))
    for a, b in zip(a_answers, b_answers):
        tfidf = TfidfVectorizer().fit_transform([a, b])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        similarities.append(score)
    # print("Similarities after calculation : ",similarities)
    # print(np.mean(similarities))
    return round(np.mean(similarities), 3)


def get_gemini_score(a_answers, b_answers):
    prompt = f"""
You are assessing co-founder compatibility based on scenario-based answers.
Each person has answered the same set of questions.

Person A: {a_answers}
Person B: {b_answers}

Based on their tone, goals, decision-making, and working style, rate their compatibility from 0 to 1 (1 being highly compatible).
Also explain your reasoning in 2-3 sentences.
Return the result in JSON format: {{
    "score": 0.87,
    "reasoning": "They share similar values and conflict resolution strategies..."
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text
        import json, re
        json_str = re.search(r"\{.*\}", text, re.DOTALL)
        if json_str:
            return json.loads(json_str.group())
    except Exception as e:
        return {"score": 0.0, "reasoning": f"Gemini API Error: {str(e)}"}
    return {"score": 0.0, "reasoning": "No valid response from Gemini"}