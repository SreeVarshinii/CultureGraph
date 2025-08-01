import streamlit as st
import json
import csv
import ast
from datetime import datetime
from collections import defaultdict
from api_utils import get_entity_id,update_master_csv
from analysis import analyze_taste_profile
from compatiblity import compute_compatibility
from create_compatiblity_log import batch_compatibility_check
# --- Streamlit App Setup ---
st.set_page_config(page_title="Co-Founder Compatibility Checker", layout="wide")
st.title("Co-Founder Compatibility Checker")
st.write("Discover how culturally compatible two potential co-founders are based on music, film, brands, travel, books, podcasts, and more.")

if st.button("Clear Cache", key="clear"):
    st.cache_data.clear()
    st.success("✅ Cache cleared. Please re-run your compatibility check.")

# --- Personal Information ---
st.header("Personal Details")
first_name = st.text_input("First Name", key="first_name")
last_name = st.text_input("Last Name", key="last_name")
location = st.text_input("Location", key="location")
email = st.text_input("Email Address", key="email")
post = st.text_input("Role", key="post")

# --- Cultural Categories ---
categories = {
    "🎵 Music Identity": [
        ("Favorite Artists", "music_artists", "text", "Taylor Swift"),
        ("Regularly Listened Bands", "music_bands", "text", "Imagine Dragons"),
        ("Genres that Define You", "music_genres", "multi3", ["Pop", "Rock", "Hip-Hop", "Jazz", "Classical"]),
        ("Artist You'd Travel to See", "music_travel", "text", "Coldplay"),
        ("Artist Reflecting Your Energy", "music_energy", "text", "Adele")
    ],
    "📚 Intellectual Taste": [
        ("Favorite Books or Authors", "books_authors", "text", "George Orwell"),
        ("Most Read Genre", "book_genres", "multi3", ["Fiction", "Non-Fiction", "Science Fiction", "Biography", "Mystery"]),
        ("Book that Influenced You", "book_influence", "text", "1984"),
        ("Books You Dislike", "book_dislike", "text", "Romance Novels"),
        ("Book to Gift a Co-Founder", "book_gift", "text", "The Lean Startup")
    ],
    "🛍 Lifestyle & Aesthetic": [
        ("Brands You Use Daily", "brands_daily", "text", "Apple, Nike, Google"),
        ("Value-Aligned Fashion/Tech Brands", "brands_values", "text", "Patagonia, Tesla"),
        ("Brands You Trust Most", "brands_trust", "text", "Amazon, Sony, IKEA"),
        ("Inspirational Brands for Builders", "brands_builder", "text", "Tesla"),
        ("Preferred Product Aesthetic", "product_aesthetic", "radio", ["Sleek", "Minimalist", "Colorful", "Raw"])
    ],
    "✈ Travel Preferences": [
        ("Top 3 Dream Destinations", "travel_dreams", "text", "Japan, Iceland, Italy"),
        ("Peaceful/Creative Place", "travel_peace", "text", "Bali"),
        ("Places You Travel to Most", "travel_type", "radio", ["Mountains", "Cities", "Islands", "Villages"]),
        ("Remote Work Destination", "travel_remote", "text", "Portugal"),
        ("Most Admired Culture", "travel_culture", "text", "Japanese")
    ],
    "🎬 Film Personality": [
        ("Films That Shaped You", "film_influence", "text", "Inception"),
        ("Genres You Rewatch", "film_genres", "multi", ["Drama", "Comedy", "Sci-Fi", "Action", "Fantasy"]),
        ("Director You Admire", "film_director", "text", "Christopher Nolan"),
        ("Movie Reflecting Your Philosophy", "film_philosophy", "text", "The Pursuit of Happyness"),
        ("Film Universe You'd Live In", "film_universe", "text", "Marvel Universe")
    ],
    "👥 Inspiration & Role Models": [
        ("Most Inspiring Professional", "role_inspire", "text", "Steve Jobs"),
        ("Followed Public Figures", "role_public", "text", "Elon Musk, Oprah Winfrey, Barack Obama"),
        ("Dream Podcast Guest or Mentor", "role_mentor", "text", "Naval Ravikant"),
        ("Favorite Modern Thinker", "role_thinker", "text", "Yuval Noah Harari"),
        ("Relatable Celebrity Lifestyle", "role_celebrity", "text", "Emma Watson")
    ],
    "🗺 Emotional Geography": [
        ("Where You Grew Up", "geo_upbringing", "text", "Chennai, India"),
        ("Cities That Feel Like Home", "geo_home", "text", "New York, San Francisco, Mumbai"),
        ("City You'd Live in Long-term", "geo_future", "text", "Amsterdam"),
        ("Region Matching Your Lifestyle", "geo_region", "text", "Scandinavia"),
        ("Place You Feel Most Inspired", "geo_inspired", "text", "Tokyo")
    ],
    "🎙 Listening & Learning": [
        ("Top 5 Podcasts", "podcasts_fav", "text", "The Daily, Lex Fridman, Tim Ferriss"),
        ("Podcast That Changed You", "podcast_change", "text", "Naval Podcast"),
        ("Favorite Podcast Host", "podcast_host", "text", "Tim Ferriss"),
        ("Preferred Format", "podcast_format", "radio", ["Interview", "Solo", "News", "Storytelling"]),
        ("When You Listen", "podcast_time", "radio", ["Morning", "Work", "Evening", "Commute"])
    ],
    "📺 Media Affinity": [
        ("Shows You Rewatch", "tv_rewatch", "text", "Friends, The Office"),
        ("Comfort Show", "tv_comfort", "text", "Brooklyn Nine-Nine"),
        ("Favorite Character Show", "tv_character", "text", "Ted Lasso"),
        ("Genre You Binge Most", "tv_genres", "multi", ["Comedy", "Thriller", "Drama", "Fantasy", "Reality"]),
        ("Must-Watch Show", "tv_mustwatch", "text", "Black Mirror")
    ],
    "🎮 Play Style & Strategy": [
        ("Games You Play Most", "game_most", "text", "Minecraft, FIFA"),
        ("Solo/Co-op/Competitive?", "game_mode", "radio", ["Solo", "Co-op", "Competitive"]),
        ("Favorite Game Universe", "game_universe", "text", "The Witcher"),
        ("Game Reflecting Decision Style", "game_decision", "text", "Civilization VI"),
        ("Game Genre That Defines You", "game_genre", "multi", ["RPG", "Shooter", "Strategy", "Simulation", "Adventure"])
    ]}

