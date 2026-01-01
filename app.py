import streamlit as st
import cv2 as cv2
import mediapipe as mp
import numpy as np
import time

st.set_page_config(page_title="AI Yoga Trainer", layout="wide")

st.title("🧘 AI Yoga Trainer")

# ---------- Pose options ----------
POSES = {
    "Squat": (90, 110),
    "Warrior Pose": (80, 100),
    "Tree Pose": (160, 180)
}

pose_name = st.selectbox("Select Pose", list(POSES.keys()))
st.write(f"Selected Pose: **{pose_name}**")

# ---------- Start/Stop ----------
start = st.button("Start Camera")
stop = st.button("Stop Camera")

# ---------- Session state ----------
if "run" not in st.session_state:
    st.session_state.run = False

if start:
    st.session_state.run = True
if stop:
    st.session_state.run = False

# ---------- MediaPipe ----------
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

frame_box = st.empty()

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180 / np.pi)
    return 360-angle if angle > 180 else angle

# ---------- Camera Loop (SAFE) ----------
if st.session_state.run:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not accessible")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            lm = results.pose_landmarks.landmark
            hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            angle = calculate_angle(hip, knee, ankle)
            min_a, max_a = POSES[pose_name]

            if min_a <= angle <= max_a:
                text = "Correct Pose ✅"
                color = (0, 255, 0)
            else:
                text = "Adjust Pose ❌"
                color = (255, 0, 0)

            cv2.putText(image, f"Angle: {int(angle)}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(image, text,
                        (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        frame_box.image(image)
        time.sleep(0.03)   # 🔴 THIS LINE IS IMPORTANT

    cap.release()
else:
    st.info("Click **Start Camera** to begin")

