import re

ROLE_KEYWORDS = {
    "leadership": ["senior leadership", "leadership", "executive", "cxo", "director"],
    "graduate": ["graduate", "final-year", "management trainee", "intern", "trainee"],
    "contact center": ["contact centre", "contact center", "customer service", "call centre", "call center"],
    "product testing": ["product testing", "testing tool", "qa engineer", "software test"],
    "engineering": ["engineer", "software", "developer", "devops", "backend", "frontend", "full-stack"]
}

LANGUAGE_KEYWORDS = {
    "English": ["english", "en\b"],
    "Spanish": ["spanish", "es\b", "latam"],
    "French": ["french", "fr\b"]
}

CLARIFICATION_PROMPTS = {
    "role": "What type of role are you hiring for? For example, software engineer, contact centre agent, or graduate trainee.",
    "seniority": "What seniority level is the role (entry-level, mid-level, senior, leadership)?",
    "language": "Which candidate language or languages should the assessments support?"
}

COMPARISON_KEYWORDS = ["compare", "difference", "vs", "versus", "different from", "than"]
FINALIZING_KEYWORDS = ["perfect", "thanks", "thank you", "that works", "confirmed", "confirm", "good", "done", "lock it in", "finalise", "finalize"]


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_context(messages):
    context = {
        "role": None,
        "domain": None,
        "seniority": None,
        "skills": [],
        "language": [],
        "include_personality": False,
        "exclude_personality": False,
        "include_simulation": False,
        "include_cognitive": False,
        "comparison_request": False,
        "final_confirmation": False,
        "raw_text": ""
    }

    text = normalize_text(" ".join([msg.content for msg in messages if msg.role == "user"]))
    context["raw_text"] = text
    if not text:
        return context

    for role, keywords in ROLE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            context["role"] = role
            break

    if any(keyword in text for keyword in ["senior", "lead", "director", "executive", "cxo", "leadership"]):
        context["seniority"] = "senior"
    elif any(keyword in text for keyword in ["junior", "entry-level", "entry", "graduate", "new grad", "trainee"]):
        context["seniority"] = "junior"
    elif any(keyword in text for keyword in ["mid-level", "mid level", "mid"]):
        context["seniority"] = "mid"

    for language, keywords in LANGUAGE_KEYWORDS.items():
        if any(re.search(keyword, text) for keyword in keywords):
            if language not in context["language"]:
                context["language"].append(language)

    if any(keyword in text for keyword in ["personality", "behavior", "behavioral", "opq"]):
        context["include_personality"] = True
    if any(keyword in text for keyword in ["drop opq", "remove opq", "no opq", "without opq", "skip personality"]):
        context["exclude_personality"] = True

    if any(keyword in text for keyword in ["simulation", "situational", "scenario", "sj", "situational judgement"]):
        context["include_simulation"] = True
    if any(keyword in text for keyword in ["cognitive", "reasoning", "g+", "verify", "ability", "aptitude"]):
        context["include_cognitive"] = True

    if any(keyword in text for keyword in COMPARISON_KEYWORDS):
        context["comparison_request"] = True

    if any(keyword in text for keyword in FINALIZING_KEYWORDS):
        context["final_confirmation"] = True

    skills_keywords = ["java", "python", "javascript", "react", "node", "sql", "linux", "networking", "aws", "docker", "spring", "api", "sales", "customer", "healthcare", "accounting", "excel", "word"]
    for skill in skills_keywords:
        if skill in text and skill not in context["skills"]:
            context["skills"].append(skill)

    return context


def get_clarification_question(context):
    if not context["role"]:
        return CLARIFICATION_PROMPTS["role"]
    if not context["seniority"]:
        return CLARIFICATION_PROMPTS["seniority"]
    if not context["language"]:
        return CLARIFICATION_PROMPTS["language"]
    if context["role"] == "leadership" and not context["skills"]:
        return "For leadership assessment, what kind of leaders are you hiring for?"
    return None


def has_sufficient_info(context):
    return bool(context["role"] or context["skills"] or context["language"])


def is_comparison_request(text):
    normalized = normalize_text(text)
    return any(keyword in normalized for keyword in COMPARISON_KEYWORDS)


def is_finalizing_message(text):
    normalized = normalize_text(text)
    return any(keyword in normalized for keyword in FINALIZING_KEYWORDS)
