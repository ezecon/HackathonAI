# app/services/embedder.py

model = None


def get_model():
    """
    Lazy load SentenceTransformer model.
    Prevents FastAPI startup crash on Render.
    """

    global model

    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def get_embedding(text: str):
    """
    Generate embedding vector for text.
    """

    loaded_model = get_model()

    vector = loaded_model.encode(text)

    return vector.tolist()