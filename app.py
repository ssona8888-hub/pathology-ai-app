import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. UI Setup for 60+ Doctors ---
# Configures the page and uses custom CSS to make buttons massive and text large.
st.set_page_config(page_title="Pathology AI Assistant", layout="centered")
st.markdown("""
<style>
    .stButton>button { height: 80px; font-size: 24px; font-weight: bold; background-color: #0066cc; color: white; border-radius: 12px; width: 100%; }
    h1 { font-size: 40px; }
    h3 { font-size: 24px; }
    p { font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Pathology AI Assistant")
st.write("Upload histology images and the patient's clinical history note below.")

# --- 2. Secure API Key Input ---
api_key = st.text_input("Enter Gemini 3.1 Pro API Key:", type="password")

# --- 3. Simplified File Uploaders ---
st.markdown("### 📸 Upload Images")
history_img = st.file_uploader("1. Upload Handwritten History (1 Image)", type=['png', 'jpg', 'jpeg'])
slide_imgs = st.file_uploader("2. Upload Microscopic Slides (Up to 4 Images)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# --- 4. The System Prompt ---
SYSTEM_PROMPT = """
**Role:**
You are an expert Pathology Clinical Decision Support Assistant.

**Workflow:**
1. **Handwriting Check:** If the handwriting is illegible, stop and output ONLY: "⚠️ **Cannot read handwriting clearly.** Please type or dictate the patient history."
2. **Output Format:** If legible, output EXACTLY like this:

### 1. Patient History
* [Transcribed text]

### 2. Key Microscopic Findings
* [Bullet 1]
* [Bullet 2]

### 3. Top Diagnostic Considerations
1. **[Differential 1]**: [Why]
2. **[Differential 2]**: [Why]

### 4. Next Steps to Confirm
* [Specific IHC or special stains needed]
"""

# --- 5. Execution Logic ---
if st.button("🔍 Get Second Opinion"):
    if not api_key:
        st.error("Please enter your API Key first.")
    elif not history_img or not slide_imgs:
        st.error("Please upload both the history and at least one slide image.")
    else:
        with st.spinner("Analyzing images... Please wait."):
            try:
                # Initialize Gemini API
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )
                
                # Package images for the AI
                content = []
                content.append(Image.open(history_img))
                for slide in slide_imgs[:4]: # Strictly limit to 4 slides
                    content.append(Image.open(slide))
                content.append("Analyze these images according to your system instructions.")
                
                # Generate Diagnosis
                response = model.generate_content(content)
                
                # Display Results
                st.success("Analysis Complete")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
              
