from app.services.recommendation_engine import (
    generate_recommendation
)

from app.services.ai_engine import (
    generate_remediation_content
)


def generate_remediation(
    user_id,
    topic,
    score,
    environment,
    class_level
):

    # ==========================
    # Recommendation
    # ==========================
    recommendation = generate_recommendation(
        user_id,
        class_level
    )

    # ==========================
    # AI Remediation Content
    # ==========================
    remediation_content = (
        generate_remediation_content(
            user_id=user_id,
            topic=topic,
            environment=environment,
            class_level=class_level
        )
    )

    # ==========================
    # Final Response
    # ==========================
    return {
        "topic": topic,
        "misconception": "Ratio Interpretation Error",
        "recommendation": recommendation,
        "remediation_content": remediation_content
    }