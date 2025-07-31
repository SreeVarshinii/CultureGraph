import streamlit as st
from api_utils import get_entity_id
from compatiblity import compute_compatibility
from ui_components import plot_radar_chart

st.set_page_config(page_title="Co-Founder Compatibility Checker", layout="wide")

st.title("Co-Founder Compatibility Checker")
st.write("Discover how culturally compatible two potential co-founders are based on music, film, brands, dining, and lifestyle preferences.")

if st.button("Clear Cache", key="clear"):
    st.cache_data.clear()
    st.success("✅ Cache cleared. Please re-run your compatibility check.")

col1, col2 = st.columns(2)

with col1:
    st.header("Person A")
    music_a = st.multiselect("Favorite Music Genres", ["Rock", "Pop", "Indie", "Hip-Hop", "Jazz", "Classical"], key="music_a")
    film_a = st.multiselect("Favorite Movie/TV Genres", ["Action", "Comedy", "Drama", "Documentary", "Sci-Fi & Fantasy"], key="film_a")
    brands_a = st.text_input("Favorite Brands (comma-separated)", "Nike, Patagonia", key="brands_a")
    free_a = st.text_input("Other Favorites (Artists, Movies, Books)", "", key="free_a")

with col2:
    st.header("Person B")
    music_b = st.multiselect("Favorite Music Genres", ["Rock", "Pop", "Indie", "Hip-Hop", "Jazz", "Classical"], key="music_b")
    film_b = st.multiselect("Favorite Movie/TV Genres", ["Action", "Comedy", "Drama", "Documentary", "Sci-Fi & Fantasy"], key="film_b")
    brands_b = st.text_input("Favorite Brands (comma-separated)", "Apple, Gucci", key="brands_b")
    free_b = st.text_input("Other Favorites (Artists, Movies, Books)", "", key="free_b")

if st.button("Check Compatibility", key="check_btn"):
    all_a_raw = list(music_a) + list(film_a) + brands_a.split(",") + free_a.split(",")
    all_b_raw = list(music_b) + list(film_b) + brands_b.split(",") + free_b.split(",")

    entity_ids_a = [get_entity_id(name.strip()) for name in all_a_raw if get_entity_id(name.strip())]
    entity_ids_b = [get_entity_id(name.strip()) for name in all_b_raw if get_entity_id(name.strip())]

    result = compute_compatibility(entity_ids_a, entity_ids_b)

    st.subheader(f"Overall Compatibility Score: {result['score']}")
    st.write("Top Shared Interests:", ", ".join(result["summary"]) if result["summary"] else "No significant shared interests found.")

    st.subheader("Category Breakdown")
    plot_radar_chart(result["category_scores"])
