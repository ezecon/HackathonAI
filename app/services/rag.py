# app/services/rag.py
import json
import numpy as np

from app.database import SessionLocal
from app.models import KnowledgeBase
from app.services.embedder import get_embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0
    return np.dot(a, b) / norm


def retrieve_context(topic: str, class_level: int):
    db = SessionLocal()

    try:
        # 1. Exact topic match first (no API call needed)
        exact_match = db.query(KnowledgeBase).filter(
            KnowledgeBase.topic.ilike(f"%{topic}%"),
            KnowledgeBase.class_level <= class_level
        ).first()

        if exact_match:
            return f"""Topic:
{exact_match.topic}

Concept:
{exact_match.concept}

Explanation:
{exact_match.explanation}

Example:
{exact_match.example}"""

        # 2. Semantic search — only if exact match failed
        try:
            query_vector = get_embedding(topic)
        except Exception as e:
            print(f"Embedding unavailable (quota?): {e}")
            # Fall back gracefully — AI will use its own knowledge
            return ""

        # Only compare rows that already have embeddings seeded
        data = db.query(KnowledgeBase).filter(
            KnowledgeBase.class_level <= class_level,
            KnowledgeBase.embedding.isnot(None)
        ).all()

        best_match = None
        best_score = -1

        for item in data:
            try:
                stored_vector = json.loads(item.embedding)
                # Skip rows with wrong dimension (old 384-dim vectors)
                if len(stored_vector) != len(query_vector):
                    continue
                score = cosine_similarity(query_vector, stored_vector)
                if score > best_score:
                    best_score = score
                    best_match = item
            except Exception:
                continue

        if not best_match:
            return ""

        return f"""Topic:
{best_match.topic}

Concept:
{best_match.concept}

Explanation:
{best_match.explanation}

Example:
{best_match.example}"""

    finally:
        db.close()