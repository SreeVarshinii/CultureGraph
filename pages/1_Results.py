import streamlit as st
import os
import json
from compatiblity import compute_compatibility  # Your compatibility function

st.set_page_config(page_title="Compare Profiles", layout="wide")
st.title("👥 Compare Co-Founder Compatibility")

# Ensure submitted profile exists
if "current_profile_path" not in st.session_state:
    st.error("Please submit your profile first.")
    st.stop()

# Load submitted profile
with open(st.session_state.current_profile_path, "r", encoding="utf-8") as f:
    current_profile = json.load(f)

st.subheader(f"Your Profile: {current_profile['first_name']} ({current_profile['email']})")

# Load all available profiles
profile_dir = "profiles"
profile_files = [f for f in os.listdir(profile_dir) if f.endswith(".json")]

# Exclude own profile
other_profiles = [f for f in profile_files if f != os.path.basename(st.session_state.current_profile_path)]

# Selection
selected_files = st.multiselect("Select profiles to compare against:", other_profiles)

# if st.button("Check Compatibility"):
#     results = []
#     for file in selected_files:
#         with open(os.path.join(profile_dir, file), "r", encoding="utf-8") as f:
#             other = json.load(f)

#         # Example compatibility logic — replace with real logic
#         score = compute_compatibility(current_profile, other)

#         results.append({
#             "name": other["first_name"],
#             "email": other["email"],
#             "score": score
#         })

#     # Display results
#     st.subheader("🧠 Compatibility Results")
#     for res in results:
#         st.markdown(f"**{res['name']}** ({res['email']}): Compatibility Score: `{res['score']}`")
