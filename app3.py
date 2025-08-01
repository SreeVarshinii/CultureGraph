
import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from textblob import TextBlob
from config import AI_API_KEY
# -------------------- CONFIG --------------------

st.set_page_config(page_title="Co-Founder Compatibility Checker", layout="wide")
genai.configure(api_key=AI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")


# -------------------- QUESTIONS --------------------
questions = [
    "How do you typically handle disagreements in a team setting?",
    "What role do you usually take in a group project?",
    "Describe your ideal work environment.",
    "How do you approach deadlines and time management?",
    "How do you handle failure?",
    "What's your approach to taking risks in business?",
    "How do you recharge or take breaks during intense periods?",
    "How do you deal with ambiguity or uncertain situations?",
    "What values are non-negotiable for you in a professional relationship?",
    "If there's a major disagreement with your co-founder, how would you resolve it?",
    "What would you do if your co-founder wanted to pivot in a direction you strongly disagreed with?",
    "How do you usually recharge after a stressful day?",
    "What motivates you the most when building something new?",
    "What's your preferred way of communicating in a team?",
    "What kind of working rhythm suits you best (e.g., early morning, async, deep work)?",
    "How do you respond when your ideas are challenged by your teammate?",
    "If your startup faced financial uncertainty, what would be your instinctive action?",
    "What motivates you to wake up and build every day?",
    "Would you rather build something meaningful to you or something that will definitely scale?",
    "How do you give feedback to your teammates?",
    "How often do you like to check in with your co-founder?",
    "How do you balance personal life and startup work?",
    "How do you respond when you’re overwhelmed or overcommitted?",
    "What does success look like to you?",
    "What kind of impact do you want your work to have on the world?",
    "How do you approach decision-making under pressure?",
    "How do you stay motivated during long, difficult projects?"
]

# -------------------- SAMPLE ANSWERS FOR TESTING --------------------
default_answers_a = [
    "I usually try to listen to everyone and then find a fair solution.",
    "I often end up organizing and making sure everyone’s on track.",
    "Quiet, focused, with minimal interruptions.",
    "I create a schedule and follow it strictly.",
    "I reflect on what went wrong and try to learn from it.",
    "I assess everything logically before taking a step.",
    "I take short walks and listen to music.",
    "I analyze the situation and reduce ambiguity with planning.",
    "Honesty, accountability, and mutual respect.",
    "I’d initiate a calm discussion and try to align perspectives.",
    "I'd want to understand their reasoning first.",
    "I usually go for a walk or listen to music.",
    "Solving real problems and helping people.",
    "Short async check-ins with room for autonomy.",
    "Deep work in the morning.",
    "I welcome pushback if it's logical.",
    "Cut non-essentials and double down on core.",
    "Knowing I’m building something that matters.",
    "I'd go for meaningful even if it's slower.",
    "Start with empathy and clarity.",
    "Once a week syncs, plus async notes.",
    "Hard stop at 7 PM — recharge is important.",
    "I step away briefly and then prioritize.",
    "Success is doing work I’m proud of, sustainably.",
    "I want to enable better lives through technology.",
    "I slow down and weigh every option carefully.",
    "I revisit the purpose and impact of what I’m building."
]

default_answers_b = [
    "I confront issues head-on and try to resolve them immediately.",
    "I like brainstorming and coming up with creative ideas.",
    "Energetic and collaborative, where people bounce ideas off each other.",
    "I prefer to work in sprints when inspiration hits.",
    "I move on quickly — failure doesn’t bother me much.",
    "I go with my gut and trust my instincts.",
    "I prefer a full disconnect — no phone, no work.",
    "I enjoy the uncertainty — it fuels my creativity.",
    "Trust, ambition, and freedom.",
    "I’d give it time, then revisit the issue once emotions settle.",
    "I'd push back but eventually support them if needed.",
    "Gaming or watching a documentary.",
    "Seeing users actually use what we build.",
    "I prefer live brainstorming and Slack throughout the day.",
    "Evening hustle after a slow start.",
    "I try to defend my idea but remain respectful.",
    "Cut burn rate and go full sales mode.",
    "Chasing a big vision that excites me.",
    "Scalable wins — the world needs solutions that work.",
    "Honest and straight to the point.",
    "Daily check-ins — I like being in sync.",
    "Work comes first if there’s a crunch.",
    "I just power through it.",
    "Growth and recognition at scale.",
    "I want to shift global conversations through my work.",
    "I rely on intuition and past experience to act quickly.",
    "I visualize the reward and end result to push through."
]

# -------------------- NLP SIMILARITY --------------------


# # -------------------- SENTIMENT SIMILARITY --------------------
# def compute_sentiment_alignment(a_answers, b_answers):
#     sentiments_a = [TextBlob(ans).sentiment.polarity for ans in a_answers]
#     sentiments_b = [TextBlob(ans).sentiment.polarity for ans in b_answers]
#     alignment_scores = [1 - abs(a - b) for a, b in zip(sentiments_a, sentiments_b)]
#     return round(np.mean(alignment_scores), 3)

# -------------------- GEMINI --------------------


# -------------------- UI --------------------
st.title("🤝 Co-Founder Compatibility Checker (NLP + Gemini + Sentiment)")

st.markdown("*Goal:* Compare two people’s answers to 27 scenario-based questions and compute compatibility using NLP, LLM, and sentiment.")

with st.expander("🔍 View All Questions"):
    for i, q in enumerate(questions, 1):
        st.markdown(f"*Q{i}*: {q}")

st.subheader("🧑 Person A")
answers_a = [st.text_input(f"A{i+1}. {q}", value=default_answers_a[i]) for i, q in enumerate(questions)]

st.subheader("🧑 Person B")
answers_b = [st.text_input(f"B{i+1}. {q}", value=default_answers_b[i]) for i, q in enumerate(questions)]

if st.button("🔎 Check Compatibility"):
    st.markdown("## 🧠 NLP Similarity Score")
    nlp_score = compute_nlp_similarity(answers_a, answers_b)
    st.write("*Score:*", nlp_score)

    # st.markdown("## ❤ Sentiment Alignment Score")
    # senti_score = compute_sentiment_alignment(answers_a, answers_b)
    # st.write("*Score:*", senti_score)

    st.markdown("## 🤖 Gemini LLM Evaluation")
    llm_result = get_gemini_score(answers_a, answers_b)
    st.write("*Score:*", llm_result.get("score", 0.0))
    st.write("*Reasoning:*", llm_result.get("reasoning","N/A"))