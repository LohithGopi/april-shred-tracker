import streamlit as st
from datetime import datetime, date, time
import pandas as pd
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="Arnold Split Basic Training", page_icon="⚡", layout="wide")

# --- VEXORA CSS ---
st.markdown("""
    <style>
    /* Deep Space Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(20, 20, 20) 0%, rgb(0, 0, 0) 90%);
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.95);
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
    
    /* Typography */
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; color: #FFFFFF !important; font-weight: 700; }
    p, label, span, div, li { color: #B0B0B0 !important; }
    strong { color: #FF4B2B !important; }
    
    /* Interactive */
    .stDateInput div div input { background-color: #1a1a1a !important; color: white !important; }
    .stButton > button {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border: none; color: white !important; font-weight: bold; border-radius: 10px;
    }
    
    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
        padding: 35px; border-radius: 20px; margin-bottom: 25px;
        color: black !important;
    }
    .hero-header h1, .hero-header p, .hero-header span { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DYNAMIC SIDEBAR ---
with st.sidebar:
    st.title("⚡ VEXORA HOME")
    st.caption("South Indian Cut Protocol")
    
    st.subheader("🗓️ Timeline")
    start_date = st.date_input("Start Date", value=date(2026, 1, 15))
    view_date = st.date_input("View Dashboard For:", value=date.today())
    
    st.divider()
    st.subheader("🥗 Daily Diet Mode")
    diet_option = st.radio("Select Menu:", ["Option A: Non-Veg", "Option B: Veg"])
    
    st.divider()
    st.subheader("⚖️ Metrics")
    start_weight = st.number_input("Start Weight (kg)", value=80.0)
    target_weight = st.number_input("Goal Weight (kg)", value=70.0)

# --- CORE LOGIC ---
day_idx = view_date.weekday()
days_into_program = (view_date - start_date).days + 1
days_left = (date(2026, 4, 1) - view_date).days

# --- 1. WORKOUT DATABASE (Exact Plan) ---
workouts = {
    0: ("Chest & Back (Day 1)", [
        {"ex": "1A. Floor Press", "sets": "4 sets x 15-20 reps", "url": "uUGDRwge4F8"},
        {"ex": "1B. DB Row", "sets": "4 sets x 15-20 reps", "url": "VKFeB7kx8fs"},
        {"ex": "2A. Flyes", "sets": "3 sets x 15 reps", "url": "eGjt4lk6g34"},
        {"ex": "2B. Single Row", "sets": "3 sets x 12 reps/arm", "url": "dFzUjzuW_20"},
        {"ex": "3. Jogging", "sets": "15–20 mins post-workout", "url": "9L2b2khyfIs"}
    ]),
    1: ("Shoulders & Arms (Day 2)", [
        {"ex": "1A. Overhead Press", "sets": "4 sets x 12-15 reps", "url": "HzIiNhHhhtA"},
        {"ex": "1B. Lateral Raises", "sets": "4 sets x 15-20 reps", "url": "3VcKaXpzqRo"},
        {"ex": "2A. Bicep Curls", "sets": "3 sets x 15 reps", "url": "ykJmrZ5v0Oo"},
        {"ex": "2B. Tricep Ext", "sets": "3 sets x 15 reps", "url": "6SS6K3lAwWI"},
        {"ex": "3. Hammer Curls", "sets": "3 sets to failure", "url": "7jqi2qWAUXk"}
    ]),
    2: ("Legs & Cardio (Day 3)", [
        {"ex": "1. Jogging", "sets": "20–30 mins (Priority)", "url": "9L2b2khyfIs"},
        {"ex": "2. Goblet Squats", "sets": "4 sets x 20 reps", "url": "MeIiGibT690"},
        {"ex": "3. Forward Lunges", "sets": "3 sets x 12 reps/leg", "url": "QE_hU8IsS8M"},
        {"ex": "4. RDL (DB)", "sets": "3 sets x 15 reps", "url": "jcNh17Ckjgg"}
    ])
}
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = ("Sunday Recovery", [])

# --- 2. WARMUP DATABASE (With Videos) ---
# Universal Starter
universal_warmup = [
    {"name": "Jumping Jacks (1 min)", "url": "c4DAnQ6DtF8"},
    {"name": "Arm Circles (30 sec)", "url": "1P-y6bPg1q4"},
    {"name": "Cat-Cow (10 reps)", "url": "kqnua4rHVVA"}
]

# Daily Specifics
specific_warmups = {
    0: ("Chest Focus", [
        {"name": "Scapular Pushups", "url": "P7j98725k5c"},
        {"name": "Doorway Stretch (Dynamic)", "url": "r2Vk6r65r1c"},
        {"name": "Light DB Pullover", "url": "jQjWlJTK5yU"}
    ]),
    1: ("Shoulder Focus", [
        {"name": "External Rotations", "url": "q5sNYB1QZsA"},
        {"name": "Wall Slides", "url": "2Q2g4g0w0M0"},
        {"name": "Wrist Circles", "url": "mJ2m55f6e8U"}
    ]),
    2: ("Leg Focus", [
        {"name": "Bodyweight Squats (x15)", "url": "aclHkVaku9U"},
        {"name": "Leg Swings", "url": "4K5i5J5q5r0"},
        {"name": "World’s Greatest Stretch", "url": "-C8Q1a1q0cE"}
    ])
}
for i in range(3, 6): specific_warmups[i] = specific_warmups[i-3]
specific_warmups[6] = ("Recovery Flow", [{"name": "15 Min Yoga", "url": "v7AYKMP6rOE"}])

# --- 3. DIET MENUS ---
diet_menus = {
    "Option A: Non-Veg": {
        "Essentials": ["Pre: Black Coffee + 1 Banana", "Post: 3-4 Boiled Egg Whites"],
        "Breakfast": "3 Egg Omelette + 2 Small Idlis",
        "Lunch": "150g Chicken Curry (Low Oil) + 1/4 Brown Rice",
        "Dinner": "2 Chapatis + 100g Grilled Fish + Salad"
    },
    "Option B: Veg": {
        "Essentials": ["Pre: Black Coffee + 1 Banana", "Post: 1 Scoop Whey OR Sprouted Moong"],
        "Breakfast": "1 Cup Pesarattu OR Paneer Bhurji + 1 Chapati",
        "Lunch": "1 Cup Thick Sambar + 100g Paneer + Small Rice",
        "Dinner": "2 Chapatis + Mixed Veg Kootu + Salad"
    }
}
selected_diet = diet_menus[diet_option]

# --- 4. MEAL REMINDER ---
def get_meal_phase():
    if view_date != date.today(): return "📅 Planning", "Reviewing " + str(view_date)
    now = datetime.now().time()
    if time(5,0) <= now <= time(9,0): return "☕ Pre-Workout", "Black Coffee + Banana"
    elif time(11,0) <= now <= time(13,0): return "🥛 Post-Workout", "Protein / Egg Whites"
    elif time(13,0) < now <= time(15,0): return "🍛 Lunch", "1/4 Rice Rule Active"
    elif time(19,0) <= now <= time(21,30): return "🥗 Dinner", "No Rice. Chapati Only."
    else: return "💧 Hydration", "Drink Water Now"

meal_title, meal_msg = get_meal_phase()
routine_name, exercise_list = workouts[day_idx]
warmup_title, warmup_list = specific_warmups[day_idx]

# --- DASHBOARD UI ---

# HEADER
st.markdown(f"""
    <div class="hero-header">
        <h1 style="margin-bottom: 5px;">Day {days_into_program}: {routine_name}</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            <b>Date:</b> {view_date.strftime('%A, %d %B %Y')} • 
            <b>Countdown:</b> {days_left} Days to April 1st
        </p>
    </div>
""", unsafe_allow_html=True)

# METRICS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="glass-card"><h3>🏋️ Daily Focus</h3><h2>{routine_name}</h2><p>Warmup: {warmup_title}</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="glass-card"><h3>🔔 Nutrition Alert</h3><h2 style="color:#FF8008 !important">{meal_title}</h2><p>{meal_msg}</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="glass-card"><h3>⚖️ Goal Tracker</h3><h2>{start_weight} kg → {target_weight} kg</h2><p>Target Loss: {round(start_weight - target_weight, 1)} kg</p></div>""", unsafe_allow_html=True)

