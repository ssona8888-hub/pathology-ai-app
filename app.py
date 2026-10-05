import streamlit as st

# --- 1. UI SETUP ---
st.set_page_config(page_title="Patho-Assist", layout="centered")

st.markdown("""
<style>
    /* 1. Hide the huge drag-and-drop box texts completely */
    div[data-testid="stFileUploadDropzone"] > div > div > span,
    div[data-testid="stFileUploadDropzone"] > div > div > small {
        display: none !important;
    }
    
    /* 2. Make the uploader box super thin and WhatsApp-like (Pill shape) */
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
    
    /* 3. Change "Browse files" text to our custom WhatsApp-like Icons */
    div[data-testid="stFileUploadDropzone"] button {
        width: 100%;
        height: 100%;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important; /* Hide original text */
        position: relative;
    }
    
    /* Custom Text and Icons inside the button */
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

    /* 4. Large Generate Diagnosis Button */
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

# --- Hidden API Setup ---
try:
    API_KEY = st.secrets["MEDICAL_API_KEY"]
except:
    pass

# ==========================================
# SECTION 1: PATIENT HISTORY
# ==========================================
st.markdown("### 📝 1. Patient History")
history_file = st.file_uploader("Upload", type=['png','jpg','jpeg'], key="h_up", label_visibility="collapsed")

# ==========================================
# SECTION 2: MICROSCOPIC SLIDES
# ==========================================
st.markdown("### 🔬 2. Microscopic Slides")
slide_type = st.radio("Type:", ["Histopathology", "Cytopathology"], horizontal=True, label_visibility="collapsed")

# Accept up to 8 multiple files
slide_files = st.file_uploader("Upload", type=['png','jpg','jpeg'], accept_multiple_files=True, key="s_up", label_visibility="collapsed")

# ==========================================
# SECTION 3: ANALYZE BUTTON
# ==========================================
if st.button("🔍 Generate Diagnosis"):
    # Ensure slide_files is a list even if empty
    slide_list = slide_files if slide_files else []
    
    if len(slide_list) > 8:
        slide_list = slide_list[:8]
        
    if not history_file:
        st.warning("⚠️ Kripya Patient History ki photo dein.")
    elif not slide_list:
        st.warning("⚠️ Kripya kam se kam ek Slide photo dein.")
    else:
        with st.spinner(f"AI is analyzing {slide_type}..."):
            st.success("App UI is Perfect! Koi right-slide nahi, sirf WhatsApp jaisa simple icon button! ✅")
            
