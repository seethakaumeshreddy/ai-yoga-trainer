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

def get_pose_image(pose_name):
    search_url = "https://en.wikipedia.org/w/api.php"

    # STEP 1: SEARCH PAGE
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": pose_name + " yoga",
        "srlimit": 1
    }

    search_res = requests.get(search_url, params=search_params, timeout=10).json()
    search_results = search_res.get("query", {}).get("search", [])

    if not search_results:
        return None

    page_title = search_results[0]["title"]

    # STEP 2: FETCH IMAGE FROM PAGE
    image_params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": page_title,
        "piprop": "thumbnail",
        "pithumbsize": 700
    }

    image_res = requests.get(search_url, params=image_params, timeout=10).json()
    pages = image_res.get("query", {}).get("pages", {})

    for page in pages.values():
        if "thumbnail" in page:
            return page["thumbnail"]["source"]

    return None


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

