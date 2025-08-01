import streamlit as st
import json
import csv
import ast
from datetime import datetime
from collections import defaultdict
from api_utils import get_entity_id,update_master_csv
from analysis import analyze_taste_profile
from compatiblity import compute_compatibility , compute_nlp_similarity ,get_gemini_score
from create_compatiblity_log import batch_compatibility_check,row_with_highest_mean
from form_Questions import categories,scenario_questions
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

# --- Scenario-Based Co-Founder Compatibility Questions ---
st.subheader("🤝 Co-Founder Compatibility Scenario Questions")
for idx, (q_text, default_answer) in enumerate(scenario_questions, 1):
    key = f"scenario_q{idx}"
    form_data[key] = st.text_input(f"Q{idx}: {q_text}", value=default_answer, key=key)

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
    filename = f"VM-{first_name.strip()}-{now}"
    filepath="profile/"+filename+".json"
    scenario_answers = [form_data[f"scenario_q{idx}"] for idx in range(1, len(scenario_questions)+1)]

    full_data = {
        "first_name": first_name,
        "email": email,
        "post": post,
        "form_data": form_data,
        "taste_analysis": analysis_results,
        "UUID": full_entity_ids_specific,    # ➕ stores as list
        "NLP": scenario_answers                   # ➕ duplicate for NLP block
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    output_csv_path="logs/logs_"+filename+".csv"
    batch_compatibility_check(full_entity_ids_specific,output_csv_path,scenario_answers)
    update_master_csv(filename, full_entity_ids_specific,scenario_answers)

    match=row_with_highest_mean(output_csv_path)

    # st.session_state.current_profile_path = filename 


    # st.success("✅ Profile submitted!")
    # st.switch_page("pages/1_Results.py")
    matched_profile_path = "profile/" + match["filename"]+".json"
    try:
        with open(matched_profile_path, "r", encoding="utf-8") as f:
            matched_profile = json.load(f)
        
        st.subheader("👥 Most Compatible Co-Founder Details:")
        st.write("**Name:**", matched_profile.get("first_name", "N/A"))
        st.write("**Email:**", matched_profile.get("email", "N/A"))
        st.write("**Role:**", matched_profile.get("post", "N/A"))
        st.write("**Taste Compatibility Score:**", round(match["score"], 3))
        st.write("**NLP-Gemini Combined Mean:**", round(match["mean"], 3))
        st.write("**Gemini Summary:**", match["Gemini_reasoning"])
    except Exception as e:
        st.error(f"⚠ Could not load matched profile JSON: {e}")

