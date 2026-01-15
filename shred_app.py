import streamlit as st
from datetime import datetime, date

# --- CONFIG ---
st.set_page_config(page_title="Custom Shred Dashboard", page_icon="💪", layout="wide")

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
    /* Input Styling */
    .stDateInput div div input, .stNumberInput div div input {
        background-color: #0E1117 !important; color: white !important; border: 1px solid #FF4B2B !important;
    }
    label, p, h1, h2, h3, span { color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Transformation Setup")
    # FLEXIBLE START DATE
    start_date = st.date_input("When did you start?", value=date.today())
    target_date = date(2026, 4, 1)
    
    st.divider()
    # WEIGHT GOALS
    start_weight = st.number_input("Starting Weight (kg)", value=80.0, step=0.1)
    goal_weight = st.number_input("Goal Weight (kg)", value=72.0, step=0.1)

# --- LOGIC ---
today = date.today()
total_duration = (target_date - start_date).days
days_passed = (today - start_date).days
days_left = (target_date - today).days

# Progress percentage for the bar
if total_duration > 0:
    prog_percent = max(0, min(100, (days_passed / total_duration)))
else:
    prog_percent = 0

# Workout Logic
workout_data = {
    0: ("Chest & Back", [{"ex": "Floor Press", "url": "https://www.youtube.com/watch?v=O130nJ0YfW8"}, {"ex": "Barbell Row", "url": "https://www.youtube.com/watch?v=6TSzP8P-S0I"}]),
    1: ("Shoulders & Arms", [{"ex": "Overhead Press", "url": "https://www.youtube.com/watch?v=8m9_Yq-uDcs"}, {"ex": "Bicep Curls", "url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"}]),
    2: ("Legs & Abs", [{"ex": "Back Squats", "url": "https://www.youtube.com/watch?v=gcNh17Ckjgg"}, {"ex": "Plank", "url": "https://www.youtube.com/watch?v=TvxNkmjdhMM"}]),
}
for i in range(3, 6): workout_data[i] = workout_data[i-3]
workout_data[6] = ("Rest & Recovery", [])
day_name, exercises = workout_data[datetime.now().weekday()]

# --- UI LAYOUT ---

# 1. Header
st.markdown(f"""
    <div class="header-card">
        <h1 style='margin:0; color:white !important;'>April Shred Dashboard</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; color:white !important;'>Mysuru, KA • ⏳ {days_left} Days Until April 1st</p>
    </div>
    """, unsafe_allow_html=True)

# 2. Top Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Today's Training")
    st.title(day_name)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Weight Tracker")
    current_w = st.number_input("Current Weight (kg)", value=start_weight, step=0.1)
    to_go = current_w - goal_weight
    st.markdown(f"**Target:** {goal_weight} kg ({to_go:.1f} kg to go)")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Timeline Progress")
    st.title(f"{int(prog_percent*100)}%")
    st.progress(prog_percent)
    st.markdown(f"<small>Started: {start_date}</small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. Training & Diet
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📋 Routine")
    if exercises:
        for item in exercises:
            with st.expander(f"💪 {item['ex']}"):
                st.video(item['url'])
    else:
        st.info("Sunday Recovery. Keep the water intake high!")
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🥗 Diet Check")
    # Diet adherence calculation
    m1 = st.checkbox("Pre-Workout Fuel")
    m2 = st.checkbox("Post-Workout Protein")
    m3 = st.checkbox("1/4 Rice Portion")
    m4 = st.checkbox("3.5L Water")
    adherence = (sum([m1, m2, m3, m4]) / 4) * 100
    st.write(f"**Daily Adherence:** {int(adherence)}%")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. Save Button
if st.button("🚀 SAVE DAILY PROGRESS"):
    st.balloons()
    st.success(f"Logged: {current_w}kg on Day {days_passed+1} of your journey.")
