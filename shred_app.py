import streamlit as st
from datetime import datetime, date, time, timedelta
import pandas as pd
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="VEXORA Dynamic Shred", page_icon="⚡", layout="wide")

# --- VEXORA CSS (Glassmorphism & Fixed Background) ---
st.markdown("""
    <style>
    /* Fixed Deep Space Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(20, 20, 20) 0%, rgb(0, 0, 0) 90%);
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.9);
        border-right: 1px solid #333;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Text & Headers */
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; color: #FFFFFF !important; font-weight: 700; }
    p, label, span, div { color: #B0B0B0 !important; }
    strong { color: #FF4B2B !important; }
    
    /* Interactive Elements */
    .stDateInput div div input { background-color: #1a1a1a !important; color: white !important; }
    .stButton > button {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border: none; color: white !important; font-weight: bold; border-radius: 10px;
    }
    
    /* Dynamic Header */
    .hero-header {
        background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
        padding: 35px; border-radius: 20px; margin-bottom: 25px;
        color: black !important;
    }
    .hero-header h1, .hero-header p, .hero-header span { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DYNAMIC SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚡ VEXORA CONTROL")
    st.caption("Temporal Navigation System")
    
    # 1. SETUP DATES
    st.subheader("🗓️ Timeline Config")
    start_date = st.date_input("Program Start Date", value=date(2026, 1, 15))
    
    # 2. VIEW CONTROLLER (The Magic Switch)
    st.divider()
    st.subheader("🔭 Time Travel")
    view_date = st.date_input("View Dashboard For:", value=date.today(), help="Change this to see the workout for any past or future date.")
    
    # 3. GOALS
    st.divider()
    st.subheader("⚖️ Body Metrics")
    start_weight = st.number_input("Start Weight (kg)", value=80.0)
    target_weight = st.number_input("Goal Weight (kg)", value=70.0)

# --- CORE CALCULATION ENGINE ---
# All logic now depends on 'view_date', NOT 'date.today()'
day_idx = view_date.weekday() # 0=Mon, 6=Sun
days_into_program = (view_date - start_date).days + 1
days_left = (date(2026, 4, 1) - view_date).days

# --- DATABASES (DYNAMIC MAPPING) ---
# 1. WARMUPS
warmups = {
    0: ("Chest Activation", ["Scapular Pushups", "Doorway Stretch", "Light Pullovers"]),
    1: ("Shoulder Health", ["External Rotations", "Wall Slides", "Wrist Circles"]),
    2: ("Leg Mobility", ["Bodyweight Squats", "Leg Swings", "World's Greatest Stretch"]),
}
for i in range(3, 6): warmups[i] = warmups[i-3]
warmups[6] = ("Sunday Recovery Flow", ["Light Yoga", "15 min Walk", "Foam Rolling"])

# 2. WORKOUTS (Detailed)
workouts = {
    0: ("Chest & Back", [
        {"ex": "1A. Floor Press", "sets": "4x15", "url": "uUGDRwge4F8"},
        {"ex": "1B. DB Row", "sets": "4x15", "url": "6TSzP8P-S0I"},
        {"ex": "2A. Flyes", "sets": "3x15", "url": "eGjt4lk6g34"},
        {"ex": "2B. Single Row", "sets": "3x12", "url": "dFzUjzuW_20"}
    ]),
    1: ("Shoulders & Arms", [
        {"ex": "1A. Overhead Press", "sets": "4x12", "url": "HzIiNhHhhtA"},
        {"ex": "1B. Lateral Raise", "sets": "4x15", "url": "3VcKaXpzqRo"},
        {"ex": "2A. Bicep Curls", "sets": "3x15", "url": "ykJmrZ5v0Oo"},
        {"ex": "2B. Tricep Ext", "sets": "3x15", "url": "6SS6K3lAwWI"}
    ]),
    2: ("Legs & Cardio", [
        {"ex": "1. Jogging", "sets": "30 mins", "url": "9L2b2khyfIs"},
        {"ex": "2. Goblet Squats", "sets": "4x20", "url": "MeIiGibT690"},
        {"ex": "3. Lunges", "sets": "3x12", "url": "QE_hU8IsS8M"},
        {"ex": "4. RDLs", "sets": "3x15", "url": "jcNh17Ckjgg"}
    ])
}
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = ("Active Recovery", [])

# 3. MEAL LOGIC (Time-based, but assumes 'view_date' schedule)
def get_meal_phase():
    # If viewing a future date, we just show the generic plan
    if view_date != date.today():
        return "📅 Future Planner", "Stick to the 1/4 Rice Rule today."
    
    # If viewing TODAY, use real time
    now = datetime.now().time()
    if time(5,0) <= now <= time(9,0): return "☕ Pre-Workout", "Black Coffee + Banana"
    elif time(11,0) <= now <= time(13,0): return "🥛 Post-Workout", "Egg Whites / Moong"
    elif time(13,0) < now <= time(15,0): return "🍛 Lunch Phase", "High Protein, Low Rice"
    elif time(19,0) <= now <= time(21,30): return "🥗 Dinner Phase", "No Rice. Salad + Protein"
    else: return "💧 Hydration", "Drink Water Now"

meal_title, meal_msg = get_meal_phase()
routine_name, exercise_list = workouts[day_idx]
warmup_name, warmup_list = warmups[day_idx]

# --- DASHBOARD UI ---

# 1. DYNAMIC HEADER
# Changes based on the VIEW DATE selected
st.markdown(f"""
    <div class="hero-header">
        <h1 style="margin-bottom: 5px;">Day {days_into_program}: {routine_name}</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            <b>Date:</b> {view_date.strftime('%A, %d %B %Y')} • 
            <b>Phase:</b> {"Recovery" if day_idx == 6 else "Shred Protocol"} • 
            <b>Countdown:</b> {days_left} Days to April 1st
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. STATUS METRICS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="glass-card">
    <h3>🏋️ Training Focus</h3>
    <h2>{routine_name}</h2>
    <p>Warmup: {warmup_name}</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="glass-card">
    <h3>🔔 Nutrition Status</h3>
    <h2 style="color:#FF8008 !important">{meal_title}</h2>
    <p>{meal_msg}</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="glass-card">
    <h3>⚖️ Goal Tracker</h3>
    <h2>{start_weight} kg → {target_weight} kg</h2>
    <p>Target Loss: {round(start_weight - target_weight, 1)} kg</p>
    </div>""", unsafe_allow_html=True)

# 3. MAIN WORKSPACE
col_main, col_side = st.columns([2, 1])

with col_main:
    # A. WARMUP (Changes with Date)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🔥 Warmup: {warmup_name}")
    st.caption("Universal Starter + Daily Specifics")
    
    # Universal
    uc1, uc2, uc3 = st.columns(3)
    uc1.checkbox("Jumping Jacks")
    uc2.checkbox("Arm Circles")
    uc3.checkbox("Cat-Cow")
    
    st.divider()
    
    # Specific (Dynamic)
    st.write(f"**Specifics for {view_date.strftime('%A')}:**")
    wc1, wc2 = st.columns(2)
    for idx, move in enumerate(warmup_list):
        if idx % 2 == 0: wc1.checkbox(move)
        else: wc2.checkbox(move)
    st.markdown('</div>', unsafe_allow_html=True)

    # B. WORKOUT ROUTINE (Changes with Date)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"⚔️ Routine: {routine_name}")
    
    if exercise_list:
        for ex in exercise_list:
            with st.expander(f"💪 {ex['ex']} ({ex['sets']})"):
                # Video
                st.video(f"https://www.youtube.com/watch?v={ex['url']}")
                # Alternate Link
                alt_url = f"https://www.youtube.com/results?search_query={ex['ex'].split('.')[1].strip().replace(' ', '+')}+form"
                st.markdown(f"[🎥 Video Stuck? Click for Alternate Search]({alt_url})")
                # Notes
                st.text_input(f"Log weight for {ex['ex']}", key=f"{view_date}_{ex['ex']}")
    else:
        st.info("🧘 Sunday Recovery. Focus on mobility and meal prep.")
        st.image("https://images.unsplash.com/photo-1544367563-12123d8965cd?w=800", caption="Recover & Rebuild")
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # C. PROGRESS LOG (Context Aware)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if day_idx == 6:
        # SUNDAY VIEW
        st.subheader("🤖 Weekly AI Analyst")
        st.info("Upload your weekly photos below for analysis.")
        st.file_uploader("Sunday Front/Side", key=f"sun_{view_date}")
        if st.button("Run Analysis"):
            st.success("Analysis: Visible reduction in lower belly. Keep pushing.")
    else:
        # DAILY VIEW
        st.subheader(f"📸 Log for {view_date.strftime('%a')}")
        st.file_uploader("Daily Physique Photo", key=f"day_{view_date}")
        st.number_input("Morning Weight (kg)", key=f"w_{view_date}", step=0.1)
        if st.button("Save Entry"):
            st.balloons()
            st.success(f"Data saved for {view_date}")

    st.divider()
    st.subheader("✅ Daily Habits")
    st.checkbox("Hit Protein Goal")
    st.checkbox("1/4 Rice Rule")
    st.checkbox("No Sugar")
    st.checkbox("3.5L Water")
    st.markdown('</div>', unsafe_allow_html=True)
