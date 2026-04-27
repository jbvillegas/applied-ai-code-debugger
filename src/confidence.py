
import difflib
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

import re
from typing import Optional

def score_confidence(
    original_code: str,
    fixed_code: str,
    error: str,
    test_result: dict,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.0,
    similarity_threshold: float = 0.95,
    use_llm: bool = True,
    llm_timeout: int = 10
) -> float:
    """
    Compute a confidence score for a code fix based on test results, code similarity, and (optionally) LLM self-rating.
    - If tests pass, base = 0.9, else 0.4
    - If code is very similar, lower confidence
    - Optionally, ask LLM to self-rate confidence (0-1)
    Args:
        original_code: The original buggy code.
        fixed_code: The fixed code.
        error: The error message from the last run.
        test_result: Dict with test results (must have 'success').
        model: LLM model to use for self-rating.
        temperature: LLM temperature.
        similarity_threshold: Similarity above which to penalize confidence.
        use_llm: If False, skip LLM self-rating.
        llm_timeout: Timeout for LLM call (not enforced, for future use).
    Returns:
        Confidence score between 0 and 1.
    """
    # Import here to avoid circular import
    from src.debugger import request_fix
    base = 0.9 if test_result.get("success") else 0.4
    similarity = difflib.SequenceMatcher(None, original_code, fixed_code).ratio()
    if similarity > similarity_threshold:
        base -= 0.2
    llm_score = 0.5
    if use_llm:
        llm_prompt = (
            f"Rate 0-1 how confident you are that this fix works.\n"
            f"Original code:\n{original_code}\nFixed code:\n{fixed_code}\nError was: {error}"
        )
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": llm_prompt}],
                max_tokens=10,
                temperature=temperature
            )
            text = response.choices[0].message['content']
            # Use regex to extract a float between 0 and 1
            match = re.search(r"([01](?:\.\d+)?|0?\.\d+)", text)
            if match:
                llm_score = float(match.group(1))
                if llm_score > 1.0:
                    llm_score = 1.0
                elif llm_score < 0.0:
                    llm_score = 0.0
            else:
                llm_score = 0.5
        except Exception as e:
            # Optionally log e
            llm_score = 0.5
    score = (base + llm_score) / 2
    # Ensure score is between 0 and 1
    score = max(0.0, min(1.0, score))
    return round(score, 2)
