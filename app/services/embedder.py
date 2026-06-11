# app/services/embedder.py

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"),
            http_options=types.HttpOptions(api_version="v1")
        )
    return _client


def get_embedding(text: str):
    client = _get_client()
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values
