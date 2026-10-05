import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads GEMINI_API_KEY from .env

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def ask_llm(prompt: str) -> str:
    """Send a prompt to Gemini and return the text reply."""
    response = _client.models.generate_content(model=_model, contents=prompt)
    return response.text