import streamlit as st
from datetime import datetime, date, time
import pandas as pd
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="VEXORA Shred Pro", page_icon="⚡", layout="wide")

# --- ADVANCED CSS (VEXORA STYLE) ---
st.markdown("""
    <style>
    /* 1. FIXED BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(30, 30, 30) 0%, rgb(0, 0, 0) 90%);
        background-attachment: fixed;
        background-size: cover;
    }

    /* 2. SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 20, 0.95);
        border-right: 1px solid #333;
    }
    
    /* 3. GLASSMORPHISM CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 75, 43, 0.5);
    }

    /* 4. HEADERS & TEXT */
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #FFFFFF !important; font-weight: 700; }
    p, label, span { color: #A0A0A0 !important; }
    strong { color: #FFFFFF !important; }

    /* 5. INTERACTIVE ELEMENTS */
    .stCheckbox { background: transparent; }
    .stButton > button {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border: none; color: white; border-radius: 12px; padding: 15px 30px; font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
    }
    
    /* 6. CRUNCH STYLE HEADER */
    .hero-header {
        background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
        padding: 40px; border-radius: 25px; color: black; margin-bottom: 30px;
        position: relative; overflow: hidden;
    }
    .hero-header h1 { color: #1a1a1a !important; }
    
    /* 7. CUSTOM ALERTS */
    .notif-pill {
        background: rgba(255, 75, 43, 0.2); border: 1px solid #FF4B2B;
        color: #FF4B2B; padding: 5px 15px; border-radius: 50px; font-size: 0.9em;
        display: inline-block; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR LOGIC ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10479/10479787.png", width=60)
    st.title("VEXORA SHRED")
    st.caption("Personal Transformation OS")
    st.divider()
    
    st.subheader("⚙️ Configuration")
    start_date = st.date_input("Start Date", value=date(2026, 1, 15))
    target_date = date(2026, 4, 1)
    
    st.subheader("🎯 Goals")
    start_weight = st.number_input("Starting Kg", value=80.0)
    target_weight = st.number_input("Target Kg", value=70.0)
    
    st.info(f"📆 Days Remaining: {(target_date - date.today()).days}")

# --- BACKEND LOGIC ---
today = date.today()
now_time = datetime.now().time()
days_passed = (today - start_date).days
day_idx = today.weekday()

# MEAL REMINDER SYSTEM
def get_meal_status():
    if time(5,0) <= now_time <= time(9,0): return "☕ Pre-Workout Phase", "Grab Black Coffee + Banana"
    elif time(11,0) <= now_time <= time(13,0): return "🥛 Anabolic Window", "Egg Whites / Moong Salad"
    elif time(13,0) < now_time <= time(15,0): return "🍛 Lunch Protocol", "1/4 Rice Rule Active"
    elif time(19,0) <= now_time <= time(21,30): return "🥗 Dinner Phase", "No Rice. Chapatis + Salad"
    else: return "💧 Hydration Check", "Drink 500ml Water Now"

status_title, status_msg = get_meal_status()

# WARMUP & WORKOUT DB (Hidden for brevity, fully included)
specific_warmups = {
    0: ["Scapular Pushups", "Doorway Stretch", "Light Pullovers"],
    1: ["External Rotations", "Wall Slides", "Wrist Circles"],
    2: ["Bodyweight Squats (x15)", "Leg Swings", "World's Greatest Stretch"],
}
for i in range(3,6): specific_warmups[i] = specific_warmups[i-3]
specific_warmups[6] = ["15 min Yoga Flow"]

workout_db = {
    0: ("Chest & Back", [{"ex": "1A. Floor Press", "url": "uUGDRwge4F8"}, {"ex": "1B. DB Row", "url": "6TSzP8P-S0I"}]),
    1: ("Shoulders & Arms", [{"ex": "1A. Overhead Press", "url": "HzIiNhHhhtA"}, {"ex": "1B. Lateral Raise", "url": "3VcKaXpzqRo"}]),
    2: ("Legs & Cardio", [{"ex": "Goblet Squats", "url": "MeIiGibT690"}, {"ex": "Romanian DL", "url": "jcNh17Ckjgg"}])
}
for i in range(3,6): workout_db[i] = workout_db[i-3]
workout_db[6] = ("Active Recovery", [])

# --- MAIN DASHBOARD UI ---

# 1. HERO HEADER (Crunch Style)
st.markdown(f"""
    <div class="hero-header">
        <span class="notif-pill">🔥 Day {days_passed + 1} of Transformation</span>
        <h1>Welcome back, Legend.</h1>
        <p style='color:#333 !important;'>Current Phase: <b>{workout_db[day_idx][0]}</b> • Location: Mysuru</p>
    </div>
""", unsafe_allow_html=True)

# 2. TOP METRICS (Interactive Charts)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Weight Trend")
    # Interactive Chart Simulation
    chart_data = pd.DataFrame(np.random.randn(20, 1).cumsum() + start_weight, columns=['Kg'])
    st.line_chart(chart_data, height=100, color="#FF4B2B")
    current_log = st.number_input("Log Today (kg)", value=start_weight, label_visibility="collapsed")
    st.caption(f"{round(current_log - target_weight, 1)} kg to go")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🔔 {status_title}")
    st.markdown(f"<h2 style='color:#FF8008 !important;'>{status_msg}</h2>", unsafe_allow_html=True)
    st.progress(0.65) # Simulating time passed in day
    st.caption("Metabolic Clock Active")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💧 Hydration Level")
    water = st.slider("Liters Drank", 0.0, 4.0, 1.5, 0.5)
    if water >= 3.5:
        st.success("Target Hit! 🌊")
    else:
        st.caption(f"{3.5 - water}L remaining")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. MAIN WORKSPACE
col_main, col_sidebar = st.columns([2, 1])

with col_main:
    # A. WARMUP SECTION
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔥 Activation Sequence")
    tab1, tab2 = st.tabs(["Universal Starter", "Daily Specific"])
    
    with tab1:
        c_a, c_b, c_c = st.columns(3)
        c_a.checkbox("Jumping Jacks (1m)")
        c_b.checkbox("Arm Circles (30s)")
        c_c.checkbox("Cat-Cow (10x)")
        
    with tab2:
        st.markdown(f"**Focus: {specific_warmups[day_idx][0]}**")
        for move in specific_warmups[day_idx]:
            st.checkbox(move)
    st.markdown('</div>', unsafe_allow_html=True)

    # B. WORKOUT SECTION
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🏋️ {workout_db[day_idx][0]}")
    
    exercises = workout_db[day_idx][1]
    if exercises:
        for ex in exercises:
            with st.expander(f"{ex['ex']}"):
                # Video Player
                st.video(f"https://www.youtube.com/watch?v={ex['url']}")
                # Alternate Link Logic
                alt_url = f"https://www.youtube.com/results?search_query={ex['ex'].replace(' ', '+')}+form"
                st.markdown(f"[⚠️ Video Unavailable? Click for Alternate Search]({alt_url})")
                
                # Note Taking
                st.text_input(f"Notes for {ex['ex']}", placeholder="e.g., Used 10kg, felt easy...")
    else:
        st.info("Sunday Recovery Mode Active.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_sidebar:
    # RIGHT SIDE: PROGRESS & ANALYTICS
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if day_idx == 6:
        st.subheader("🤖 AI Analyst")
        st.write("Upload weekly photos to generate report.")
        st.file_uploader("Sunday Upload", key="wk_up")
        if st.button("Generate Analysis"):
            st.success("Analysis: Abdominal definition increased. continue deficit.")
    else:
        st.subheader("📸 Daily Log")
        st.file_uploader("Upload Physique", key="dy_up")
        st.caption("Consistency is key.")
        
    st.divider()
    st.subheader("🥗 Adherence")
    st.checkbox("High Protein")
    st.checkbox("Low Carb (Night)")
    st.checkbox("No Sugar")
    st.markdown('</div>', unsafe_allow_html=True)
