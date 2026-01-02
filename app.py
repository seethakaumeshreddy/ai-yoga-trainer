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

# ---------------- FUNCTION (MUST BE FIRST) ----------------
def get_pose_image(pose_name):
    url = "https://en.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "AI-Yoga-Trainer/1.0 (educational project)"
    }

    try:
        # Search Wikipedia
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": pose_name + " yoga",
            "srlimit": 1
        }

        search_response = requests.get(
            url, params=search_params, headers=headers, timeout=10
        )

        if not search_response.headers.get("Content-Type", "").startswith("application/json"):
            return None

        search_data = search_response.json()
        results = search_data.get("query", {}).get("search", [])

        if not results:
            return None

        page_title = results[0]["title"]

        # Get image from page
        image_params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "titles": page_title,
            "piprop": "thumbnail",
            "pithumbsize": 700
        }

        image_response = requests.get(
            url, params=image_params, headers=headers, timeout=10
        )

        if not image_response.headers.get("Content-Type", "").startswith("application/json"):
            return None

        image_data = image_response.json()
        pages = image_data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "thumbnail" in page:
                return page["thumbnail"]["source"]

    except Exception:
        return None

    return None


# ---------------- LOAD POSES ----------------
with open("poses.json", "r", encoding="utf-8") as f:
    POSES = json.load(f)

pose_list = list(POSES.keys())

# ---------------- SELECT POSE ----------------
selected_pose = st.selectbox("Select Yoga Pose", pose_list)
pose_data = POSES[selected_pose]

# ---------------- IMAGE DISPLAY ----------------
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
