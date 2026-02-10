import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="IT Data Analytics Quiz", page_icon="📊")

# --- DATA: QUESTIONS ---
questions = [
    {"q": "In the Digital Gold Era, what does 'Garbage In, Garbage Out' (GIGO) warn about?", "options": ["A) Storage costs", "B) Poor data leads to unreliable results", "C) Deleted data", "D) Raw data value"], "answer": "B"},
    {"q": "Which step involves extracting logs or gathering sensor readings?", "options": ["A) TELL", "B) THINK", "C) LOOK", "D) ACT"], "answer": "C"},
    {"q": "What is the primary objective during the 'THINK' stage?", "options": ["A) Backing up data", "B) Identifying patterns and anomalies", "C) Designing UI", "D) Connecting sensors"], "answer": "B"},
    {"q": "What is the primary goal of the 'TELL' phase?", "options": ["A) Hide errors", "B) Write code", "C) Translate findings into strategy", "D) Maximize data on screen"], "answer": "C"},
    {"q": "Why is data visualization key to the 'TELL' stage?", "options": ["A) Prevents deletion", "B) Simplifies patterns for decisions", "C) Cleans errors", "D) Stores images"], "answer": "B"},
    {"q": "How does analytics help Cybersecurity professionals?", "options": ["A) Website layouts", "B) Detecting intrusions via anomalies", "C) Manufacturing", "D) Replacing passwords"], "answer": "B"},
    {"q": "In IT, why is data compared to 'Gold'?", "options": ["A) It is heavy", "B) It must be refined to unlock value", "C) It is running out", "D) Conducts electricity"], "answer": "B"},
    {"q": "Which phase focuses on 'Cleaning' data?", "options": ["A) THINK", "B) TELL", "C) LOOK", "D) REPORT"], "answer": "C"},
    {"q": "How does 'Predictive Maintenance' assist an IT manager?", "options": ["A) Buying new PCs", "B) Using data to fix failures early", "C) Speeding up internet", "D) Replacing humans"], "answer": "B"},
    {"q": "What is a major benefit of data literacy for graduates?", "options": ["A) Typing speed", "B) Strategic roles and higher pay", "C) No more coding", "D) Fixing printers"], "answer": "B"}
]

# --- SESSION STATE ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.submitted = False

# --- UI: HEADER ---
st.title("📊 IT Data Analytics Assessment")

if not st.session_state.quiz_started:
    name = st.text_input("Enter your Full Name:")
    if st.button("Start Quiz"):
        if name:
            st.session_state.name = name
            st.session_state.quiz_started = True
            st.rerun()
        else:
            st.warning("Please enter your name.")
elif st.session_state.quiz_started and not st.session_state.submitted:
    q_idx = st.session_state.current_q
    item = questions[q_idx]
    st.subheader(f"Question {q_idx + 1} of {len(questions)}")
    st.write(item["q"])
    choice = st.radio("Select one:", item["options"], key=f"q{q_idx}")
    if st.button("Next"):
        if choice[0] == item["answer"]:
            st.session_state.score += 1
        if q_idx + 1 < len(questions):
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.submitted = True
            st.rerun()
else:
    st.balloons()
    score, total = st.session_state.score, len(questions)
    st.success(f"### Done, {st.session_state.name}!")
    st.metric("Score", f"{score}/{total}")
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        new_row = pd.DataFrame([{"Student Name": st.session_state.name, "Score": score, "Total": total, "Percentage": f"{(score/total)*100}%", "Time Submitted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}])
        existing_data = conn.read(worksheet="Results")
        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Results", data=updated_data)
        st.info("✅ Result saved to Google Sheets.")
    except Exception as e:
        st.error(f"Error saving data: {e}")