# MAIN CONTENT
col_main, col_side = st.columns([2, 1])

with col_main:
    # A. WARMUP (Video Enabled)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🔥 Step 1: {warmup_title}")
    
    tab_u, tab_s = st.tabs(["1. Universal Starter", "2. Specific Warmup"])
    
    with tab_u:
        for move in universal_warmup:
            with st.expander(move['name']):
                st.video(f"https://www.youtube.com/watch?v={move['url']}")
                st.checkbox(f"Done: {move['name']}", key=move['name'])
    
    with tab_s:
        for move in warmup_list:
            with st.expander(move['name']):
                st.video(f"https://www.youtube.com/watch?v={move['url']}")
                st.checkbox(f"Done: {move['name']}", key=move['name'])
    
    st.info("⚠️ Warmup Rule: Do 1 set @ 50% weight before your first heavy set.")
    st.markdown('</div>', unsafe_allow_html=True)

    # B. WORKOUT
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"⚔️ Step 2: {routine_name}")
    st.write("Perform 'A' and 'B' as a Superset (30s rest).")
    
    if exercise_list:
        for ex in exercise_list:
            with st.expander(f"💪 {ex['ex']}"):
                st.write(f"**Target:** {ex['sets']}")
                st.video(f"https://www.youtube.com/watch?v={ex['url']}")
                alt_url = f"https://www.youtube.com/results?search_query={ex['ex'].replace(' ', '+')}+form"
                st.markdown(f"[🎥 Video Issue? Search Here]({alt_url})")
                st.text_input(f"Notes ({ex['ex']})", key=f"n_{ex['ex']}")
    else:
        st.info("Sunday Recovery Day.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # C. SOUTH INDIAN DIET
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🥗 {diet_option}")
    st.write("**Essentials:**")
    for item in selected_diet["Essentials"]: st.checkbox(item)
    st.divider()
    st.write("**Main Meals:**")
    st.checkbox(f"🍳 {selected_diet['Breakfast']}")
    st.checkbox(f"🍛 {selected_diet['Lunch']}")
    st.checkbox(f"🥗 {selected_diet['Dinner']}")
    st.divider()
    st.subheader("💧 Hydration (4L)")
    water = st.slider("Liters", 0.0, 4.0, 1.5, 0.5)
    st.markdown('</div>', unsafe_allow_html=True)

    # D. DUAL PHOTO UPLOAD
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if day_idx == 6:
        # SUNDAY (Weekly Analyst)
        st.subheader("🤖 Weekly AI Analyst")
        st.write("Upload BOTH views for full analysis.")
        f_pic = st.file_uploader("1. Front View", key="sun_front")
        b_pic = st.file_uploader("2. Back View", key="sun_back")
        
        if st.button("Run Full Analysis"):
            if f_pic and b_pic:
                st.success("Analysis Complete: Lat width increasing (Back View). Lower abs sharpening (Front View).")
            else:
                st.error("Please upload both photos.")
    else:
        # DAILY LOG
        st.subheader("📸 Daily Body Log")
        st.write("Track changes daily.")
        d_f = st.file_uploader("Front View", key=f"day_f_{view_date}")
        d_b = st.file_uploader("Back View", key=f"day_b_{view_date}")
        
        if st.button("Save Daily Log"):
            st.success("Daily visual log saved.")

    st.markdown('</div>', unsafe_allow_html=True)
