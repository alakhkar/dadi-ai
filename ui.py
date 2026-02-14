import streamlit as st
from logic import DadiModel


CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }

    /* Container padding - responsive */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 8rem;
        max-width: 900px;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    @media (min-width: 768px) {
        .block-container {
            padding-top: 2.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }

    /* Header styling */
    .dadi-header {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .dadi-header h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0;
    }

    .dadi-header p {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }

    @media (min-width: 768px) {
        .dadi-header {
            padding: 2rem;
        }
        
        .dadi-header h1 {
            font-size: 1.75rem;
        }
    }

    /* Hide Streamlit branding */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Chat messages container */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 1rem !important;
    }

    /* User messages (assistant messages are even in streamlit) */
    .stChatMessage[data-testid="stChatMessageContent"] {
        max-width: 100%;
    }

    /* Style user messages */
    div[data-testid="stChatMessage"]:has(img[alt="🧑‍💻"]) div[data-testid="stChatMessageContent"] {
        background: white;
        border-radius: 18px;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.06);
        color: #1a1a1a;
        margin-left: auto;
        max-width: 85%;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Style Dadi (AI) messages */
    div[data-testid="stChatMessage"]:has(img[alt="👵🏽"]) div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #c9ffe5 0%, #b8f5d8 100%);
        border-radius: 18px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 15px rgba(56, 189, 140, 0.15);
        border: 1px solid rgba(56, 189, 140, 0.2);
        color: #0a4d3c;
        max-width: 85%;
        font-size: 0.95rem;
        line-height: 1.6;
        font-weight: 400;
    }

    div[data-testid="stChatMessage"]:has(img[alt="👵🏽"]) div[data-testid="stChatMessageContent"] p {
        color: #0a4d3c !important;
        margin: 0;
    }

    @media (min-width: 768px) {
        div[data-testid="stChatMessage"]:has(img[alt="🧑‍💻"]) div[data-testid="stChatMessageContent"],
        div[data-testid="stChatMessage"]:has(img[alt="👵🏽"]) div[data-testid="stChatMessageContent"] {
            max-width: 75%;
            padding: 1.25rem 1.75rem;
            font-size: 1rem;
        }
    }

    /* Avatar styling */
    .stChatMessage img {
        width: 36px !important;
        height: 36px !important;
        border-radius: 50%;
        background: white;
        padding: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    @media (min-width: 768px) {
        .stChatMessage img {
            width: 40px !important;
            height: 40px !important;
        }
    }

    /* Chat input container - fixed at bottom */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: linear-gradient(to top, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.95) 70%, transparent 100%);
        backdrop-filter: blur(10px);
        z-index: 999;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    @media (min-width: 768px) {
        .stChatInput {
            padding: 1.5rem 2rem;
        }
    }

    /* Chat input field */
    .stChatInput > div {
        max-width: 900px;
        margin: 0 auto;
    }

    .stChatInput input {
        border-radius: 24px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.875rem 1.25rem !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.2s ease !important;
        background: white !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stChatInput input:focus {
        border-color: #38bd8c !important;
        box-shadow: 0 4px 24px rgba(56, 189, 140, 0.2) !important;
        outline: none !important;
    }

    .stChatInput input::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }

    @media (min-width: 768px) {
        .stChatInput input {
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
        }
    }

    /* Send button styling */
    button[kind="primary"] {
        background: linear-gradient(135deg, #38bd8c 0%, #2d9a6f 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 12px rgba(56, 189, 140, 0.3) !important;
    }

    button[kind="primary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 16px rgba(56, 189, 140, 0.4) !important;
    }

    button[kind="primary"]:active {
        transform: scale(0.98) !important;
    }

    /* Scrollbar styling for webkit browsers */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .stSpinner > div {
        border-color: #38bd8c transparent transparent transparent !important;
    }

    /* Mobile optimizations */
    @media (max-width: 767px) {
        .block-container {
            padding-bottom: 7rem;
        }
        
        div[data-testid="stChatMessage"]:has(img[alt="🧑‍💻"]) div[data-testid="stChatMessageContent"],
        div[data-testid="stChatMessage"]:has(img[alt="👵🏽"]) div[data-testid="stChatMessageContent"] {
            max-width: 90%;
        }
    }

    /* Smooth animations */
    .stChatMessage {
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Remove extra spacing */
    .element-container {
        margin: 0 !important;
    }

    /* Caption styling */
    .stCaption {
        font-size: 0.9rem !important;
        color: #64748b !important;
        font-weight: 400 !important;
    }
    </style>
"""


def run():
    st.set_page_config(
        page_title="DADI AI - Wisdom Modernized",
        page_icon="👵🏽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(CSS, unsafe_allow_html=True)

    # Get API key from secrets
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API Key missing! Please add GEMINI_API_KEY to .streamlit/secrets.toml")
        st.stop()

    # Initialize the model
    model = DadiModel(api_key)

    # Custom header
    st.markdown("""
        <div class="dadi-header">
            <div style="font-size: 2.5rem;">👵🏽</div>
            <div style="flex: 1;">
                <h1>Dadi AI</h1>
                <p>Wisdom, modernized.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "model", 
                "content": "Beta, simplicity is the ultimate sophistication. What is troubling you today?"
            }
        ]

    # Display chat messages
    for message in st.session_state.messages:
        avatar = "👵🏽" if message["role"] == "model" else "🧑‍💻"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask Dadi for wisdom..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.chat_message("model", avatar="👵🏽"):
            with st.spinner(""):
                response_text = model.generate(prompt)
                st.markdown(response_text)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "model", "content": response_text})