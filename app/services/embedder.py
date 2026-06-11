# app/services/embedder.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def get_embedding(text: str) -> list[float]:
    client = _get_client()
    result = client.models.embed_content(
        model="models/text-embedding-004",   # must include "models/" prefix
        contents=text,
    )
    return result.embeddings[0].values