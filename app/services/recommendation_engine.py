from app.services.misconception_engine import (
    get_user_misconceptions
)


def generate_recommendation(
    user_id: str,
    class_level: int
):

    misconceptions = get_user_misconceptions(
        user_id
    )

    if not misconceptions:

        return {
            "status": "good",
            "priority": "low",
            "class_level": class_level,
            "recommendation":
            "Continue normal learning path."
        }

    top_issue = misconceptions[0]

    topic = top_issue["topic"]

    misconception = top_issue["misconception"]

    return {

        "status":
        "needs_remediation",

        "priority":
        "high",

        "class_level":
        class_level,

        "topic":
        topic,

        "misconception":
        misconception,

        "recommendation":
        f"Student needs extra practice in {topic}",

        "next_action":
        f"Generate remediation lesson for {topic}"
    }