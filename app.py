from dotenv import load_dotenv
load_dotenv()  # Load all the env variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Gemini Flash model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from Gemini
def get_gemini_response(user_input, image, prompt):
    response = model.generate_content([user_input, image, prompt])
    return response.text

# ---------------- UI Setup ---------------- #
st.set_page_config(page_title="Gemini Invoice Extractor", page_icon="🧾", layout="centered")

# Custom styled title
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: 700;
            color: #ff4b4b;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #888;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.5em;
        }
    </style>
    <div class="title">🚀 Multi Language Invoice Extractor</div>
    <div class="subtitle">Upload an invoice in any language and ask anything about it using Gemini</div>
""", unsafe_allow_html=True)

# ---------------- User Input ---------------- #
input_text = st.text_input("💬 Ask something about the invoice:", key="input")

uploaded_file = st.file_uploader("📤 Upload an invoice image (JPG, JPEG, PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Uploaded Invoice", use_column_width=True)

    submit = st.button("🧠 Analyze Invoice")

    input_prompt = """ 
    You are an expert in understanding invoices. The uploaded image is an invoice.
    Answer the user's questions based on the contents of the invoice image.
    """

    if submit:
        with st.spinner("Analyzing the invoice... 💭"):
            response = get_gemini_response(input_text, image, input_prompt)
            st.success("✅ Response Generated!")

            st.markdown("### 🧾 Gemini Response:")
            st.write(response)
else:
    st.info("Please upload an invoice image to get started.")
