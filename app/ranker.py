from models import Recommendation

PERSONALITY_KEYS = ["Personality", "Behavior", "Motivation"]
ABILITY_KEYS = ["Ability", "Aptitude", "Reasoning"]
SIMULATION_KEYS = ["Simulation", "Situational Judgment", "Assessment Exercises"]


def determine_test_type(keys):
    if any(personality_key in key for key in keys for personality_key in PERSONALITY_KEYS):
        return "P"
    if any(ability_key in key for key in keys for ability_key in ABILITY_KEYS):
        return "A"
    if any(sim_key in key for key in keys for sim_key in SIMULATION_KEYS):
        return "S"
    return "K"


def rank_and_filter(results, context):
    ranked = sorted(results, key=lambda x: x['score'], reverse=True)
    filtered = []
    languages = [lang.lower() for lang in context.get("language", [])]

    for item in ranked:
        assessment = item['item']
        keys = assessment.get('keys', [])
        job_levels = [level.lower() for level in assessment.get('job_levels', [])]

        if context.get("exclude_personality") and any(personality in key for personality in PERSONALITY_KEYS for key in keys):
            continue

        if languages and assessment.get('languages'):
            item_languages = [lang.lower() for lang in assessment['languages'] if lang]
            if not any(lang in item_languages for lang in languages):
                continue

        if context.get("role") == "leadership":
            if not any(personality in key for personality in PERSONALITY_KEYS for key in keys):
                continue

        if context.get("include_simulation") and not any(sim_key in key for sim_key in SIMULATION_KEYS for key in keys):
            continue

        if context.get("include_cognitive") and not any(ability in key for ability in ABILITY_KEYS for key in keys):
            continue

        filtered.append(assessment)
        if len(filtered) >= 10:
            break

    return filtered


def generate_recommendations(catalog_items):
    recommendations = []
    for item in catalog_items[:10]:
        rec = Recommendation(
            name=item['name'],
            test_type=determine_test_type(item.get('keys', [])),
            keys=item.get('keys', []),
            duration=item.get('duration', 'Variable'),
            languages=item.get('languages', []),
            url=item['link']
        )
        recommendations.append(rec)
    return recommendations


def find_catalog_items_by_name(query, catalog):
    normalized_query = query.lower()
    found = []
    for item in catalog:
        name = item['name'].lower()
        if name in normalized_query:
            found.append(item)
    if len(found) < 2:
        for item in catalog:
            name = item['name'].lower()
            tokens = [token for token in name.split() if len(token) > 4]
            if any(token in normalized_query for token in tokens):
                if item not in found:
                    found.append(item)
            if len(found) >= 3:
                break
    return found[:3]


def compare_catalog_items(query, catalog):
    candidates = find_catalog_items_by_name(query, catalog)
    if len(candidates) < 2:
        return None

    comparisons = []
    for item in candidates:
        keys = ", ".join(item.get('keys', [])) or "Not specified"
        duration = item.get('duration') or "Not specified"
        languages = ", ".join(item.get('languages', [])) or "Not specified"
        comparisons.append(f"{item['name']} focuses on {keys}; duration {duration}; languages {languages}.")

    return "Here is how those catalog items differ: " + " ".join(comparisons)
