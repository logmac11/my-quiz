import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="IT Data Analytics Quiz", page_icon="📊")

# Your Spreadsheet URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/11tpVhGAqNGGH0XraZg1URZJvWEh8SPmiWfoJOmTw__8/edit?usp=sharing"

# ... (Previous Questions and Session State Code) ...

# --- STEP 3: SUBMISSION LOGIC ---
else:
    st.balloons()
    score, total = st.session_state.score, len(questions)
    st.success(f"### Thank you, {st.session_state.name}!")
    
    try:
        # Pass the URL directly to the connection
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        new_row = pd.DataFrame([{
            "Name": st.session_state.name,
            "Phone": st.session_state.phone,
            "Email": st.session_state.email,
            "Score": score,
            "Total": total,
            "Percentage": f"{(score/total)*100}%",
            "Time Submitted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        # NOTE: Make sure your Google Sheet tab is renamed from 'Sheet1' to 'Results'
        existing_data = conn.read(spreadsheet=spreadsheet_url, worksheet="Results")
        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(spreadsheet=spreadsheet_url, worksheet="Results", data=updated_data)
        
        st.info("✅ Result successfully saved to your Google Sheet.")
    except Exception as e:
        st.error(f"Error saving data: {e}")
