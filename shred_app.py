import streamlit as st
from datetime import datetime

# --- DEADLINE CONFIG ---
deadline = datetime(2026, 4, 1)
today_dt = datetime.now()
days_left = (deadline - today_dt).days

# --- APP CONFIG ---
st.set_page_config(page_title="April Shred Tracker", page_icon="🔥", layout="centered")

# --- CUSTOM THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stCheckbox { font-size: 18px; background: #1e2130; border-radius: 8px; padding: 10px; margin-bottom: 5px; }
    div.stButton > button:first-child { background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & COUNTDOWN ---
st.title("🏃‍♂️ Arnold Split: April Shred")
st.subheader(f"⏳ {max(0, days_left)} Days Until April 1st!")
progress = max(0, min(100, (60 - days_left) / 60)) 
st.progress(progress)

# --- WORKOUT DATA (FIXED VIDEOS) ---
workouts = {
    0: {"name": "Chest & Back", "exercises": [
        {"ex": "Dumbbell/Barbell Floor Press", "url": "https://www.youtube.com/watch?v=uUGDRwge4F8"},
        {"ex": "Barbell Bent-Over Row", "url": "https://www.youtube.com/watch?v=VKFeB7kx8fs"},
        {"ex": "Dumbbell Floor Flyes", "url": "https://www.youtube.com/watch?v=eGjt4lk6g34"}
    ], "jog": "15 mins steady pace"},
    1: {"name": "Shoulders & Arms", "exercises": [
        {"ex": "Overhead Press", "url": "https://www.youtube.com/watch?v=2yjwxtZ_Vsc"},
        {"ex": "Lateral Raises", "url": "https://www.youtube.com/watch?v=3VcKaXpzqRo"},
        {"ex": "Bicep Curls", "url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"},
        {"ex": "Tricep Overhead Extension", "url": "https://www.youtube.com/watch?v=6SS6K3lAwWI"}
    ], "jog": "Rest Day for Legs"},
    2: {"name": "Legs & Abs", "exercises": [
        {"ex": "Barbell Back Squats", "url": "https://www.youtube.com/watch?v=R2dMsVhZTVM"},
        {"ex": "Dumbbell Goblet Squats", "url": "https://www.youtube.com/watch?v=MVMnk0HiTMc"},
        {"ex": "Plank (Focus on core)", "url": "https://www.youtube.com/watch?v=ASdvN_XEl_c"}
    ], "jog": "25 mins high intensity"},
}

# Mapping Thu/Fri/Sat to the same split
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = {"name": "Rest & Recovery", "exercises": [], "jog": "20 min light walk"}

# --- TODAY'S WORKOUT SECTION ---
day_idx = today_dt.weekday()
current_workout = workouts[day_idx]

st.header(f"📅 Today's Split: {current_workout['name']}")

if current_workout['exercises']:
    for item in current_workout['exercises']:
        with st.expander(f"💪 {item['ex']}"):
            st.video(item['url'])
            # Dynamic Fallback Search
            search_url = f"https://www.youtube.com/results?search_query=how+to+do+{item['ex'].replace(' ', '+')}"
            st.write(f"[Problem with video? Click here to search for {item['ex']}]({search_url})")
    st.warning(f"🏃 Cardio Goal: {current_workout['jog']}")
else:
    st.success("Sunday Rest! Focus on your Weekly Progress Photos.")

st.divider()

# --- DIET LOG ---
st.header("🥗 South Indian Diet Log")
c1, c2 = st.columns(2)
with c1:
    st.checkbox("☕ Pre-Workout: Coffee + Banana")
    st.checkbox("🥚 Post-Workout: 3 Egg Whites / Kadale Kalu")
with c2:
    st.checkbox("🍚 Rice: Quarter Plate Only")
    st.checkbox("💧 Water: 3.5 Liters Done")

# --- PROGRESS ---
st.divider()
st.header("📸 Sunday Progress")
w1, w2 = st.columns(2)
with w1:
    weight = st.number_input("Weight (kg)", format="%.2f")
with w2:
    waist = st.number_input("Waist (cm)", format="%.1f")

st.file_uploader("Upload Sunday Photo", type=['jpg', 'png'])

if st.button("SAVE LOG"):
    st.balloons()
    st.success("Progress Saved! See you tomorrow.")
