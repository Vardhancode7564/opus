"""AI Suggestion Generator - Uses Groq LLM to generate project improvement suggestions."""

import requests
import logging
import json

from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_suggestions(student_idea, similar_projects):
    """
    Use Groq LLM to generate improvement suggestions for a student project idea
    based on similar existing projects.
    """
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY is not set. Please add it to your .env file to enable AI suggestions."

    # Build context from similar projects
    similar_context = ""
    for i, proj in enumerate(similar_projects[:5], 1):
        similar_context += (
            f"{i}. {proj.get('project_title', 'N/A')} "
            f"(Similarity: {proj.get('similarity_score', 'N/A')})\n"
            f"   Description: {proj.get('description', 'N/A')}\n"
            f"   Technologies: {proj.get('technologies', 'N/A')}\n\n"
        )

    prompt = f"""You are an academic project advisor. A student has proposed the following project idea:

**Project Title:** {student_idea.get('title', '')}
**Project Description:** {student_idea.get('description', '')}
**Domain:** {student_idea.get('domain', '')}

Here are existing similar projects found in our database:

{similar_context}

Based on this information, provide exactly 3 specific and actionable suggestions to improve or differentiate this project. Each suggestion should:
1. Be innovative and technically feasible for a student
2. Build upon the existing idea rather than replacing it
3. Address a gap not covered by the similar projects

Format your response as:
**Suggestion 1: [Title]**
[2-3 sentence description]

**Suggestion 2: [Title]**
[2-3 sentence description]

**Suggestion 3: [Title]**
[2-3 sentence description]
"""

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful academic project advisor who provides concise, actionable improvement suggestions for student projects.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 800,
        }

        resp = requests.post(
            GROQ_API_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()

        return data["choices"][0]["message"]["content"]

    except requests.RequestException as e:
        logger.error(f"Groq API error: {e}")
        return f"⚠️ Error generating suggestions: {e}"
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected Groq response format: {e}")
        return "⚠️ Error parsing AI response. Please try again."
