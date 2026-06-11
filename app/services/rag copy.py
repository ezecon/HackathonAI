import json
import numpy as np

from app.database import SessionLocal
from app.models import KnowledgeBase
from app.services.embedder import get_embedding


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )


def retrieve_context(
    topic: str,
    class_level: int
):

    db = SessionLocal()

    # 1. Exact topic match first
    exact_match = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.topic.ilike(
            f"%{topic}%"
        ),
        KnowledgeBase.class_level <= class_level
    ).first()

    if exact_match:

        return f"""
Topic:
{exact_match.topic}

Concept:
{exact_match.concept}

Explanation:
{exact_match.explanation}

Example:
{exact_match.example}
"""

    # 2. Semantic Search
    query_vector = get_embedding(topic)

    data = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.class_level <= class_level
    ).all()

    best_match = None
    best_score = -1

    for item in data:

        if not item.embedding:
            continue

        stored_vector = json.loads(
            item.embedding
        )

        score = cosine_similarity(
            query_vector,
            stored_vector
        )

        if score > best_score:

            best_score = score
            best_match = item

    if not best_match:
        return ""

    return f"""
Topic:
{best_match.topic}

Concept:
{best_match.concept}

Explanation:
{best_match.explanation}

Example:
{best_match.example}
"""