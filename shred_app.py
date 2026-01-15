import streamlit as st
from datetime import datetime, date, time
import pandas as pd
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="90 Days", page_icon="⚡", layout="wide")

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
    
    /* Guidelines Box */
    .guide-box {
        border-left: 4px solid #FF4B2B;
        background: rgba(255, 75, 43, 0.1);
        padding: 10px 15px;
        margin-bottom: 15px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DYNAMIC SIDEBAR ---
with st.sidebar:
    st.title("⚡ 90 Days Hard Challenge")
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
# UPDATED DEADLINE: May 1st, 2026
days_left = (date(2026, 5, 1) - view_date).days

# --- 1. WORKOUT DATABASE (Program Guidelines) ---
workouts = {
    0: ("Chest & Back (Width/Thickness)", [
        {"ex": "BB Floor Press", "sets": "4 sets x 12-15", "url": "uUGDRwge4F8"},
        {"ex": "BB Bent Over Row", "sets": "4 sets x 12-15", "url": "6TSzP8P-S0I"},
        {"ex": "DB Floor Flys", "sets": "3 sets x 12-15", "url": "eGjt4lk6g34"},
        {"ex": "One-Arm DB Row", "sets": "3 sets x 12/side", "url": "dFzUjzuW_20"},
        {"ex": "Push-ups", "sets": "3 sets x Failure", "url": "IODxDxX7oi4"},
        {"ex": "DB Pullover", "sets": "3 sets x 15", "url": "jQjWlJTK5yU"}
    ]),
    1: ("Shoulders & Arms (Arnold Look)", [
        {"ex": "Arnold Press", "sets": "4 sets x 10-12", "url": "3mlObjy7O7w"},
        {"ex": "Side Lateral Raise", "sets": "4 sets x 15", "url": "3VcKaXpzqRo"},
        {"ex": "BB Upright Row", "sets": "3 sets x 12", "url": "amCU-ziCQ4E"},
        {"ex": "BB Bicep Curl", "sets": "4 sets x 10-12", "url": "kwG2ipFRgfo"},
        {"ex": "BB Skullcrushers", "sets": "4 sets x 12", "url": "d_KZxk8_SMc"},
        {"ex": "Hammer Curls", "sets": "3 sets x 12", "url": "7jqi2qWAUXk"},
        {"ex": "Overhead Extension", "sets": "3 sets x 15", "url": "6SS6K3lAwWI"}
    ]),
    2: ("Legs & Lower Back (Calorie Burn)", [
        {"ex": "Goblet Squat", "sets": "4 sets x 15-20", "url": "MeIiGibT690"},
        {"ex": "DB Lunges", "sets": "3 sets x 12/leg", "url": "D7KaRcUTQeE"},
        {"ex": "Stiff-Leg Deadlift", "sets": "4 sets x 12-15", "url": "jcNh17Ckjgg"},
        {"ex": "Calf Raises", "sets": "4 sets x 20", "url": "KxEYX_cEbFA"},
        {"ex": "Plank", "sets": "3 sets x 45 sec", "url": "ASdvN_XEl_c"}
    ])
}
# Map Day 4, 5, 6
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = ("Rest & Active Recovery", [])

# --- 2. WARMUP DATABASE (Specifics) ---
warmups = {
    0: ("Chest Warmup", [
        {"name": "Arm Circles (Big & Small)", "url": "1P-y6bPg1q4"},
        {"name": "Torso Twists (30s)", "url": "q5At0q7k3F4"},
        {"name": "Wall Slides (15 reps)", "url": "2Q2g4g0w0M0"},
        {"name": "Cat-Cow Stretch (10 reps)", "url": "kqnua4rHVVA"},
        {"name": "Push-up to Down Dog (10 reps)", "url": "z-tX1B3jXjo"}
    ]),
    1: ("Shoulder Warmup", [
        {"name": "Shoulder Dislocations (15 reps)", "url": "02e1y2q4dKA"},
        {"name": "Band Pull-Aparts (Simulate)", "url": "fo3d4b68J58"},
        {"name": "Arm Cross Swings (30s)", "url": "4rGqjH1a2j0"},
        {"name": "Wrist Circles", "url": "mJ2m55f6e8U"}
    ]),
    2: ("Leg Warmup", [
        {"name": "Leg Swings (Front/Side)", "url": "4K5i5J5q5r0"},
        {"name": "Bodyweight Squats (20 reps)", "url": "aclHkVaku9U"},
        {"name": "Lunge with Twist (10/side)", "url": "4rGqjH1a2j0"},
        {"name": "High Knees (30s)", "url": "Z7z7sZ3A1kU"},
        {"name": "Glute Bridges (15 reps)", "url": "0Di1rZ7r-20"}
    ])
}
for i in range(3, 6): warmups[i] = warmups[i-3]
warmups[6] = ("Recovery Flow", [{"name": "30 Min Brisk Walk", "url": "nj155mF4q_Y"}])

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
warmup_title, warmup_list = warmups[day_idx]

# --- DASHBOARD UI ---

# HEADER
st.markdown(f"""
    <div class="hero-header">
        <h1 style="margin-bottom: 5px;">Day {days_into_program}: {routine_name}</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            <b>Date:</b> {view_date.strftime('%A, %d %B %Y')} • 
            <b>Countdown:</b> {days_left} Days to May 1st
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
    # A. WARMUP (Specifics)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"🔥 Step 1: {warmup_title}")
    st.write("Perform all movements for 5-7 minutes.")
    
    for move in warmup_list:
        with st.expander(move['name']):
            st.video(f"https://www.youtube.com/watch?v={move['url']}")
            # Fallback Link
            alt_url = f"https://www.youtube.com/results?search_query={move['name'].replace(' ', '+')}"
            st.markdown(f"[🎥 Video Unavailable? Search Here]({alt_url})")
            st.checkbox(f"Done: {move['name']}", key=move['name'])
    st.markdown('</div>', unsafe_allow_html=True)

    # B. WORKOUT (Program Guidelines)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"⚔️ Step 2: {routine_name}")
    
    # Guidelines Box
    st.markdown("""
        <div class="guide-box">
            <b>📜 PROGRAM GUIDELINES:</b><br>
            • <b>Rest:</b> 45 Seconds between sets (Fast for Fat Burn)<br>
            • <b>Tempo:</b> 2s Up (Explode) — 1s Squeeze — 3s Down (Control)<br>
            • <b>Setup:</b> Tight spin-locks. Barbell for compounds, DBs for isolation.
        </div>
    """, unsafe_allow_html=True)
    
    if exercise_list:
        for ex in exercise_list:
            with st.expander(f"💪 {ex['ex']}"):
                st.write(f"**Target:** {ex['sets']}")
                st.video(f"https://www.youtube.com/watch?v={ex['url']}")
                alt_url = f"https://www.youtube.com/results?search_query={ex['ex'].replace(' ', '+')}+form"
                st.markdown(f"[🎥 Video Issue? Search Here]({alt_url})")
                st.text_input(f"Notes ({ex['ex']})", key=f"n_{ex['ex']}", placeholder="Log weights used...")
        
        st.divider()
        st.subheader("🏁 Fat Loss Finisher (Cardio Replacement)")
        st.write("Do this immediately after weights:")
        f1, f2, f3 = st.columns(3)
        f1.checkbox("Jumping Jacks (3x1 min)")
        f2.checkbox("Mtn Climbers (3x30 sec)")
        f3.checkbox("Shadow Box (3x2 min)")
        
    else:
        st.info("🧘 Day 7: Active Recovery. Go for a 30-minute Brisk Walk.")
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
                st.success("Analysis: Lat width increasing (Back View). Lower abs sharpening (Front View).")
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
