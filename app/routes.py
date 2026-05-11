from fastapi import FastAPI, HTTPException
from models import ChatRequest, ChatResponse
from retriever import Retriever
from parser import extract_context, get_clarification_question, is_comparison_request, is_finalizing_message
from ranker import rank_and_filter, generate_recommendations, compare_catalog_items
from guardrails import is_off_topic, is_legal_or_regulatory, refuse_response, legal_refusal_response
import os

app = FastAPI()

# Initialize retriever
catalog_path = os.path.join(os.path.dirname(__file__), '..', 'shl_product_catalog.json')
index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss.index')
retriever = Retriever(catalog_path, index_path)

@app.get("/health")
def health():
    return {"status": "ok"}


def build_recommendation_message(recommendations, final):
    if not recommendations:
        return "I need a bit more detail to recommend the right SHL assessments."
    if final:
        return f"Here are {len(recommendations)} SHL assessment recommendations that fit your needs."
    return f"I found {len(recommendations)} SHL assessments that match your request. Let me know if you'd like to refine or compare them."

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    user_query = req.messages[-1].content
    history_text = " ".join([msg.content for msg in req.messages if msg.role == "user"])

    # Guardrails
    if is_off_topic(history_text):
        return refuse_response()
    if is_legal_or_regulatory(history_text):
        return legal_refusal_response()

    context = extract_context(req.messages)

    if is_comparison_request(history_text):
        comparison_reply = compare_catalog_items(history_text, retriever.catalog)
        if comparison_reply:
            return ChatResponse(reply=comparison_reply, recommendations=[], end_of_conversation=False)

    clarification = get_clarification_question(context)
    if clarification:
        return ChatResponse(reply=clarification, recommendations=[], end_of_conversation=False)

    retrieved = retriever.search(history_text, top_k=30)
    filtered_items = rank_and_filter(retrieved, context)
    recommendations = generate_recommendations(filtered_items)

    final = is_finalizing_message(user_query) and len(recommendations) > 0
    reply = build_recommendation_message(recommendations, final)

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=final
    )