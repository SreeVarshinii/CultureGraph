import requests
from config import SEARCH_URL, HEADERS
import streamlit as st
import csv
import os
import json


@st.cache_data(show_spinner=False)
def get_entity_id(name: str):
    """Fetch Qloo entity_id dynamically for any name (artist, brand, genre)."""
    params = {"query": name, "limit": 1}
    # print(params)
    r = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    if r.status_code != 200 or not r.json().get("results"):
        return None
    return r.json()["results"][0]["entity_id"]

def update_master_csv(filename, entity_ids, csv_path="logs/master_entity_log.csv"):
    """
    Appends the filename and associated entity IDs to a master CSV.
    """
    row = {
        "filename": filename,
        "full_entity_ids":entity_ids
    }

    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["filename", "full_entity_ids"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)
