import os
import google.generativeai as genai

from dotenv import load_dotenv

from app.services.rag import retrieve_context
from app.services.memory_retriever import get_user_memory
from app.services.mastery_engine import calculate_mastery_score

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

import json


def generate_remediation_content(
    user_id,
    topic,
    environment,
    class_level
):

    # ==========================
    # RAG
    # ==========================
    knowledge = retrieve_context(
        topic,
        class_level
    )

    if knowledge:

        if isinstance(knowledge, str):

            rag_context = f"""
Topic: {topic}

Knowledge:
{knowledge}
"""

        else:

            rag_context = f"""
Topic: {topic}

Concept:
{getattr(knowledge, "concept", "")}

Explanation:
{getattr(knowledge, "explanation", "")}

Example:
{getattr(knowledge, "example", "")}
"""

    else:

        rag_context = "No matching knowledge found."

    # ==========================
    # MEMORY
    # ==========================
    memory = get_user_memory(user_id)

    preferred_environment = environment
    weak_topics = ""
    strong_topics = ""
    last_topic = "Unknown"

    if memory:

        preferred_environment = (
            memory.get("preferred_environment")
            or environment
        )

        weak_topics = memory.get(
            "weak_topics",
            ""
        )

        strong_topics = memory.get(
            "strong_topics",
            ""
        )

        last_topic = memory.get(
            "last_topic",
            "Unknown"
        )

    # ==========================
    # MASTERY SCORE
    # ==========================
    mastery = calculate_mastery_score(
        user_id
    )

    mastery_score = mastery[
        "mastery_score"
    ]

    mastery_level = mastery[
        "level"
    ]

    # ==========================
    # ADAPTIVE DIFFICULTY
    # ==========================
    if mastery_score < 40:

        difficulty_hint = """
Difficulty: EASY
- very simple explanation
- beginner friendly
"""

    elif mastery_score < 75:

        difficulty_hint = """
Difficulty: MEDIUM
- standard level
"""

    else:

        difficulty_hint = """
Difficulty: HARD
- slightly challenging
"""

    # ==========================
    # FINAL PROMPT
    # ==========================
    prompt = f"""
You are an expert mathematics teacher.

Generate SHORT remediation content.

=================================
USER MEMORY
=================================

Preferred Environment:
{preferred_environment}

Weak Topics:
{weak_topics}

Strong Topics:
{strong_topics}

Last Topic:
{last_topic}

Mastery Score:
{mastery_score}

Mastery Level:
{mastery_level}

=================================
KNOWLEDGE BASE (RAG)
=================================

{rag_context}

=================================
CURRENT LESSON
=================================

Class Level:
{class_level}

Topic:
{topic}

Environment:
{preferred_environment}

=================================
ADAPTIVE DIFFICULTY
=================================

{difficulty_hint}

=================================
INSTRUCTIONS
=================================

1. Explain concept clearly
2. Use RAG knowledge only
3. Class {class_level} level language
4. One real-life example
5. ONE word problem
6. Step-by-step solution
7. Keep curriculum aligned
8. Keep response SHORT and concise
9. Maximum 80 words per section
10. Return simple student-friendly language
11. step_by_step_solution must be short bullet points
12. Do NOT generate long paragraphs

=================================
IMPORTANT OUTPUT RULE
=================================

Return ONLY valid JSON.

Format:

{{
    "concept_explanation": "",
    "example": "",
    "word_problem": "",
    "answer": "",
    "step_by_step_solution": []
}}

Do not return markdown.
Do not return explanation outside JSON.
"""

    

    try:

        response = model.generate_content(
            prompt
        )

        cleaned_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(
            cleaned_text
        )

    except Exception as e:

        print("Gemini Error:", str(e))

        return {
            "concept_explanation":
                "AI service temporarily unavailable. Please try again in a few seconds.",
            "example": "",
            "word_problem": "",
            "answer": "",
            "step_by_step_solution": []
        }
    

