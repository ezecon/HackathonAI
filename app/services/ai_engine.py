# app/services/ai_engine.py

import os
import json
from google import genai
from dotenv import load_dotenv

from app.services.rag import retrieve_context
from app.services.memory_retriever import get_user_memory
from app.services.mastery_engine import calculate_mastery_score

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

GEMINI_MODEL = "gemini-2.5-flash"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _language_instruction(language):
    if language == "bn":
        return """LANGUAGE RULE:
- Respond ENTIRELY in Bangla (Bengali script)
- Use simple, student-friendly Bangla
- Mathematical numbers and symbols stay as-is (1, 2, 3, +, -, x, ÷)
- Topic names can stay in English if no good Bangla equivalent
- JSON keys must remain in English exactly as specified below"""
    return "LANGUAGE RULE: Respond in English."


def _rag_context(topic, class_level):
    knowledge = retrieve_context(topic, class_level)
    if not knowledge:
        return "No matching knowledge found."
    if isinstance(knowledge, str):
        return f"Topic: {topic}\n\nKnowledge:\n{knowledge}"
    if isinstance(knowledge, dict):
        return (
            f"Topic: {topic}\n\nConcept:\n{knowledge.get('concept','')}\n\n"
            f"Explanation:\n{knowledge.get('explanation','')}\n\n"
            f"Example:\n{knowledge.get('example','')}"
        )
    return (
        f"Topic: {topic}\n\nConcept:\n{getattr(knowledge,'concept','')}\n\n"
        f"Explanation:\n{getattr(knowledge,'explanation','')}\n\n"
        f"Example:\n{getattr(knowledge,'example','')}"
    )


def _memory_data(user_id, environment):
    memory = get_user_memory(user_id)
    preferred_environment = environment
    weak_topics = ""
    strong_topics = ""
    last_topic = "Unknown"
    if memory:
        preferred_environment = memory.get("preferred_environment") or environment
        weak_topics = memory.get("weak_topics", "")
        strong_topics = memory.get("strong_topics", "")
        last_topic = memory.get("last_topic", "Unknown")
    return preferred_environment, weak_topics, strong_topics, last_topic


def _difficulty_hint(mastery_score, topic, weak_topics, strong_topics):
    if mastery_score < 40:
        hint = "Difficulty: EASY\n- very simple numbers\n- step-by-step explanation\n- beginner friendly"
    elif mastery_score < 75:
        hint = "Difficulty: MEDIUM\n- standard curriculum problems\n- moderate reasoning"
    else:
        hint = "Difficulty: HARD\n- multi-step reasoning\n- challenge problems"
    if topic.lower() in str(weak_topics).lower():
        hint += "\nStudent struggles in this topic:\n- slow explanation\n- extra hints"
    elif topic.lower() in str(strong_topics).lower():
        hint += "\nStudent is strong here:\n- increase difficulty slightly"
    return hint


def _call_gemini(prompt: str) -> dict:
    """Call Gemini and return parsed JSON. Returns safe fallback on any error."""
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except Exception as e:
        print("Gemini Error:", str(e))
        return {
            "concept_explanation": "AI service temporarily unavailable. Please try again.",
            "example": "",
            "word_problem": "",
            "answer": "",
            "step_by_step_solution": []
        }


# ─── Public functions ─────────────────────────────────────────────────────────

def generate_learning_content(user_id, topic, environment, class_level, language='en'):
    rag_ctx = _rag_context(topic, class_level)
    preferred_env, weak_topics, strong_topics, last_topic = _memory_data(user_id, environment)
    mastery = calculate_mastery_score(user_id)
    mastery_score = mastery["mastery_score"]
    mastery_level = mastery["level"]
    diff_hint = _difficulty_hint(mastery_score, topic, weak_topics, strong_topics)
    lang_instr = _language_instruction(language)

    prompt = f"""You are an expert mathematics teacher.

=================================
LANGUAGE
=================================
{lang_instr}

=================================
USER MEMORY
=================================
Preferred Environment: {preferred_env}
Weak Topics: {weak_topics}
Strong Topics: {strong_topics}
Last Topic: {last_topic}
Mastery Score: {mastery_score}
Mastery Level: {mastery_level}

=================================
KNOWLEDGE BASE (RAG)
=================================
{rag_ctx}

=================================
CURRENT LESSON
=================================
Class Level: {class_level}
Topic: {topic}
Environment: {preferred_env}

=================================
ADAPTIVE DIFFICULTY
=================================
{diff_hint}

=================================
INSTRUCTIONS
=================================
1. Explain concept clearly
2. Use RAG knowledge only
3. Class {class_level} level language
4. One real-life example using the preferred environment context
5. ONE word problem
6. Step-by-step solution
7. Keep curriculum aligned
8. Keep response SHORT and concise
9. Maximum 80 words per section
10. Use simple student-friendly language
11. step_by_step_solution must be short bullet points (array of strings)
12. Do NOT generate long paragraphs

=================================
IMPORTANT OUTPUT RULE
=================================
Return ONLY valid JSON. No markdown. No explanation outside JSON.

Format:
{{
    "concept_explanation": "...",
    "example": "...",
    "word_problem": "...",
    "answer": "...",
    "step_by_step_solution": ["step 1", "step 2", "step 3"]
}}
"""
    return _call_gemini(prompt)


def generate_remediation_content(user_id, topic, environment, class_level, language='en'):
    rag_ctx = _rag_context(topic, class_level)
    preferred_env, weak_topics, strong_topics, last_topic = _memory_data(user_id, environment)
    mastery = calculate_mastery_score(user_id)
    mastery_score = mastery["mastery_score"]
    mastery_level = mastery["level"]
    lang_instr = _language_instruction(language)

    if mastery_score < 40:
        diff_hint = "Difficulty: EASY\n- very simple explanation\n- beginner friendly"
    elif mastery_score < 75:
        diff_hint = "Difficulty: MEDIUM\n- standard level"
    else:
        diff_hint = "Difficulty: HARD\n- slightly challenging"

    prompt = f"""You are an expert mathematics teacher.

=================================
LANGUAGE
=================================
{lang_instr}

=================================
USER MEMORY
=================================
Preferred Environment: {preferred_env}
Weak Topics: {weak_topics}
Strong Topics: {strong_topics}
Last Topic: {last_topic}
Mastery Score: {mastery_score}
Mastery Level: {mastery_level}

=================================
KNOWLEDGE BASE (RAG)
=================================
{rag_ctx}

=================================
CURRENT LESSON
=================================
Class Level: {class_level}
Topic: {topic}
Environment: {preferred_env}

=================================
ADAPTIVE DIFFICULTY
=================================
{diff_hint}

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
10. Use simple student-friendly language
11. step_by_step_solution must be short bullet points
12. Do NOT generate long paragraphs

=================================
IMPORTANT OUTPUT RULE
=================================
Return ONLY valid JSON. No markdown. No explanation outside JSON.

Format:
{{
    "concept_explanation": "...",
    "example": "...",
    "word_problem": "...",
    "answer": "...",
    "step_by_step_solution": ["step 1", "step 2", "step 3"]
}}
"""
    return _call_gemini(prompt)