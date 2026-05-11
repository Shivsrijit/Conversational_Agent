import json

SYSTEM_PROMPT = """
You are an SHL assessment recommendation assistant.

Rules:
- Recommend ONLY assessments from the provided catalog.
- Never invent assessments, report names, or URLs.
- Ask clarifying questions if information is insufficient.
- Support refinement, comparison, and leadership assessment scenarios.
- Keep responses concise and directly relevant.
- If the user has provided enough detail, provide a clear recommendation.
"""

def generate_prompt(context, retrieved_items, user_query):
    prompt = SYSTEM_PROMPT + "\n\n"
    
    if context:
        prompt += f"Context from conversation: {json.dumps(context)}\n\n"
    
    prompt += f"User query: {user_query}\n\n"
    
    if retrieved_items:
        prompt += "Retrieved catalog entries:\n"
        for item in retrieved_items[:10]:  # Limit to top 10
            prompt += f"- Name: {item['item']['name']}\n"
            prompt += f"  Description: {item['item']['description'][:200]}...\n"
            prompt += f"  Keys: {', '.join(item['item']['keys'])}\n"
            prompt += f"  Job Levels: {', '.join(item['item']['job_levels'])}\n"
            prompt += f"  URL: {item['item']['link']}\n\n"
    
    prompt += "Respond with a helpful recommendation or a single clarifying question if you need more information."
    
    return prompt