# --- Collect Form Inputs ---
form_data = {}
for section, questions in categories.items():
    st.subheader(section)
    for qtext, key, *extras in questions:
        widget_key = f"{key}_A"
        if extras and extras[0] == "multi":
            form_data[key] = st.multiselect(qtext, extras[1], default=extras[1], key=widget_key)
        elif extras and extras[0] == "radio":
            form_data[key] = st.radio(qtext, extras[1], index=0, key=widget_key)
        elif extras and extras[0] == "text":
            form_data[key] = st.text_input(qtext, value=extras[1], key=widget_key)

# --- Submission Logic ---
if st.button("Submit"):
    grouped_inputs = defaultdict(list)
    for key, value in form_data.items():
        category = key.split("_")[0]
        grouped_inputs[category].extend(value if isinstance(value, list) else [value])

    analysis_results = {}
    full_entity_ids=[]
    full_entity_ids_specific=[]
    for category, terms in grouped_inputs.items():
        cleaned_terms = [t.strip() for t in terms if t.strip()]
        entity_ids = [get_entity_id(term) for term in cleaned_terms if get_entity_id(term)]
        full_entity_ids_specific.extend(entity_ids)
        if entity_ids:
            genre_result = analyze_taste_profile(entity_ids)
            analysis_results[category] = genre_result
            for genre in genre_result:
                genre_entity_id = get_entity_id(genre)
                if genre_entity_id:
                    full_entity_ids.append(genre_entity_id)
    st.session_state.analysis_results = analysis_results
    st.session_state.show_result = True

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"VM-{first_name.strip()}-{now}.json"
    filepath="profile/"+filename
    full_data = {
        "first_name": first_name,
        "email": email,
        "post": post,
        "form_data": form_data,
        "taste_analysis": analysis_results,
        "UUID": full_entity_ids_specific
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    output_csv_path="logs/logs_"+filename
    batch_compatibility_check(full_entity_ids_specific,output_csv_path)
    update_master_csv(filename, full_entity_ids_specific)
    # st.session_state.current_profile_path = filename 


    # st.success("✅ Profile submitted!")
    # st.switch_page("pages/1_Results.py")
