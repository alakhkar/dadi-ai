import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="DADI AI",
    page_icon="👵🏽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CLEAN & POLISHED CSS ---
st.markdown("""
    <style>
    /* Import Google Font: Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BACKGROUND */
    .stApp {
        background-color: #F8F9FA; /* Soft Gray-White */
    }

    /* REMOVE HEADER PADDING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* CHAT BUBBLES - SHARED */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }

    /* DADI'S BUBBLE (AI) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05); /* Soft Shadow */
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #E5E7EB;
    }

    /* USER'S BUBBLE (Human) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #2563EB; /* Professional Blue */
        color: Blue;
        border-radius: 20px 20px 5px 20px; /* Subtle shape styling */
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.2); /* Glow effect */
    }
    
    /* Text Color Fix for User Bubble */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) p {
        color: Blue !important;
    }

    /* INPUT FIELD - FLOATING STYLE */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 70% !important;
        z-index: 1000;
    }
    
    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.08) !important;
    }
    
    /* HIDE DEFAULT HEADER */
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 API Key missing! Check .streamlit/secrets.toml")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Persona
system_prompt = """
You are Dadi AI. A minimalist, wise, and slightly sarcastic Indian grandmother.
Keep answers short and elegant.
"""

# --- 4. UI HEADER ---
col1, col2 = st.columns([1, 10])
with col1:
    st.write("👵🏽") 
with col2:
    st.markdown("### Dadi AI")

st.caption("Wisdom, modernized.")

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Beta, simplicity is the ultimate sophistication. What is troubling you?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👵🏽" if message["role"] == "model" else "🧑‍💻"):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Dadi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("model", avatar="👵🏽"):
        chat_history = [{"role": "user", "parts": [system_prompt + " User says: " + prompt]}]
        response = model.generate_content(chat_history)
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "model", "content": response.text})