import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION (Viral Hook: Make it look good on mobile) ---
st.set_page_config(
    page_title="Dadi AI 👵🏽",
    page_icon="👵🏽",
    layout="centered"
)

# --- CSS FOR "DADI VIBES" ---
# This hides the default Streamlit header and adds a custom background feel
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF5E1;  /* Creamy chai color */
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #E0F7FA;
    }
    .chat-message.bot {
        background-color: #FFECB3;
        border: 2px solid #FFC107;
    }
    </style>
""", unsafe_allow_html=True)

# --- API SETUP ---
# In production, use st.secrets. For now, you can paste your key below for testing.
# BUT simpler for local test: Set it in terminal: export GEMINI_API_KEY="your_key"
api_key = st.secrets.get("GEMINI_API_KEY") 

if not api_key:
    st.error("Arre beta! Where is the API Key? Put it in .streamlit/secrets.toml")
    st.stop()

genai.configure(api_key=api_key)

# --- THE DADI PERSONA ---
model = genai.GenerativeModel('gemini-2.5-flash')

system_prompt = """
You are Dadi AI, a 75-year-old sarcastic Indian grandmother. 
Speak in Hinglish. Roast the user lovingly. 
Blame their phone for everything. 
Keep responses short and punchy so they can be screenshotted.
"""

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Arre beta! Finally you have time for your Dadi? Tell me, have you eaten?"}
    ]

# --- UI HEADER ---
st.title("👵🏽 Dadi AI")
st.caption("She judges you because she loves you.")

# --- DISPLAY CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👵🏽" if message["role"] == "model" else "🧑🏽"):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Ask Dadi for advice (at your own risk)..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑🏽"):
        st.markdown(prompt)

    # 2. Generate Dadi's response
    with st.chat_message("model", avatar="👵🏽"):
        # Construct the full prompt context
        chat_history = [
            {"role": "user", "parts": [system_prompt + " User says: " + prompt]}
        ]
        
        response = model.generate_content(chat_history)
        dadi_reply = response.text
        
        st.markdown(dadi_reply)
        
        # 3. VIRAL FEATURE: "Copy to Share" Button
        # We append a little signature to make it shareable
        share_text = f"👵🏽 Dadi AI says: {dadi_reply} \n\nGet roasted at: dadi-ai.streamlit.app"
        st.code(share_text, language=None)
        st.caption("👆 Copy this and put it on your WhatsApp Status!")

    # 4. Save history
    st.session_state.messages.append({"role": "model", "content": dadi_reply})