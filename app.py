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

# --- API Key is now HIDDEN and pulled securely from Streamlit Secrets ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    st.error("Admin setup required: Secrets not configured.")
    st.stop()

# --- 2. Box 1: Patient History ---
st.markdown("### 📝 1. Patient History (1 Image)")
hist_tab1, hist_tab2 = st.tabs(["📷 Direct Camera", "📁 Upload Photo"])
history_file = None

with hist_tab1:
    hist_cam = st.camera_input("History ki photo lein", key="hist_cam")
    if hist_cam: 
        history_file = hist_cam

with hist_tab2:
    hist_up = st.file_uploader("Upload History Note", type=['png', 'jpg', 'jpeg'], key="hist_up")
    if hist_up: 
        history_file = hist_up

# --- 3. Box 2: Microscopic Slides ---
st.markdown("### 🔬 2. Microscopic Slides (Up to 8 Images)")
slide_type = st.radio("Select Slide Type:", ["Histopathology", "Cytopathology"], horizontal=True)

slide_tab1, slide_tab2 = st.tabs(["📷 Direct Camera", "📁 Upload Photos"])
slide_files = []

with slide_tab1:
    slide_cam = st.camera_input("Microscope se photo lein", key="slide_cam")
    if slide_cam: 
        slide_files.append(slide_cam)

with slide_tab2:
    slide_up = st.file_uploader("Upload Slides", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="slide_up")
    if slide_up:
        slide_files.extend(slide_up[:8])

# --- 4. Medical AI Execution ---
if st.button("🔍 Generate Diagnosis"):
    # Limit check
    if len(slide_files) > 8:
        st.warning("Aapne 8 se zyada photos daali hain. Sirf pehli 8 photos analyze hongi.")
        slide_files = slide_files[:8]
        
    # Validation checks
    if not history_file:
        st.error("Kripya Patient History ki photo zaroor daalein.")
    elif not slide_files:
        st.error("Kripya kam se kam ek Microscopic Slide ki photo zaroor daalein.")
    else:
        # Smart Warning for less than 5 images
        if len(slide_files) < 5:
            st.warning("⚠️ Smart Warning: Optimal accuracy ke liye kam se kam 5 alag-alag fields ki photos zaroori hain. (Analysis continue ho raha hai...)")
            
        with st.spinner(f"Medical AI analyzing {slide_type} morphology..."):
            try:
                # Placeholder UI testing confirmation
                st.success("App UI bilkul ready hai! ✅ (Master API Key se connected)")
                st.info(f"Target: {slide_type}. Total {len(slide_files)} slide images + History received. Jab endpoint final hoga, result yahan dikhega.")
                
            except Exception as e:
                st.error(f"Connection Error: {e}")
                
