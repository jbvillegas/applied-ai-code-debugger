import difflib
from .debugger import request_fix
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def score_confidence(original_code: str, fixed_code: str, error: str, test_result: dict) -> float:
    # Heuristic: if tests pass, base 0.9, else 0.4
    base = 0.9 if test_result.get("success") else 0.4
    # Similarity: if very similar, lower confidence
    similarity = difflib.SequenceMatcher(None, original_code, fixed_code).ratio()
    if similarity > 0.95:
        base -= 0.2
    # LLM self-rating
    llm_prompt = f"Rate 0-1 how confident you are that this fix works.\nOriginal code:\n{original_code}\nFixed code:\n{fixed_code}\nError was: {error}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": llm_prompt}],
        max_tokens=10,
        temperature=0.0
    )
    text = response.choices[0].message['content']
    try:
        llm_score = float([s for s in text.split() if s.replace('.', '', 1).isdigit()][0])
    except Exception:
        llm_score = 0.5
    return round((base + llm_score) / 2, 2)
