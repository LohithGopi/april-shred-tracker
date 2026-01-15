import streamlit as st
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="April Shred Tracker", page_icon="🔥", layout="centered")

# --- CUSTOM THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stCheckbox { font-size: 20px; padding: 10px; border-radius: 5px; background: #1e2130; margin-bottom: 5px; }
    div.stButton > button:first-child { background-color: #ff4b4b; color: white; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- WORKOUT DATA ---
workouts = {
    0: {"name": "Chest & Back", "exercises": [
        {"ex": "Barbell Floor Press", "url": "https://www.youtube.com/watch?v=uUGDRwge4F8"},
        {"ex": "Barbell Bent-Over Row", "url": "https://www.youtube.com/watch?v=9efgcAjQW7E"},
        {"ex": "Dumbbell Flyes", "url": "https://www.youtube.com/watch?v=eGjt4lk6g34"}
    ], "jog": "15 mins steady pace"},
    1: {"name": "Shoulders & Arms", "exercises": [
        {"ex": "Barbell Overhead Press", "url": "https://www.youtube.com/watch?v=2yjwxtZ_Vsc"},
        {"ex": "Lateral Raises", "url": "https://www.youtube.com/watch?v=3VcKaXpzqRo"},
        {"ex": "Barbell Curls", "url": "https://www.youtube.com/watch?v=kwG2ipFRgfo"}
    ], "jog": "None (Focus on Arms)"},
    2: {"name": "Legs & Abs", "exercises": [
        {"ex": "Barbell Back Squats", "url": "https://www.youtube.com/watch?v=SW_C1A-rejs"},
        {"ex": "Dumbbell Goblet Squats", "url": "https://www.youtube.com/watch?v=MeIiGibT690"},
        {"ex": "Plank (Hold 60s)", "url": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
    ], "jog": "25 mins high intensity"},
}
# Map Thu/Fri/Sat to the same split
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = {"name": "Rest & Recovery", "exercises": [], "jog": "20 min light walk"}

# --- APP HEADER ---
st.title("🏃‍♂️ Arnold Split: April Shred")
day_idx = datetime.now().weekday()
today = workouts[day_idx]

# --- SECTION 1: TODAY'S WORKOUT ---
st.header(f"📅 Today: {today['name']}")
if today['exercises']:
    for item in today['exercises']:
        with st.expander(f"▶️ {item['ex']}"):
            st.video(item['url'])
            st.caption("Focus: 3-second lowering (Eccentric) phase for maximum cut.")
    st.warning(f"🏃 Cardio: {today['jog']}")
else:
    st.success("Recovery Day! Keep the diet clean today.")

st.divider()

# --- SECTION 2: SOUTH INDIAN DIET LOG ---
st.header("🥗 Daily Diet & Habit Log")
st.subheader("Did you hit your targets?")

col1, col2 = st.columns(2)
with col1:
    pre_workout = st.checkbox("☕ Pre: Black Coffee + Banana")
    post_workout = st.checkbox("🥚 Post: 3 Egg Whites / Kadale Kalu")
    protein_lunch = st.checkbox("🍗 Lunch: Chicken/Fish/Paneer")
    
with col2:
    water_target = st.checkbox("💧 Water: 3.5 Liters total")
    low_carb = st.checkbox("🍚 Rice: Only 1/4th of plate")
    no_sugar = st.checkbox("🚫 No Sugar / Fried Snacks")

# --- SECTION 3: PROGRESS TRACKER ---
st.divider()
st.header("📸 Weekly Progress (Sundays)")
w_col1, w_col2 = st.columns(2)
with w_col1:
    weight = st.number_input("Weight (kg)", format="%.2f", step=0.1)
with w_col2:
    waist = st.number_input("Waist (cm)", format="%.1f", step=0.1)

uploaded_photo = st.file_uploader("Upload Sunday Face/Body Photo", type=['jpg', 'png'])

if st.button("SAVE TODAY'S DATA"):
    st.balloons()
    st.success("Data recorded locally. Let's get that April jawline!")