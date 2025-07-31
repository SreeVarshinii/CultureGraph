import streamlit as st
from ui_components import plot_radar_chart

st.set_page_config(page_title="Compatibility Results", layout="wide")

st.title("🎯 Compatibility Results")

if "compatibility_result" not in st.session_state:
    st.warning("⚠️ Please complete the compatibility form first.")
    st.stop()

result = st.session_state.compatibility_result

st.subheader(f"Overall Compatibility Score: {result['score'] * 100:.2f} %")
if result["summary"]:
    st.write("Top Shared Interests:", ", ".join(result["summary"]))
else:
    st.write("No significant shared interests found.")

st.subheader("Category Breakdown")
plot_radar_chart(result["category_scores"])
