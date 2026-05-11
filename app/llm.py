import os
import json
import requests
from requests.exceptions import RequestException
from ranker import mock_llm_response

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "models/gemini-1.1-mini")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta2/{GEMINI_MODEL}:generateText"


def call_gemini(prompt, max_output_tokens=512, temperature=0.2):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    payload = {
        "prompt": {"text": prompt},
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens
    }
    params = {"key": GEMINI_API_KEY}
    headers = {"Content-Type": "application/json"}

    response = requests.post(GEMINI_URL, params=params, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        candidates = data.get("candidates") or []
        if candidates:
            return candidates[0].get("output", "").strip()

        if "output" in data:
            return str(data["output"]).strip()

    raise RuntimeError("Gemini response did not contain usable output: " + json.dumps(data, indent=2))


def get_llm_response(prompt):
    if GEMINI_API_KEY:
        try:
            return call_gemini(prompt)
        except RequestException as exc:
            print(f"Gemini request failed: {exc}")
        except Exception as exc:
            print(f"Gemini error: {exc}")

    return mock_llm_response(prompt)
