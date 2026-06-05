import json

from app.database import SessionLocal
from app.models import KnowledgeBase
from app.services.embedder import get_embedding

db = SessionLocal()

with open(
    "dataset.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

inserted = 0

for item in data:

    existing = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.topic ==
        item["topic"]
    ).first()

    if existing:
        continue

    text = f"""
    {item["topic"]}
    {item["concept"]}
    {item["explanation"]}
    {item["example"]}
    """

    embedding = get_embedding(
        text
    )

    row = KnowledgeBase(
        topic=item["topic"],
        class_level=item["class_level"],
        concept=item["concept"],
        explanation=item["explanation"],
        example=item["example"],
        embedding=json.dumps(
            embedding
        )
    )

    db.add(row)

    inserted += 1

db.commit()

print(
    f"{inserted} rows inserted successfully."
)