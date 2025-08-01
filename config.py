import streamlit as st

API_KEY = st.secrets["API_KEY"]
AI_API_KEY=st.secrets["AI_API_KEY"]
SEARCH_URL = "https://hackathon.api.qloo.com/search"
COMPARE_URL = "https://hackathon.api.qloo.com/v2/insights/compare?filter.type=urn%3Atag"
ANALYSIS_URL="https://hackathon.api.qloo.com/analysis"
HEADERS = {"accept": "application/json", "X-Api-Key": API_KEY}