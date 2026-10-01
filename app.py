import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.set_page_config(page_title="Parking Space Detection", page_icon="🚗", layout="wide")


@st.cache_resource
def load_model():
    # Relative path: best.pt must sit next to app.py in the GitHub repo
    return YOLO("best.pt")


# Class-name keywords used to group detections (case-insensitive)
EMPTY_WORDS = ("empty", "free", "vacant", "available")
OCCUPIED_WORDS = ("occupied", "busy", "taken", "car")


def group_of(name: str) -> str:
    n = name.lower()
    if any(w in n for w in EMPTY_WORDS):
        return "empty"
    if any(w in n for w in OCCUPIED_WORDS):
        return "occupied"
    return "other"


st.title("🚗 Parking Space Detection")
st.write("Upload a parking image to detect empty and occupied parking spaces.")

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load best.pt. Make sure it is in the same folder as app.py.\n\n{e}")
    st.stop()

confidence = st.slider("Confidence threshold", 0.05, 0.95, 0.25, 0.05)

uploaded_file = st.file_uploader("Upload a parking image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    left, right = st.columns(2)
    with left:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with st.spinner("Detecting..."):
        result = model.predict(image, conf=confidence, verbose=False)[0]
        annotated = result.plot()[:, :, ::-1]  # BGR -> RGB

    with right:
        st.subheader("Detection Result")
        st.image(annotated, use_container_width=True)

    # Count detections per class
    counts = {"empty": 0, "occupied": 0, "other": 0}
    per_class = {}
    for cls_id in result.boxes.cls.tolist():
        name = model.names[int(cls_id)]
        counts[group_of(name)] += 1
        per_class[name] = per_class.get(name, 0) + 1

    st.subheader("Detection Counts")
    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 Empty spaces", counts["empty"])
    c2.metric("🔴 Occupied spaces", counts["occupied"])
    c3.metric("Total detections", len(result.boxes))

    if per_class:
        st.write("Per-class breakdown:", per_class)
    else:
        st.info("No objects detected. Try lowering the confidence threshold.")

    st.caption(f"Model classes: {list(model.names.values())}")
