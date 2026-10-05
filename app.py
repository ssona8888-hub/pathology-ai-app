import streamlit as st

# --- 1. UI SETUP ---
st.set_page_config(page_title="Patho-Assist", layout="centered")

st.markdown("""
<style>
    /* 1. Force columns to stay side-by-side on mobile screens */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 10px !important;
    }
    
    div[data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 50% !important;
        padding: 0 !important;
    }

    /* 2. Hide extra text and empty space in File Uploader */
    div[data-testid="stFileUploadDropzone"] {
        padding: 5px !important;
    }
    div[data-testid="stFileUploadDropzone"] > div > div > span,
    div[data-testid="stFileUploadDropzone"] > div > div > small {
        display: none !important;
    }

    /* 3. Make Analyze button huge and easy to press */
    .stButton>button { 
        height: 60px; 
        font-size: 20px; 
        font-weight: bold; 
        background-color: #004d99; 
        color: white; 
        border-radius: 8px; 
        width: 100%; 
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Patho-Assist")

# --- Hidden API Setup ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    pass

# ==========================================
# SECTION 1: PATIENT HISTORY
# ==========================================
st.markdown("### 📝 1. Patient History")
col1, col2 = st.columns(2)
history_file = None

with col1:
    hist_cam = st.camera_input("Camera", key="h_cam", label_visibility="collapsed")
    if hist_cam: history_file = hist_cam
with col2:
    hist_up = st.file_uploader("Upload", type=['png','jpg','jpeg'], key="h_up", label_visibility="collapsed")
    if hist_up: history_file = hist_up


# ==========================================
# SECTION 2: MICROSCOPIC SLIDES
# ==========================================
st.markdown("### 🔬 2. Microscopic Slides")
slide_type = st.radio("Type:", ["Histopathology", "Cytopathology"], horizontal=True, label_visibility="collapsed")

col3, col4 = st.columns(2)
slide_files = []

with col3:
    slide_cam = st.camera_input("Camera", key="s_cam", label_visibility="collapsed")
    if slide_cam: slide_files.append(slide_cam)
with col4:
    slide_up = st.file_uploader("Upload", type=['png','jpg','jpeg'], accept_multiple_files=True, key="s_up", label_visibility="collapsed")
    if slide_up: slide_files.extend(slide_up[:8])


# ==========================================
# SECTION 3: ANALYZE BUTTON
# ==========================================
if st.button("🔍 Analyze Now"):
    if len(slide_files) > 8:
        slide_files = slide_files[:8]
        
    if not history_file:
        st.warning("⚠️ Kripya Patient History upload karein.")
    elif not slide_files:
        st.warning("⚠️ Kripya kam se kam ek Slide photo dein.")
    else:
        with st.spinner(f"AI is analyzing {slide_type}..."):
            st.success("App UI is Ready! The Camera and Upload are now permanently side-by-side. ✅")
            
