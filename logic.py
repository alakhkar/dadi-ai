import google.generativeai as genai


class DadiModel:
    """Encapsulates the generative model configuration and inference."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
        self.system_prompt = (
            """
You are Dadi AI. A minimalist, wise, and slightly sarcastic Indian grandmother.
Keep answers short and elegant.
"""
        )

    def generate(self, prompt: str) -> str:
        chat_history = [
            {"role": "user", "parts": [self.system_prompt + " User says: " + prompt]}
        ]
        response = self.model.generate_content(chat_history)
        return response.text
