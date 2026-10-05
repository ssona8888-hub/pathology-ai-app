import streamlit as st
import requests
import base64
from PIL import Image
import io

# --- 1. SUPER SIMPLE UI SETUP ---
st.set_page_config(page_title="Patho-Assist", layout="centered")

# Styling for Big, Easy Buttons (like WhatsApp)
st.markdown("""
<style>
    /* Main Analyze Button */
    .stButton>button { 
        height: 70px; 
        font-size: 24px; 
        font-weight: bold; 
        background-color: #004d99; 
        color: white; 
        border-radius: 12px; 
        width: 100%; 
        margin-top: 20px;
    }
    
    /* Make headers bigger */
    h3 { font-size: 26px !important; color: #333; margin-bottom: 5px; }
    
    /* Small text instruction */
    .instruct { font-size: 16px; color: #666; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Patho-Assist")
st.markdown("<div class='instruct'>Upload photos for AI Analysis. Fast & Simple.</div>", unsafe_allow_html=True)

# --- API Key (Hidden) ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    st.error("Setup Error. Contact Admin.")
    st.stop()

# ==========================================
# SECTION 1: PATIENT HISTORY
# ==========================================
st.markdown("### 📝 1. Patient History")
st.markdown("<div class='instruct'>Take a photo of the form or upload from gallery.</div>", unsafe_allow_html=True)

# Create two columns for buttons side-by-side
col1, col2 = st.columns(2)
history_file = None

with col1:
    hist_cam = st.camera_input("📷 Camera", key="hist_cam")
    if hist_cam: history_file = hist_cam

with col2:
    hist_up = st.file_uploader("⬆️ Upload (Gallery)", type=['png', 'jpg', 'jpeg'], key="hist_up")
    if hist_up: history_file = hist_up


st.markdown("---") # Divider line

# ==========================================
# SECTION 2: MICROSCOPIC SLIDES
# ==========================================
st.markdown("### 🔬 2. Microscopic Slides")
st.markdown("<div class='instruct'>Select type, then take up to 8 photos.</div>", unsafe_allow_html=True)

slide_type = st.radio("Slide Type:", ["Histopathology", "Cytopathology"], horizontal=True)

col3, col4 = st.columns(2)
slide_files = []

with col3:
    slide_cam = st.camera_input("📷 Camera", key="slide_cam")
    if slide_cam: slide_files.append(slide_cam)

with col4:
    slide_up = st.file_uploader("⬆️️ Upload (Gallery)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="slide_up")
    if slide_up: slide_files.extend(slide_up[:8])


st.markdown("---") # Divider line

# ==========================================
# SECTION 3: ANALYZE BUTTON
# ==========================================
if st.button("🔍 Analyze Now"):
    # Limit check
    if len(slide_files) > 8:
        slide_files = slide_files[:8]
        
    # Validation checks
    if not history_file:
        st.warning("⚠️ Please provide Patient History first.")
    elif not slide_files:
        st.warning("⚠️ Please provide at least one Slide Photo.")
    else:
        # Smart Warning for less than 5 images
        if len(slide_files) < 5:
            st.info("💡 Tip: For best results, use 5 or more slide photos. (Analyzing now...)")
            
        with st.spinner(f"AI is analyzing {slide_type}... Please wait."):
            try:
                # Placeholder UI testing confirmation
                st.success("App UI is Ready and Super Simple! ✅")
                st.info(f"Received: History + {len(slide_files)} Slides. Ready for Dr7.ai API.")
                
            except Exception as e:
                st.error(f"Error: {e}")
                
