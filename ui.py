import streamlit as st
import time
import random

# --- PAGE CONFIGURATION (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="Dadi AI",
    page_icon="👵",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/alakhkar/dadi-ai',
        'Report a bug': "https://github.com/alakhkar/dadi-ai/issues",
        'About': "# Dadi AI\nYour personal health and lifestyle assistant."
    }
)

# --- CUSTOM CSS FOR POLISHED UI ---
# This injects custom CSS to hide the default header, style the chat, 
# and make the interface look professional and responsive.
def load_custom_css():
    st.markdown("""
        <style>
        /* Import a warm, professional font */
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&display=swap');

        /* GENERAL SETTINGS */
        .stApp {
            background-color: #fcfbf9; /* Warm off-white background */
            font-family: 'Inter', sans-serif;
        }
        
        /* HIDE STREAMLIT BRANDING */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* CUSTOM HEADER */
        .header-container {
            padding: 1rem 2rem;
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            margin-top: -60px; /* Pull up to cover default padding */
            margin-bottom: 2rem;
            text-align: center;
        }
        .header-title {
            font-family: 'Lora', serif;
            color: #4a3b32;
            font-size: 2.5rem;
            font-weight: 600;
            margin: 0;
        }
        .header-subtitle {
            font-size: 1rem;
            color: #8c7b70;
            margin-top: 0.5rem;
        }

        /* CHAT BUBBLE STYLING */
        .stChatMessage {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        /* User Message (Right aligned visually via Streamlit defaults, tweaked here) */
        .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #f0f2f6; 
        }

        /* Dadi Message (Warm accent) */
        .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
            background-color: #fff8f0;
            border: 1px solid #fae1d2;
        }
        
        /* AVATARS */
        .stChatMessage .st-emotion-cache-1p1nwyz {
            width: 45px;
            height: 45px;
            border-radius: 50%;
        }

        /* INPUT FIELD STYLING */
        .stChatInput {
            border-radius: 20px;
            border: 1px solid #d1d5db;
        }

        /* MOBILE RESPONSIVENESS */
        @media (max-width: 768px) {
            .header-title { font-size: 1.8rem; }
            .stChatMessage { padding: 0.8rem; }
        }
        </style>
    """, unsafe_allow_html=True)

# --- MOCK BACKEND LOGIC ---
# Replace this function with your actual model call (e.g., OpenAI/Gemini API)
def get_dadi_response(user_input):
    """
    Simulates Dadi's response with a slight delay for realism.
    """
    # Simple keyword-based responses for the demo
    responses = [
        "Oh beta, have you eaten properly today? Health is wealth!",
        "Let me think... Grandma suggests drinking some turmeric milk for that.",
        "Don't worry too much, everything happens for a reason. Take a deep breath.",
        "In my time, we used to treat this with simple home remedies.",
        "That sounds lovely! Tell me more about it."
    ]
    return random.choice(responses)

# --- MAIN APP UI ---
def run():
    load_custom_css()

    # Custom Header
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">Dadi AI 👵</h1>
            <p class="header-subtitle">Your wise companion for health and life advice</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Session State for Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Namaste beta! I am your Dadi. How are you feeling today?"}
        ]

    # Display Chat History
    # We use a container to keep the chat area distinct
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            # Choose avatar based on role
            avatar = "👵" if message["role"] == "assistant" else "🧑‍💻"
            
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Chat Input Area
    if prompt := st.chat_input("Ask Dadi for advice..."):
        # 1. Add User Message to History
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Display User Message Immediately
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # 3. Generate and Display Assistant Response
        with st.chat_message("assistant", avatar="👵"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulate "thinking" with a spinner
            with st.spinner("Dadi is thinking..."):
                time.sleep(1) # Simulate network delay
                response_text = get_dadi_response(prompt)
                
                # Stream the response like a real LLM
                for chunk in response_text.split():
                    full_response += chunk + " "
                    time.sleep(0.05) # Typewriter effect
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
        
        # 4. Add Assistant Message to History
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Sidebar for Reset/Options
    with st.sidebar:
        st.header("Settings")
        st.info("This is a demo of the Dadi-AI interface.")
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
if __name__ == "__main__":
    run()