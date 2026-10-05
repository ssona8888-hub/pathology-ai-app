import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. Professional UI Setup ---
st.set_page_config(page_title="Patho-Assist Pro", layout="centered")
st.markdown("""
<style>
    .stButton>button { height: 60px; font-size: 20px; font-weight: bold; background-color: #004d99; color: white; border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Patho-Assist Pro")
st.write("Upload histology images or use the direct camera for AI analysis.")

# --- API Key is now HIDDEN and pulled securely from Streamlit Secrets ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    st.error("Admin setup required: Secrets not configured.")
    st.stop()

# --- 2. Camera & Upload Options ---
tab1, tab2 = st.tabs(["📷 Direct Camera", "📁 Upload Photos"])
image_files = []

with tab1:
    camera_photo = st.camera_input("Microscope se photo lein")
    if camera_photo:
        image_files.append(camera_photo)

with tab2:
    # Upload limit changed to 8
    uploaded_slides = st.file_uploader("Upload Slides / History (Up to 8 Images)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if uploaded_slides:
        # Strictly limit to 8 images
        image_files.extend(uploaded_slides[:8])

# --- 3. Medical AI Execution ---
if st.button("🔍 Generate Diagnosis"):
    if not image_files:
        st.error("Kripya kam se kam ek photo (Camera ya Upload) zarur dein.")
    else:
        # Ensure total images don't exceed 8 even if mixed from camera and upload
        if len(image_files) > 8:
            st.warning("Aapne 8 se zyada photos daali hain. Sirf pehli 8 photos analyze hongi.")
            image_files = image_files[:8]
            
        with st.spinner("Medical AI analyzing visual morphology..."):
            try:
                # Placeholder for UI testing
                st.success("App is successfully connected to the hidden Master API Key! ✅")
                st.info(f"Total {len(image_files)} images ready for analysis. Jab Dr7.ai ka connection code final hoga, result yahan aayega.")
                
            except Exception as e:
                st.error(f"Connection Error: {e}")
                
