import streamlit as st
from datetime import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="Shred Dashboard", page_icon="💪", layout="wide")

# Custom CSS for the "Crunch Fitness" Dashboard Look
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; color: #333; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; }
    
    /* Card Styling */
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .header-card {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF8008 100%);
        color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px;
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    .stCheckbox { background: white; padding: 10px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- CALCULATIONS ---
deadline = datetime(2026, 4, 1)
days_left = (deadline - datetime.now()).days
workout_data = {
    0: ("Chest & Back", ["Floor Press", "Barbell Row", "Flyes"]),
    1: ("Shoulders & Arms", ["Overhead Press", "Lateral Raise", "Curls"]),
    2: ("Legs & Abs", ["Back Squats", "Goblet Squats", "Plank"]),
}
for i in range(3, 6): workout_data[i] = workout_data[i-3]
workout_data[6] = ("Rest & Recovery", [])

day_name, exercises = workout_data[datetime.now().weekday()]

# --- SIDEBAR (Gym Listing Style) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/69/69840.png", width=50)
    st.title("Gym Listing")
    st.text_input("🔍 Search Workouts")
    st.markdown("### My Plan\n**365 Executive Plan**")
    st.divider()
    st.markdown("### Quick Stats")
    st.metric("Daily Water", "3.5L", "0.5L")
    st.metric("Consistency", "92%", "4%")

# --- MAIN CONTENT ---
# Header Card
st.markdown(f"""
    <div class="header-card">
        <h1 style='margin:0;'>April Shred Dashboard</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Mysuru, KA • ⏳ {days_left} Days to Deadline</p>
    </div>
    """, unsafe_allow_html=True)

# Top Metrics (Punch in, Revenue, Expense style)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Today's Split")
    st.title(day_name)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Current Weight")
    st.title("78.5 kg")
    st.markdown("📉 -1.2kg this week")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Diet Adherence")
    st.title("85%")
    st.progress(0.85)
    st.markdown("</div>", unsafe_allow_html=True)

# Workout & Diet Section
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📋 Training Plan")
    if exercises:
        for ex in exercises:
            with st.expander(f"💪 {ex}"):
                st.write("Video instruction placeholder...")
                st.info("Form Tip: 3-second lowering phase.")
    else:
        st.write("Enjoy your active recovery! Go for a 20-min light walk.")
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🥗 Diet Log")
    st.checkbox("Pre-Workout Meal")
    st.checkbox("Post-Workout Protein")
    st.checkbox("Quarter Plate Rice")
    st.checkbox("3.5L Water")
    st.markdown("</div>", unsafe_allow_html=True)

# Progress Section
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.subheader("📈 Body Progression")
st.file_uploader("Upload Sunday Photo", label_visibility="collapsed")
st.button("Save Daily Log")
st.markdown("</div>", unsafe_allow_html=True)
