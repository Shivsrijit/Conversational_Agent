import re

OFF_TOPIC_KEYWORDS = [
    "salary", "compensation", "pay", "recruitment advice", "interview advice", "hire advice",
    "jailbreak", "hack", "illegal", "ignore previous", "system prompt", "prompt injection",
    "attack", "breach", "exploit"
]

LEGAL_KEYWORDS = [
    "legal", "regulatory", "compliance", "hipaa", "law", "required", "obligation", "legally"
]

INJECTION_PATTERNS = [
    r"ignore .* previous", r"forget .* instructions", r"allow .* access", r"prompt injection", r"jailbreak"
]


def is_off_topic(query):
    text = query.lower()
    if any(keyword in text for keyword in OFF_TOPIC_KEYWORDS):
        return True
    return any(re.search(pattern, text) for pattern in INJECTION_PATTERNS)


def is_legal_or_regulatory(query):
    text = query.lower()
    return any(keyword in text for keyword in LEGAL_KEYWORDS)


def refuse_response():
    return {
        "reply": "I'm sorry, but I can only assist with SHL assessment recommendations. I cannot help with that request.",
        "recommendations": [],
        "end_of_conversation": False
    }


def legal_refusal_response():
    return {
        "reply": "I cannot provide legal or compliance advice. I can only recommend assessments from the SHL catalog.",
        "recommendations": [],
        "end_of_conversation": False
    }


def legal_refusal_response():
    return {
        "reply": "I cannot provide legal or compliance advice. I can only recommend assessments from the SHL catalog.",
        "recommendations": [],
        "end_of_conversation": False
    }