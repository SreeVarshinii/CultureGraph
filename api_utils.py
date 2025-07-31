import requests
from config import SEARCH_URL, HEADERS
import streamlit as st

@st.cache_data(show_spinner=False)
def get_entity_id(name: str):
    """Fetch Qloo entity_id dynamically for any name (artist, brand, genre)."""
    params = {"query": name, "limit": 1}
    print(params)
    r = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    if r.status_code != 200 or not r.json().get("results"):
        return None
    return r.json()["results"][0]["entity_id"]
