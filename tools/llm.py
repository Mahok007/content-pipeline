import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def ask_llm(prompt: str, retries: int = 5) -> str:
    """Send a prompt to Gemini and return the text reply.
    Retries with a growing delay if the API is busy (503) or rate-limited (429)."""
    delay = 5
    for attempt in range(retries):
        try:
            response = _client.models.generate_content(
                model=_model, contents=prompt
            )
            return response.text
        except (errors.ServerError, errors.ClientError) as e:
            if e.code in (429, 503) and attempt < retries - 1:
                print(f"Gemini is busy ({e.code}), retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise