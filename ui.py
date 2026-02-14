import streamlit as st
from logic import DadiModel


CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F8F9FA;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .stChatMessage {
        background-color: transparent;
        border: none;
    }

    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #E5E7EB;
    }

    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #C9FFE5;
        color: Blue;
        border-radius: 20px 20px 5px 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.2);
    }

    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) p {
        color: Blue !important;
    }

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

    header {visibility: hidden;}
    </style>
"""


def run():
    st.set_page_config(
        page_title="DADI AI",
        page_icon="👵🏽",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.markdown(CSS, unsafe_allow_html=True)

    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API Key missing! Check .streamlit/secrets.toml")
        st.stop()

    model = DadiModel(api_key)

    col1, col2 = st.columns([1, 10])
    with col1:
        st.write("👵🏽")
    with col2:
        st.markdown("### Dadi AI")

    st.caption("Wisdom, modernized.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "content": "Beta, simplicity is the ultimate sophistication. What is troubling you?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=("👵🏽" if message["role"] == "model" else "🧑‍💻")):
            st.markdown(message["content"]) 

    if prompt := st.chat_input("Ask Dadi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        with st.chat_message("model", avatar="👵🏽"):
            response_text = model.generate(prompt)
            st.markdown(response_text)

        st.session_state.messages.append({"role": "model", "content": response_text})
