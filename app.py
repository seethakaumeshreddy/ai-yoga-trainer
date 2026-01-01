import streamlit as st
import json

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Yoga Trainer", layout="wide")
st.title("🧘 AI Yoga Trainer")

st.info(
    "ℹ️ Note: Live posture correction (camera) works in local mode only. "
    "This cloud version demonstrates pose selection and reference visualization."
)

# ---------------- LOAD POSES ----------------
with open("poses.json", "r", encoding="utf-8") as f:
    POSES = json.load(f)

pose_list = list(POSES.keys())

# ---------------- SELECT POSE ----------------
selected_pose = st.selectbox("Select Yoga Pose", pose_list)

pose_data = POSES[selected_pose]

# ---------------- POSE IMAGE ----------------
st.markdown("### 🖼️ Reference Pose Image")

image_url = f"https://source.unsplash.com/featured/?yoga,{selected_pose.replace(' ', '')}"

st.image(
    image_url,
    caption=f"{selected_pose} (reference image)",
    use_column_width=True
)

# ---------------- POSE DETAILS ----------------
st.markdown("### ℹ️ Pose Information")
st.write("**English Name:**", pose_data.get("english", selected_pose))
st.write("**Category:**", pose_data.get("category", "—"))
st.write("**Difficulty:**", pose_data.get("difficulty", "—"))
st.write("**Benefits:**", pose_data.get("benefits", "—"))

# ---------------- CAMERA MESSAGE ----------------
st.markdown("### 📷 Live Posture Correction")
st.warning(
    "Camera-based posture correction is available in the local version of this project "
    "using OpenCV and MediaPipe."
)
