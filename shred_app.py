import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
from datetime import datetime, date, time

# --- CONFIG ---
st.set_page_config(page_title="90 Days Hard", page_icon="⚡", layout="wide")

# --- VEXORA CSS (Kept from your original design) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 10% 20%, rgb(20, 20, 20) 0%, rgb(0, 0, 0) 90%); background-attachment: fixed; background-size: cover; }
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 15, 0.95); border-right: 1px solid #333; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 25px; margin-bottom: 20px; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; color: #FFFFFF !important; font-weight: 700; }
    p, label, span, div, li { color: #B0B0B0 !important; }
    .hero-header { background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%); padding: 35px; border-radius: 20px; margin-bottom: 25px; color: black !important; }
    .hero-header h1, .hero-header p { color: #1a1a1a !important; }
    .analysis-box { background: rgba(0, 255, 150, 0.1); border: 1px solid #00FF96; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .analysis-warning { background: rgba(255, 165, 0, 0.1); border: 1px solid #FFA500; padding: 15px; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER: CALCULATE ANGLES ---
def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (a, b, c).
    a = first point coordinates [x, y]
    b = mid point coordinates [x, y]
    c = end point coordinates [x, y]
    """
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# --- REAL AI ENGINE (MediaPipe) ---
def process_video(video_path, exercise_name):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(video_path)
    
    # Video Properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Output Video Setup
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    # Using 'avc1' codec for better browser compatibility
    fourcc = cv2.VideoWriter_fourcc(*'avc1') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    feedback_log = []
    frames_processed = 0
    min_knee_angle = 180
    min_elbow_angle = 180
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to RGB (MediaPipe requires RGB)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make detection
        results = pose.process(image)
        
        # Draw the landmarks back onto the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # EXTRACT LANDMARKS
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates for specific joints
            # LEFT SIDE
            l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # CALCULATE REAL ANGLES
            knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
            elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
            
            # Track minimums (max depth/flexion)
            if knee_angle < min_knee_angle: min_knee_angle = knee_angle
            if elbow_angle < min_elbow_angle: min_elbow_angle = elbow_angle

            # Visualize Angles on Screen
            cv2.putText(image, str(int(knee_angle)), tuple(np.multiply(l_knee, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(int(elbow_angle)), tuple(np.multiply(l_elbow, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        out.write(image)
        frames_processed += 1

    cap.release()
    out.release()
    
    # --- INTELLIGENT FEEDBACK GENERATION ---
    final_feedback = {"status": "success", "msg": "Analysis Complete", "details": []}
    
    # 1. SQUAT / LEG LOGIC
    if "Squat" in exercise_name or "Leg" in exercise_name:
        if min_knee_angle < 95:
            final_feedback["details"].append("✅ Great Depth! You broke parallel (knee angle < 90°).")
        elif min_knee_angle < 110:
            final_feedback["details"].append("⚠️ Good Depth, but try to go slightly lower for full activation.")
        else:
            final_feedback["status"] = "warning"
            final_feedback["details"].append("❌ Too High. You didn't reach depth. Aim for hips parallel to knees.")

    # 2. PRESS / PUSH LOGIC
    elif "Press" in exercise_name or "Push" in exercise_name:
        if min_elbow_angle < 70:
            final_feedback["details"].append("✅ Full Range of Motion (Deep stretch at the bottom).")
        else:
            final_feedback["details"].append("⚠️ Try to bring the weight lower to stretch the chest/shoulders more.")

    # 3. PULL / ROW LOGIC
    elif "Row" in exercise_name or "Pull" in exercise_name:
        final_feedback["details"].append("ℹ️ For Rows: Ensure your back remained neutral (straight line) throughout.")
    
    else:
        final_feedback["details"].append(f"Movement analyzed. Max Knee Flexion: {int(min_knee_angle)}°. Max Elbow Flexion: {int(min_elbow_angle)}°.")

    return output_path, final_feedback

# --- DYNAMIC SIDEBAR ---
with st.sidebar:
    st.title("⚡ 90 Days Hard")
    st.caption("Accurate AI Form Edition")
    start_date = st.date_input("Start Date", value=date(2026, 1, 15))
    view_date = st.date_input("View Dashboard For:", value=date.today())
    st.divider()
    diet_option = st.radio("Select Menu:", ["Option A: Non-Veg", "Option B: Veg"])
    st.divider()
    start_weight = st.number_input("Start Weight (kg)", value=80.0)
    target_weight = st.number_input("Goal Weight (kg)", value=70.0)

# --- CORE LOGIC ---
day_idx = view_date.weekday()
days_into_program = (view_date - start_date).days + 1
days_left = (date(2026, 5, 1) - view_date).days

# Workouts & Warmups Data
workouts = {
    0: ("Chest & Back", [{"ex": "BB Floor Press", "sets": "4x12", "url": "uUGDRwge4F8"}, {"ex": "BB Bent Over Row", "sets": "4x12", "url": "6TSzP8P-S0I"}]),
    1: ("Shoulders & Arms", [{"ex": "Arnold Press", "sets": "4x12", "url": "3mlObjy7O7w"}, {"ex": "BB Bicep Curl", "sets": "4x12", "url": "kwG2ipFRgfo"}]),
    2: ("Legs", [{"ex": "Goblet Squat", "sets": "4x15", "url": "MeIiGibT690"}, {"ex": "DB Lunges", "sets": "3x12", "url": "D7KaRcUTQeE"}])
}
# Fill remaining days
for i in range(3, 6): workouts[i] = workouts[i-3]
workouts[6] = ("Rest", [])

warmups = {
    0: ("Upper Body Warmup", [{"name": "Arm Circles", "url": "1P-y6bPg1q4"}]),
    1: ("Shoulder Warmup", [{"name": "Dislocations", "url": "02e1y2q4dKA"}]),
    2: ("Leg Warmup", [{"name": "Leg Swings", "url": "4K5i5J5q5r0"}])
}
for i in range(3, 6): warmups[i] = warmups[i-3]
warmups[6] = ("Recovery", [])

routine_name, exercise_list = workouts[day_idx]
warmup_title, warmup_list = warmups[day_idx]

# --- UI LAYOUT ---
st.markdown(f"""<div class="hero-header"><h1>Day {days_into_program}: {routine_name}</h1><p>Date: {view_date}</p></div>""", unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(f"⚔️ {routine_name}")
    
    if exercise_list:
        for ex in exercise_list:
            with st.expander(f"💪 {ex['ex']}"):
                t1, t2 = st.tabs(["📝 Guide", "🤖 Real AI Analysis"])
                
                with t1:
                    st.write(f"**Target:** {ex['sets']}")
                    st.video(f"https://www.youtube.com/watch?v={ex['url']}")
                
                with t2:
                    st.info("Upload a video. The AI will detect your joints and measure angles.")
                    uploaded_file = st.file_uploader(f"Upload {ex['ex']}", type=['mp4', 'mov'], key=f"vid_{ex['ex']}")
                    
                    if uploaded_file is not None:
                        # Save to temp file for OpenCV to read
                        tfile = tempfile.NamedTemporaryFile(delete=False) 
                        tfile.write(uploaded_file.read())
                        
                        if st.button(f"Start Computer Vision Scan", key=f"btn_{ex['ex']}"):
                            with st.spinner("🤖 Mapping Skeleton & Calculating Angles..."):
                                try:
                                    # RUN THE REAL ENGINE
                                    processed_video_path, feedback = process_video(tfile.name, ex['ex'])
                                    
                                    # Show Feedback
                                    css_class = "analysis-warning" if feedback['status'] == 'warning' else "analysis-box"
                                    st.markdown(f"""<div class="{css_class}"><h3>{feedback['msg']}</h3><ul>{''.join([f'<li>{d}</li>' for d in feedback['details']])}</ul></div>""", unsafe_allow_html=True)
                                    
                                    # Show Processed Video
                                    st.subheader("👁️ AI Vision Overlay")
                                    st.video(processed_video_path)
                                    
                                except Exception as e:
                                    st.error(f"Error analyzing video: {e}")
    else:
        st.info("Rest Day.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🥗 Diet")
    st.write("Track your meals here.")
    st.checkbox("Breakfast")
    st.checkbox("Lunch")
    st.checkbox("Dinner")
    st.markdown('</div>', unsafe_allow_html=True)