def generate_learning_content(
    user_id,
    topic,
    environment,
    class_level
):

    # ==========================
    # RAG
    # ==========================
    knowledge = retrieve_context(
        topic,
        class_level
    )

    rag_context = ""

    if knowledge:

        # object support
        if hasattr(knowledge, "concept"):

            rag_context = f"""
Topic: {topic}

Concept:
{knowledge.concept}

Explanation:
{knowledge.explanation}

Example:
{knowledge.example}
"""

        # dict support
        elif isinstance(
            knowledge,
            dict
        ):

            rag_context = f"""
Topic: {topic}

Concept:
{knowledge.get('concept', '')}

Explanation:
{knowledge.get('explanation', '')}

Example:
{knowledge.get('example', '')}
"""

        # string support
        elif isinstance(
            knowledge,
            str
        ):

            rag_context = f"""
Topic: {topic}

Knowledge:
{knowledge}
"""

        else:

            rag_context = (
                "No matching knowledge found."
            )

    else:

        rag_context = (
            "No matching knowledge found."
        )

    # ==========================
    # MEMORY
    # ==========================
    memory = get_user_memory(
        user_id
    )

    preferred_environment = environment
    weak_topics = ""
    strong_topics = ""
    last_topic = "Unknown"

    if memory:

        preferred_environment = (
            memory.get(
                "preferred_environment"
            )
            or environment
        )

        weak_topics = memory.get(
            "weak_topics",
            ""
        )

        strong_topics = memory.get(
            "strong_topics",
            ""
        )

        last_topic = memory.get(
            "last_topic",
            "Unknown"
        )

    # ==========================
    # MASTERY SCORE
    # ==========================
    mastery = calculate_mastery_score(
        user_id
    )

    mastery_score = mastery[
        "mastery_score"
    ]

    mastery_level = mastery[
        "level"
    ]

    # ==========================
    # ADAPTIVE DIFFICULTY
    # ==========================
    if mastery_score < 40:

        difficulty_hint = """
Difficulty: EASY
- very simple numbers
- step-by-step explanation
- beginner friendly
"""

    elif mastery_score < 75:

        difficulty_hint = """
Difficulty: MEDIUM
- standard curriculum problems
- moderate reasoning
"""

    else:

        difficulty_hint = """
Difficulty: HARD
- multi-step reasoning
- challenge problems
"""

    # topic adjustment layer
    if topic.lower() in str(
        weak_topics
    ).lower():

        difficulty_hint += """
Student struggles in this topic:
- slow explanation
- extra hints
"""

    elif topic.lower() in str(
        strong_topics
    ).lower():

        difficulty_hint += """
Student is strong here:
- increase difficulty slightly
"""

    # ==========================
    # FINAL PROMPT
    # ==========================
    prompt = f"""
You are an expert mathematics teacher.

=================================
USER MEMORY
=================================

Preferred Environment:
{preferred_environment}

Weak Topics:
{weak_topics}

Strong Topics:
{strong_topics}

Last Topic:
{last_topic}

Mastery Score:
{mastery_score}

Mastery Level:
{mastery_level}

=================================
KNOWLEDGE BASE (RAG)
=================================

{rag_context}

=================================
CURRENT LESSON
=================================

Class Level:
{class_level}

Topic:
{topic}

Environment:
{preferred_environment}

=================================
ADAPTIVE DIFFICULTY
=================================

{difficulty_hint}

=================================
INSTRUCTIONS
=================================

1. Explain concept clearly
2. Use RAG knowledge only
3. Class {class_level} level language
4. One real-life example
5. ONE word problem
6. Step-by-step solution
7. Keep curriculum aligned

=================================
OUTPUT FORMAT
=================================

Concept Explanation:
...

Example:
...

Word Problem:
...

Answer:
...

Step-by-Step Solution:
...
"""

    response = model.generate_content(
        prompt
    )

    return response.text