import streamlit as st
import base64

# --- 1. SUPER SIMPLE UI SETUP ---
st.set_page_config(page_title="Patho-Assist", layout="centered")

# Styling for Compact Icons and Big Analyze Button
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
        margin-top: 30px;
    }
    
    /* Hide the huge default labels of file_uploader and camera_input */
    div[data-testid="stFileUploader"] label, div[data-testid="stCameraInput"] label {
        display: none;
    }
    
    /* Make headers slightly smaller for a single screen feel */
    h3 { font-size: 22px !important; color: #333; margin-bottom: 2px; }
    
    /* Small text instruction */
    .instruct { font-size: 14px; color: #666; margin-bottom: 5px; }

    /* Custom Box Styling to look like a single horizontal bar */
    .action-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-around; /* Distribute space evenly */
        border: 1px solid #dcdcdc;
    }
    
    /* Tweak internal columns to be tighter */
    div[data-testid="column"] {
        padding: 0 !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Patho-Assist")

# --- API Key (Hidden) ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    st.error("Setup Error. Contact Admin.")
    st.stop()


# Helper function to create the compact box layout
def create_action_box(title, instruction, key_prefix, is_multiple=False):
    st.markdown(f"### {title}")
    st.markdown(f"<div class='instruct'>{instruction}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='action-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    captured_file = None
    uploaded_files = None
    
    with col1:
        # Camera input (label hidden by CSS)
        cam = st.camera_input("Cam", key=f"{key_prefix}_cam")
        if cam: captured_file = cam
    with col2:
        # File uploader (label hidden by CSS)
        up = st.file_uploader("Up", type=['png', 'jpg', 'jpeg'], accept_multiple_files=is_multiple, key=f"{key_prefix}_up")
        if up: uploaded_files = up
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    return captured_file, uploaded_files

# ==========================================
# SECTION 1: PATIENT HISTORY
# ==========================================
hist_cam, hist_up = create_action_box("📝 1. Patient History", "Take a photo OR upload from gallery.", "hist")
history_file = hist_cam if hist_cam else hist_up

# ==========================================
# SECTION 2: MICROSCOPIC SLIDES
# ==========================================
slide_type = st.radio("Slide Type:", ["Histopathology", "Cytopathology"], horizontal=True)
slide_cam, slide_up = create_action_box("🔬 2. Microscopic Slides", "Take photos OR upload (Up to 8).", "slide", is_multiple=True)

slide_files = []
if slide_cam:
    slide_files.append(slide_cam)
if slide_up:
     # If it's a list (multiple files), extend it
    if isinstance(slide_up, list):
         slide_files.extend(slide_up)
    else:
        slide_files.append(slide_up)


# ==========================================
# SECTION 3: ANALYZE BUTTON
# ==========================================
if st.button("🔍 Analyze Now"):
    if len(slide_files) > 8:
        slide_files = slide_files[:8]
        
    if not history_file:
        st.warning("⚠️ Please provide Patient History first.")
    elif not slide_files:
        st.warning("⚠️ Please provide at least one Slide Photo.")
    else:
        if len(slide_files) < 5:
            st.info("💡 Tip: For best results, use 5 or more slide photos. (Analyzing now...)")
            
        with st.spinner(f"AI is analyzing {slide_type}... Please wait."):
            try:
                st.success("App UI is Ready! The Camera and Upload are now side-by-side. ✅")
                st.info(f"Received: History + {len(slide_files)} Slides. Ready for API.")
            except Exception as e:
                st.error(f"Error: {e}")
                
