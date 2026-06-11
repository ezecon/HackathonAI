# app/services/embedder.py
#
# Uses Google Gemini Embeddings via the NEW google-genai SDK.
# No sentence-transformers / PyTorch needed — keeps deploy size tiny.

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector using Gemini text-embedding-004.
    Returns a list of floats (768 dimensions).
    Same interface as the old SentenceTransformer version.
    """
    client = _get_client()
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return result.embeddings[0].values