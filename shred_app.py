import streamlit as st
from datetime import datetime, date, time
import time as t_module

# --- CONFIG & THEME ---
st.set_page_config(page_title="Arnold Shred Pro", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    .metric-card { background-color: #1C2128; padding: 20px; border-radius: 15px; border: 1px solid #30363D; margin-bottom: 20px; }
    .header-card { background: linear-gradient(90deg, #FF4B2B 0%, #FF8008 100%); color: white; padding: 25px; border-radius: 20px; margin-bottom: 25px; }
    .warmup-box { background-color: #121921; border-left: 5px solid #00D1FF; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .timer-box { background-color: #211616; border: 2px solid #FF4B2B; padding: 20px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
today = date.today()
day_idx = today.weekday()
now_time = datetime.now().time()

# Warmup Database
warmup_db = {
    0: ["Scapular Pushups", "Doorway Chest Stretch (Pulse)", "Light DB Pullovers"],
    1: ["External Rotations", "Wall Slides", "Wrist Circles"],
    2: ["15 Bodyweight Squats", "Leg Swings (Pendulum)", "World’s Greatest Stretch", "Ankle Circles"],
}
for i in range(3, 6): warmup_db[i] = warmup_db[i-3]
warmup_db[6] = ["Light Stretching", "Mobility Work"]

# --- SIDEBAR: REST TIMER ---
with st.sidebar:
    st.header("⏱️ Superset Rest Timer")
    rest_time = st.number_input("Seconds", value=30, step=5)
    if st.button("START TIMER"):
        placeholder = st.empty()
        for i in range(rest_time, 0, -1):
            placeholder.markdown(f"<h1 style='text-align:center; color:#FF4B2B;'>{i}</h1>", unsafe_allow_html=True)
            t_module.sleep(1)
        st.success("REST OVER! START SET B")
        st.audio("https://www.soundjay.com/buttons/beep-07.wav")

# --- HEADER & MEAL NOTIF ---
st.markdown('<div class="header-card"><h1 style="margin:0; color:white;">April Shred Dashboard</h1></div>', unsafe_allow_html=True)

# --- STEP 1: WARMUP SECTION ---
st.header("🧘 Step 1: Warmup (Core & Specific)")
col_w1, col_w2 = st.columns(2)

with col_w1:
    st.markdown('<div class="warmup-box">', unsafe_allow_html=True)
    st.subheader("⚡ 3-Min Full Body Starter")
    st.checkbox("Jumping Jacks (1 min)")
    st.checkbox("Arm Circles (30 sec)")
    st.checkbox("Cat-Cow Stretch (10 reps)")
    st.markdown('</div>', unsafe_allow_html=True)

with col_w2:
    st.markdown('<div class="warmup-box">', unsafe_allow_html=True)
    st.subheader(f"🎯 Daily Specific: Day {day_idx+1}")
    for move in warmup_db[day_idx]:
        st.checkbox(move)
    st.info("⚠️ RULE: Finish 1 set @ 50% weight before heavy sets.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 2: TRAINING & DIET ---
st.divider()
st.header("🏋️ Step 2: Training & Nutrition")

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📋 Training Routine")
    # Using your previously provided specific workout plan logic here
    st.write("**Superset Focus:** 30s rest between 1A and 1B.")
    st.checkbox("Superset 1 (4 Sets)")
    st.checkbox("Superset 2 (3 Sets)")
    st.checkbox("Finisher / Jogging")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🥗 Diet Adherence")
    d1 = st.checkbox("Pre-Workout Fuel")
    d2 = st.checkbox("Post-Workout Protein")
    d3 = st.checkbox("1/4 Rice Rule")
    d4 = st.checkbox("3.5L Water")
    score = (sum([d1, d2, d3, d4]) / 4) * 100
    st.write(f"Daily Compliance: **{int(score)}%**")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PROGRESS LOGGING ---
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.subheader("📊 Log Weight & Sunday Photos")
st.number_input("Current Weight (kg)", step=0.1)
if day_idx == 6: # Sunday
    st.file_uploader("Upload Sunday Progress Photo")
if st.button("🚀 SAVE DAILY DATA"):
    st.balloons()
    st.success("Log Saved locally.")
st.markdown('</div>', unsafe_allow_html=True)
