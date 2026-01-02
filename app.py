import streamlit as st
import json
import requests

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Yoga Trainer", layout="wide")
st.title("🧘 AI Yoga Trainer")

st.info(
    "ℹ️ Note: Live posture correction (camera) works in local mode only. "
    "This cloud version demonstrates pose selection and dynamic reference visualization."
)

# ---------------- LOAD POSES ----------------
with open("poses.json", "r", encoding="utf-8") as f:
    POSES = json.load(f)

pose_list = list(POSES.keys())

# ---------------- SELECT POSE ----------------
selected_pose = st.selectbox("Select Yoga Pose", pose_list)

pose_data = POSES[selected_pose]

# ---------------- DYNAMIC IMAGE FROM WIKIPEDIA ----------------
st.markdown("### 🖼️ Reference Pose Image")
image_url = get_pose_image(selected_pose)

if image_url:
    st.image(
        image_url,
        caption=f"{selected_pose} (Wikipedia reference image)",
        use_column_width=True
    )
else:
    st.warning("No reference image found for this pose.")
image_url = get_pose_image(selected_pose)

if image_url:
    st.image(
        image_url,
        caption=f"{selected_pose} (Wikipedia reference image)",
        use_column_width=True
    )
else:
    st.warning("No reference image found for this pose.")


# ---------------- POSE DETAILS ----------------
st.markdown("### ℹ️ Pose Information")
st.write("**English Name:**", pose_data.get("english", selected_pose))
st.write("**Category:**", pose_data.get("category", "—"))
st.write("**Difficulty:**", pose_data.get("difficulty", "—"))
st.write("**Benefits:**", pose_data.get("benefits", "—"))

# ---------------- CAMERA NOTE ----------------
st.markdown("### 📷 Live Posture Correction")
st.warning(
    "Camera-based posture correction using OpenCV & MediaPipe "
    "is available in the local version of this project."
)


