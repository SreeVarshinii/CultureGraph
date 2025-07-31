import streamlit as st
from api_utils import get_entity_id
from compatiblity import compute_compatibility
from ui_components import plot_radar_chart

st.set_page_config(page_title="Co-Founder Compatibility Checker", layout="wide")

st.title("Co-Founder Compatibility Checker")
st.write("Discover how culturally compatible two potential co-founders are based on music, film, brands, travel, books, podcasts, and more.")

if st.button("Clear Cache", key="clear"):
    st.cache_data.clear()
    st.success("✅ Cache cleared. Please re-run your compatibility check.")

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
    ]
}

col1, col2 = st.columns(2)

for col, person in zip([col1, col2], ["A", "B"]):
    with col:
        st.header(f"Co-Founder {person}")
        for section, questions in categories.items():
            st.subheader(section)
            for qtext, key, *extras in questions:
                widget_key = f"{key}_{person}"
                if extras and extras[0] == "multi":
                    st.multiselect(qtext, extras[1], default=extras[1], key=widget_key)
                elif extras and extras[0] == "radio":
                    st.radio(qtext, extras[1], index=0, key=widget_key)
                elif extras and extras[0] == "text":
                    st.text_input(qtext, value=extras[1], key=widget_key)

if st.button("Check Compatibility"):
    def collect_entities(person):
        inputs = [v for k, v in st.session_state.items() if k.endswith(f"_{person}") and isinstance(v, str) and v.strip()]
        lists = [v for k, v in st.session_state.items() if k.endswith(f"_{person}") and isinstance(v, list) and v]
        all_terms = inputs + [item for sublist in lists for item in sublist]
        return [get_entity_id(name.strip()) for name in all_terms if get_entity_id(name.strip())]

    entity_ids_a = collect_entities("A")
    entity_ids_b = collect_entities("B")

    result = compute_compatibility(entity_ids_a, entity_ids_b)
    print(entity_ids_a, entity_ids_b)
    st.session_state.compatibility_result = result
    st.session_state.show_result = True

    # Redirect to results page (hack using st.switch_page)
    st.switch_page("pages/1_Results.py")
    # st.subheader(f"Overall Compatibility Score: {result['score']*100:.2f} %")
    # st.write("Top Shared Interests:", ", ".join(result["summary"]) if result["summary"] else "No significant shared interests found.")

    # st.subheader("Category Breakdown")
    # plot_radar_chart(result["category_scores"])
