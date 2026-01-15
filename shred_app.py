import streamlit as st
from datetime import datetime, date

# --- CONFIG ---
st.set_page_config(page_title="Pro Shred Dashboard", page_icon="💪", layout="wide")

# --- FORCED DARK THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    [data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    .metric-card {
        background-color: #1C2128; padding: 20px; border-radius: 15px;
        border: 1px solid #30363D; margin-bottom: 20px; color: white;
    }
    .header-card {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF8008 100%);
        color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px;
    }
    .stVideo { border-radius: 15px; overflow: hidden; }
    label, p, h1, h2, h3, span { color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ App Settings")
    start_date = st.date_input("Training Start Date", value=date(2026, 1, 15))
    target_date = date(2026, 4, 1)
    st.divider()
    start_weight = st.number_input("Starting Weight (kg)", value=80.0)
    goal_weight = st.number_input("Goal Weight (kg)", value=70.0)

# --- CALCULATION LOGIC ---
today = date.today()
days_left = (target_date - today).days
day_of_week = today.weekday() # 0=Mon, 6=Sun

# Workout Database
workout_db = {
    0: ("Chest & Back", [
        {"ex": "Barbell Floor Press", "url": "https://www.youtube.com/watch?v=uUGDRwge4F8"},
        {"ex": "Barbell Bent-Over Row", "url": "https://www.youtube.com/watch?v=6TSzP8P-S0I"},
        {"ex": "Dumbbell Flyes", "url": "https://www.youtube.com/watch?v=eGjt4lk6g34"}
    ]),
    1: ("Shoulders & Arms", [
        {"ex": "Overhead Press", "url": "https://www.youtube.com/watch?v=2yjwxtZ_Vsc"},
        {"ex": "Lateral Raises", "url": "https://www.youtube.com/watch?v=3VcKaXpzqRo"},
        {"ex": "Bicep Curls", "url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"}
    ]),
    2: ("Legs & Abs", [
        {"ex": "Barbell Squats", "url": "https://www.youtube.com/watch?v=gcNh17Ckjgg"},
        {"ex": "Goblet Squats", "url": "https://www.youtube.com/watch?v=MVMnk0HiTMc"},
        {"ex": "Plank", "url": "https://www.youtube.com/watch?v=TvxNkmjdhMM"}
    ]),
}
# Map Thu/Fri/Sat
for i in range(3, 6): workout_db[i] = workout_db[i-3]
# Special Sunday Data
workout_db[6] = ("Recovery & Progress", [])

day_name, exercises = workout_db[day_of_week]

# --- UI LAYOUT ---

# 1. Header
st.markdown(f"""
    <div class="header-card">
        <h1 style='margin:0; color:white !important;'>April Shred Dashboard</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; color:white !important;'>⏳ {days_left} Days Until Your Goal</p>
    </div>
    """, unsafe_allow_html=True)

# 2. Daily Metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-card"><h3>Focus</h3><h2>{day_name}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Weight Log")
    curr_w = st.number_input("Log Weight (kg)", value=start_weight, step=0.1)
    st.write(f"Remaining: {round(curr_w - goal_weight, 1)} kg")
    st.markdown('</div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Diet Progress")
    d1 = st.checkbox("Protein Hit")
    d2 = st.checkbox("Rice Rule")
    d3 = st.checkbox("3.5L Water")
    st.progress(sum([d1, d2, d3]) / 3)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Training & Progress Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📋 Routine & Instructions")
    
    if day_of_week == 6:
        st.info("Today is Sunday Recovery. Use the right panel for your Weekly Progress Check.")
        st.write("**Next Week's Sneak Peek:** Chest & Back starts tomorrow!")
    else:
        for item in exercises:
            with st.expander(f"💪 {item['ex']} (Watch Video)"):
                st.video(item['url'])
                st.write(f"Instruction: Use your $10\\text{{ kg}}$ barbell. Focus on a 3-second descent.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # SUNDAY PROGRESS CHECK - Always visible but emphasized on Sunday
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    if day_of_week == 6:
        st.subheader("📸 Sunday Progress Check")
        st.success("It's Progress Day!")
    else:
        st.subheader("📊 Weekly Stats")
    
    waist = st.number_input("Waist Size (cm)", value=85.0)
    photo = st.file_uploader("Upload Weekly Photo", type=['jpg', 'png'])
    
    if st.button("🚀 SAVE ENTRY"):
        st.balloons()
        st.success("Data Saved to local session.")
    st.markdown("</div>", unsafe_allow_html=True)
