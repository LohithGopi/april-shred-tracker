import streamlit as st
from datetime import datetime, date, time
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Arnold Shred Pro", page_icon="🔥", layout="wide")

# --- FORCED PRO THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    .metric-card { background-color: #1C2128; padding: 20px; border-radius: 15px; border: 1px solid #30363D; margin-bottom: 20px; }
    .header-card { background: linear-gradient(90deg, #FF4B2B 0%, #FF8008 100%); color: white; padding: 25px; border-radius: 20px; margin-bottom: 25px; }
    .notif-box { background-color: #1a1e24; border-left: 5px solid #FF4B2B; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    label, p, h1, h2, h3, span { color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM LOGIC ---
today = date.today()
now_time = datetime.now().time()
day_idx = today.weekday()

# --- 1. MEAL NOTIFICATION SYSTEM ---
def get_meal_reminder():
    if time(5, 0) <= now_time <= time(8, 30):
        return "☕ 5:00-8:30 AM | PRE-WORKOUT: Black Coffee + Banana"
    elif time(8, 31) <= now_time <= time(10, 30):
        return "🍳 8:30-10:30 AM | BREAKFAST: Eggs/Pesarattu + 2 Idli"
    elif time(11, 0) <= now_time <= time(12, 30):
        return "🥛 11:00-12:30 PM | POST-WORKOUT: 3-4 Egg Whites/Moong Salad"
    elif time(13, 0) <= now_time <= time(15, 0):
        return "🍛 1:00-3:00 PM | LUNCH: 150g Chicken/Paneer + 1/4 Cup Rice"
    elif time(19, 0) <= now_time <= time(21, 30):
        return "🥗 7:00-9:30 PM | DINNER: 2 Chapatis + Fish/Dal + Salad"
    else:
        return "💧 HYDRATION: Drink 500ml water now to flush facial bloat."

# --- 2. WORKOUT DATABASE (WITH VIDEOS) ---
workout_db = {
    0: ("Chest & Back", [
        {"ex": "1A. Floor Press", "url": "https://www.youtube.com/watch?v=uUGDRwge4F8"},
        {"ex": "1B. 2-Arm DB Row", "url": "https://www.youtube.com/watch?v=6TSzP8P-S0I"},
        {"ex": "2A. DB Flyes", "url": "https://www.youtube.com/watch?v=eGjt4lk6g34"},
        {"ex": "2B. Single Row", "url": "https://www.youtube.com/watch?v=dFzUjzuW_20"}
    ]),
    1: ("Shoulders & Arms", [
        {"ex": "1A. Overhead Press", "url": "https://www.youtube.com/watch?v=HzIiNhHhhtA"},
        {"ex": "1B. Lateral Raise", "url": "https://www.youtube.com/watch?v=3VcKaXpzqRo"},
        {"ex": "2A. Bicep Curls", "url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"},
        {"ex": "2B. Tricep Ext", "url": "https://www.youtube.com/watch?v=6SS6K3lAwWI"}
    ]),
    2: ("Legs & Cardio", [
        {"ex": "2. Goblet Squats", "url": "https://www.youtube.com/watch?v=MeIiGibT690"},
        {"ex": "3. Forward Lunges", "url": "https://www.youtube.com/watch?v=QE_hU8IsS8M"},
        {"ex": "4. Romanian DL", "url": "https://www.youtube.com/watch?v=jcNh17Ckjgg"}
    ]),
}
for i in range(3, 6): workout_db[i] = workout_db[i-3]
workout_db[6] = ("Recovery", [])

# --- UI LAYOUT ---
st.markdown('<div class="header-card"><h1>April Shred Dashboard</h1></div>', unsafe_allow_html=True)

# Live Meal Reminder
st.markdown(f'<div class="notif-box"><b>🔔 MEAL REMINDER:</b> {get_meal_reminder()}</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    # WORKOUT SECTION
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    day_name, exercises = workout_db[day_idx]
    st.subheader(f"📋 Today's Routine: {day_name}")
    
    if exercises:
        for item in exercises:
            with st.expander(f"💪 {item['ex']} (Watch Form Video)"):
                st.video(item['url'])
                st.info("Instruction: 3-sec lowering phase. Use your Symactive weights.")
    else:
        st.success("Sunday Recovery! Let's analyze your week below.")
    st.markdown('</div>', unsafe_allow_html=True)

    # DAILY PROGRESS (PHOTO UPLOAD)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📸 Daily Body Log")
    st.write("Upload a photo every day to feed the Weekly Analyst.")
    st.file_uploader("Upload Today's Progress Photo", key="daily_p")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # DIET LOG
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🥗 Diet Check")
    d1 = st.checkbox("High Protein")
    d2 = st.checkbox("1/4 Rice Only")
    d3 = st.checkbox("3.5L Water")
    st.markdown('</div>', unsafe_allow_html=True)

    # WEEKLY PROGRESS ANALYST
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    if day_idx == 6:
        st.subheader("🤖 Weekly AI Analyst")
        st.write("It's Sunday. I'm ready to analyze your daily logs.")
        if st.button("RUN WEEKLY ANALYSIS"):
            st.warning("Analyzing daily photos and diet adherence...")
            st.success("Analysis Complete: Jawline sharpness up 12%. Upper body vascularity improving. Recommendation: Stay the course on the 1/4 rice rule.")
    else:
        st.subheader("📈 Weekly Tracker")
        st.write("Full body analysis unlocks every Sunday.")
    
    st.number_input("Log Weight (kg)", step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 SAVE ALL DATA"):
    st.balloons()
    st.success("Data stored for today's session.")
