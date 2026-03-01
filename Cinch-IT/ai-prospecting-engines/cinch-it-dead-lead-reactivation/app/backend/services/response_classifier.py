"""
AI-powered response classification.
When a lead replies to our outreach, classify their intent.
"""

import json
from typing import Dict
from openai import OpenAI
from config import get_settings

settings = get_settings()

CLASSIFICATION_PROMPT = """You are classifying email/SMS replies from business contacts who received outreach from an IT services company (Cinch IT).

Classify the reply into EXACTLY ONE of these categories:
- INTERESTED: They want to learn more, schedule a meeting, or are open to a conversation
- NOT_INTERESTED: They explicitly decline, say no thanks, or are not interested
- WRONG_PERSON: They say they're not the right contact, or no longer at the company
- OUT_OF_OFFICE: Auto-reply, vacation, or away message
- UNSUBSCRIBE: They want to be removed from the list, say stop, or request no more contact
- UNKNOWN: Can't determine intent

Also extract:
- sentiment: positive, neutral, negative
- urgency: high (wants to talk now), medium (interested but not urgent), low (polite decline), none
- suggested_action: what should the sales team do next

Reply in JSON format only:
{
    "classification": "INTERESTED|NOT_INTERESTED|WRONG_PERSON|OUT_OF_OFFICE|UNSUBSCRIBE|UNKNOWN",
    "sentiment": "positive|neutral|negative",
    "urgency": "high|medium|low|none",
    "suggested_action": "brief recommendation",
    "confidence": 0.0-1.0
}"""


def classify_response(reply_text: str, original_subject: str = "", 
                      contact_name: str = "", company: str = "") -> Dict:
    """
    Classify an inbound reply using OpenAI.
    Returns classification dict.
    """
    if not settings.openai_api_key:
        return {
            "classification": "UNKNOWN",
            "sentiment": "neutral",
            "urgency": "none",
            "suggested_action": "Manual review needed — no AI key configured",
            "confidence": 0.0,
        }

    try:
        client = OpenAI(api_key=settings.openai_api_key)

        context = f"Contact: {contact_name} at {company}\n"
        if original_subject:
            context += f"Original email subject: {original_subject}\n"
        context += f"\nTheir reply:\n{reply_text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast + cheap for classification
            messages=[
                {"role": "system", "content": CLASSIFICATION_PROMPT},
                {"role": "user", "content": context},
            ],
            temperature=0.1,
            max_tokens=200,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        return {
            "classification": "UNKNOWN",
            "sentiment": "neutral",
            "urgency": "none",
            "suggested_action": f"Manual review needed — AI error: {str(e)}",
            "confidence": 0.0,
        }
