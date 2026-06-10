
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/text-embedding-004"  # free, fast, 768-dim


def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector using Gemini text-embedding-004.
    Returns a list of floats (768 dimensions).
    """
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]