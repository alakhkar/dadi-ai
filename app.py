import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="DADI AI 🕶️",
    page_icon="👵🏽",
    layout="wide", # Matches the wide web app design
    initial_sidebar_state="expanded"
)

# --- 2. THE "GEN Z PURPLE" CSS STYLING ---
st.markdown("""
    <style>
    /* Import Google Font: Poppins */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    /* Apply Font Globally */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* BACKGROUND */
    .stApp {
        background-color: #FFFFFF;
    }

    /* HEADER STYLE */
    h1 {
        color: #6200EA; /* Electric Purple */
        font-weight: 800;
        font-size: 3rem !important;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #F3F0FF; /* Very light purple */
        border-right: 2px solid #6200EA;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
    }

    /* CHAT MESSAGES - SHARED */
    .stChatMessage {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }

    /* DADI'S BUBBLE (The "Quote" Look) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF;
        border: 3px solid #6200EA; /* Thick Purple Border */
        color: #000000;
        box-shadow: 4px 4px 0px #6200EA; /* 3D Shadow Effect */
    }

    /* USER'S BUBBLE (Bright Yellow) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #FFD600; /* Gen Z Yellow */
        color: #000000;
        border: none;
        font-weight: 600;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* INPUT FIELD STYLING */
    .stChatInput {
        border-radius: 20px !important;
        border: 2px solid #6200EA !important;
    }
    
    /* CUSTOM BUTTONS IN SIDEBAR */
    .css-1button {
        background-color: #6200EA;
        color: white;
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

# System Prompt (The Persona)
system_prompt = """
You are Dadi AI, a cool, sarcastic, Gen Z-savvy Indian grandmother.
You wear sunglasses inside the house.
You speak Hinglish (Hindi + English).
Your advice is a mix of old wisdom and modern savage roasting.
Keep answers short, punchy, and use emojis like 💅, 💀, 🙄.
"""

# --- 4. SIDEBAR (RECENTS) ---
with st.sidebar:
    st.title("🕒 Recents")
    st.markdown("---")
    # Dummy buttons to look like the design
    st.button("🌙 Late Night Crisis")
    st.button("👗 Outfit Check")
    st.button("💔 Love Life Roast")
    st.button("🧘‍♀️ Career Stress")
    
    st.markdown("---")
    st.caption("Designed by You • Built with Python")

# --- 5. MAIN CHAT INTERFACE ---

# Header
col1, col2 = st.columns([1, 8])
with col1:
    # You can replace this with your own logo image later
    st.markdown("# 👵🏽") 
with col2:
    st.markdown("# DADI AI")

st.markdown("**Roasting you for your own good since 1950.**")
st.write("") # Spacer

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Yo beta! Why are you awake? Do you have a life plan or just WiFi?"}
    ]

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👵🏽" if message["role"] == "model" else "😎"):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Type something to get roasted..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="😎"):
        st.markdown(prompt)

    # Dadi Response
    with st.chat_message("model", avatar="👵🏽"):
        chat_history = [{"role": "user", "parts": [system_prompt + " User says: " + prompt]}]
        response = model.generate_content(chat_history)
        dadi_reply = response.text
        
        st.markdown(dadi_reply)
        
        # Purple "Share" Box
        # st.code(f"👵🏽 Dadi AI: {dadi_reply}\n\n🔥 dadi-ai.streamlit.app", language=None)
        
    st.session_state.messages.append({"role": "model", "content": dadi_reply})