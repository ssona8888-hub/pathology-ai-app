import streamlit as st
import requests
import base64

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
        color: transparent !important; 
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
    st.error("Admin error: Please configure API Key in Secrets.")
    st.stop()

# --- HELPER FUNCTION: Convert images for API ---
def encode_image(upload_file):
    bytes_data = upload_file.getvalue()
    return base64.b64encode(bytes_data).decode('utf-8')

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
slide_files = st.file_uploader("Upload", type=['png','jpg','jpeg'], accept_multiple_files=True, key="s_up", label_visibility="collapsed")

# ==========================================
# SECTION 3: REAL API EXECUTION
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
        with st.spinner(f"AI is analyzing {slide_type}... Please wait."):
            try:
                # 1. Prepare images and prompt
                content_array = []
                
                # Instruction for the Medical AI
                prompt_text = f"You are a highly accurate Pathology Assistant. Carefully analyze these images (Patient History and {slide_type} slides). Objectively describe the morphology (cell architecture, stroma, nuclear features). Provide a precise differential diagnosis based ONLY on visible evidence, and suggest confirmatory IHC/special stains."
                content_array.append({"type": "text", "text": prompt_text})
                
                # Attach History
                content_array.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encode_image(history_file)}"}
                })
                
                # Attach Slides
                for slide in slide_list:
                    content_array.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encode_image(slide)}"}
                    })

                # 2. Setup the Dr7.ai Request 
                url = "https://dr7.ai/api/v1/medical/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
                payload = {
                    "model": "medgemma-4b-it", 
                    "messages": [{"role": "user", "content": content_array}],
                    "max_tokens": 1500
                }
                
                # 3. Send to Server
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis Complete")
                    st.markdown("### 📑 AI Diagnostic Report")
                    # Display the final AI text
                    st.write(result["choices"][0]["message"]["content"])
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")
                
