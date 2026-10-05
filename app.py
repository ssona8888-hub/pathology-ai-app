import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. UI SETUP (WhatsApp-like Design) ---
st.set_page_config(page_title="Patho-Assist", layout="centered")

st.markdown("""
<style>
    div[data-testid="stFileUploadDropzone"] > div > div > span,
    div[data-testid="stFileUploadDropzone"] > div > div > small {
        display: none !important;
    }
    
    div[data-testid="stFileUploadDropzone"] {
        padding: 0px !important;
        min-height: 55px !important;
        border-radius: 30px !important;
        background-color: #f0f2f6;
        border: 1px solid #ccc !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    div[data-testid="stFileUploadDropzone"] button {
        width: 100%;
        height: 100%;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important; 
        position: relative;
    }
    
    div[data-testid="stFileUploadDropzone"] button::after {
        content: "📷 Camera   /   📎 Gallery";
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        color: #333 !important;
        font-size: 16px !important;
        font-weight: bold;
        visibility: visible;
    }

    .stButton>button { 
        height: 60px; 
        font-size: 20px; 
        font-weight: bold; 
        background-color: #004d99; 
        color: white; 
        border-radius: 30px; 
        width: 100%; 
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Patho-Assist")

# --- Hidden API Setup for Gemini ---
try:
    # Use GEMINI_API_KEY from secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using Gemini 1.5 Pro for better image recognition
    model = genai.GenerativeModel('gemini-1.5-pro') 
except Exception as e:
    st.error("⚠️ Setup Error: Kripya Streamlit Secrets mein apni GEMINI_API_KEY set karein.")
    st.stop()

# ==========================================
# SECTION 1: PATIENT HISTORY
# ==========================================
st.markdown("### 📝 1. Patient History")
history_file = st.file_uploader("Upload History", type=['png','jpg','jpeg'], key="h_up", label_visibility="collapsed")

# ==========================================
# SECTION 2: MICROSCOPIC SLIDES
# ==========================================
st.markdown("### 🔬 2. Microscopic Slides")
slide_type = st.radio("Type:", ["Histopathology", "Cytopathology"], horizontal=True, label_visibility="collapsed")
slide_files = st.file_uploader("Upload Slides", type=['png','jpg','jpeg'], accept_multiple_files=True, key="s_up", label_visibility="collapsed")

# ==========================================
# SECTION 3: ANALYZE BUTTON (GEMINI FREE API)
# ==========================================
if st.button("🔍 Generate Diagnosis"):
    slide_list = slide_files if slide_files else []
    
    if len(slide_list) > 8:
        slide_list = slide_list[:8]
        
    if not history_file:
        st.warning("⚠️ Kripya Patient History ki photo dein.")
    elif not slide_list:
        st.warning("⚠️ Kripya kam se kam ek Slide photo dein.")
    else:
        with st.spinner(f"Free AI (Gemini) is analyzing {slide_type}... Please wait."):
            try:
                # Prepare images for Gemini
                image_parts = []
                
                # Open History Image
                hist_img = Image.open(history_file)
                image_parts.append(hist_img)
                
                # Open Slide Images
                for slide in slide_list:
                    slide_img = Image.open(slide)
                    image_parts.append(slide_img)
                
                # Medical Prompt
                prompt = f"You are a Pathology Assistant. Carefully analyze these uploaded images (The first image is the Patient History, and the following are {slide_type} microscopic slides). Describe the morphology and provide a precise differential diagnosis based on visible evidence."
                
                # Send to Gemini
                response = model.generate_content([prompt] + image_parts)
                
                st.success("✅ Analysis Complete")
                st.markdown("### 📑 AI Diagnostic Report")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"API Error: {e}")
                
