import streamlit as st
import numpy as np
import cv2
from PIL import Image
from pyzbar.pyzbar import decode

# ---------------- UI ----------------
st.set_page_config(page_title="SKINIQ AI", layout="wide")

texts = {
    "BG": {
        "title": "✨ SKINIQ AI",
        "upload": "Качи снимка на лице",
        "analyze": "Анализирай",
        "skin_type": "Тип кожа",
        "routine": "Препоръчана рутина",
        "barcode": "Скенер за продукт"
    },
    "EN": {
        "title": "✨ SKINIQ AI",
        "upload": "Upload face photo",
        "analyze": "Analyze",
        "skin_type": "Skin type",
        "routine": "Recommended routine",
        "barcode": "Product scanner"
    }
}

lang = st.sidebar.selectbox("Language", ["BG", "EN"])
t = texts[lang]

city = st.sidebar.text_input("Location", "Sofia")
st.sidebar.info(f"☀️ SPF recommendation for {city}: SPF 30-50")

st.title(t["title"])

tab1, tab2 = st.tabs([t["skin_type"], t["barcode"]])

# ---------------- SKIN ANALYSIS ----------------
def analyze_skin(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    texture = np.std(gray)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    redness = np.mean(cv2.absdiff(gray, blur))

    if texture < 30:
        skin_type = "dry / sensitive"
    elif texture < 60:
        skin_type = "normal"
    else:
        skin_type = "oily / visible pores"

    return skin_type, texture, redness


def get_routine(skin):
    routines = {
        "dry / sensitive": ["Gentle cleanser", "Hyaluronic acid", "SPF"],
        "normal": ["Balanced cleanser", "Vitamin C serum", "SPF"],
        "oily / visible pores": ["Gel cleanser", "Niacinamide", "SPF"]
    }
    return routines.get(skin, routines["normal"])


# ---------------- TAB 1 (SKIN) ----------------
with tab1:
    file = st.file_uploader(t["upload"], type=["jpg", "png"])

    if file:
        image = Image.open(file)
        st.image(image, width=250)

        if st.button(t["analyze"]):
            img = np.array(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            skin, texture, redness = analyze_skin(img)

            st.success("Analysis complete")

            st.write("🔹", t["skin_type"], ":", skin)
            st.write("🔹 Texture:", round(texture, 2))
            st.write("🔹 Redness:", round(redness, 2))

            st.subheader(t["routine"])
            st.write(get_routine(skin))


# ---------------- TAB 2 (BARCODE) ----------------
with tab2:
    file2 = st.file_uploader("Scan product barcode", type=["jpg", "png"])

    if file2:
        img = Image.open(file2)
        st.image(img, width=200)

        data = decode(np.array(img))

        if data:
            code = data[0].data.decode("utf-8")
            st.success(f"Barcode: {code}")
        else:
            st.warning("Barcode not detected")
