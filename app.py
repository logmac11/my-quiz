import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Data Detective:Case Closed", page_icon="📊")

# Your Spreadsheet URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/11tpVhGAqNGGH0XraZg1URZJvWEh8SPmiWfoJOmTw__8/edit?usp=sharing"

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

# --- STEP 1: REGISTRATION ---
if not st.session_state.quiz_started:
    st.subheader("Student Registration")
    name = st.text_input("Full Name:")
    phone = st.text_input("Phone Number:")
    email = st.text_input("Email Address:")
    
    if st.button("Start Quiz"):
        if name and phone and email:
            st.session_state.name = name
            st.session_state.phone = phone
            st.session_state.email = email
            st.session_state.quiz_started = True
            st.rerun()
        else:
            st.warning("Please fill in all details to proceed.")

# --- STEP 2: THE QUIZ ---
elif st.session_state.quiz_started and not st.session_state.submitted:
    q_idx = st.session_state.current_q
    item = questions[q_idx]
    
    # Progress Bar
    progress = (q_idx) / len(questions)
    st.progress(progress)
    
    st.subheader(f"Question {q_idx + 1} of {len(questions)}")
    st.write(item["q"])
    choice = st.radio("Select your answer:", item["options"], key=f"q{q_idx}")
    
    if st.button("Submit Answer"):
        if choice[0] == item["answer"]:
            st.session_state.score += 1
        
        if q_idx + 1 < len(questions):
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.submitted = True
            st.rerun()

# --- STEP 3: SCORES & SUBMISSION ---
else:
    st.balloons()
    score = st.session_state.score
    total = len(questions)
    percentage = (score / total) * 100

    # Display Results to Student
    st.header("✨ Quiz Results")
    col1, col2 = st.columns(2)
    col1.metric("Correct Answers", f"{score} / {total}")
    col2.metric("Final Grade", f"{int(percentage)}%")

    if percentage >= 80:
        st.success("Excellent work! You have a strong grasp of IT Data Analytics.")
    elif percentage >= 50:
        st.warning("Good effort! Review the 'Look • Think • Tell' framework for better results.")
    else:
        st.error("Keep practicing. Focus on how data is refined like gold.")

    # Save to Google Sheets
    with st.spinner("Saving your results to the database..."):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            new_row = pd.DataFrame([{
                "Name": st.session_state.name,
                "Phone": st.session_state.phone,
                "Email": st.session_state.email,
                "Score": score,
                "Total": total,
                "Percentage": f"{percentage}%",
                "Time Submitted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            
            existing_data = conn.read(spreadsheet=spreadsheet_url, worksheet="Results")
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(spreadsheet=spreadsheet_url, worksheet="Results", data=updated_data)
            st.info("✅ Result saved to Google Sheets.")
        except Exception as e:
            st.error(f"Error saving data: {e}")

    if st.button("Restart Quiz"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

