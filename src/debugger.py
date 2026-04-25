import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

PROMPT_TEMPLATE = """
You are an expert Python debugger. Fix the code below.

ORIGINAL CODE:
{code}

ERROR ENCOUNTERED:
{error}
{history_section}
Provide ONLY the corrected code, no explanations. Use the same function/class names.
CORRECTED CODE:
"""

import re
import time
from typing import Optional

def request_fix(
    code: str,
    error: str,
    attempt_num: int,
    previous_attempts: Optional[list] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.2,
    max_tokens: int = 1500,
    system_prompt: Optional[str] = None,
    retries: int = 2,
    retry_delay: float = 2.0
) -> str:
    """
    Query the LLM to fix code given an error and history. Returns only the corrected code.
    Args:
        code: The code to fix.
        error: The error message.
        attempt_num: Current attempt number.
        previous_attempts: List of previous attempts (for context).
        model: LLM model to use.
        temperature: LLM temperature.
        max_tokens: Max tokens for LLM response.
        system_prompt: Optional system prompt for LLM.
        retries: Number of retries on failure.
        retry_delay: Seconds to wait between retries.
    Returns:
        The fixed code as a string (no explanations).
    """
    history_section = ""
    if previous_attempts and attempt_num > 1:
        for i, att in enumerate(previous_attempts, 1):
            history_section += f"\nAttempt {i}:\nCode:\n{att.get('proposed_fix','')}\nError:\n{att.get('error_after_fix','')}\n"
    prompt = PROMPT_TEMPLATE.format(code=code, error=error, history_section=history_section)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    last_exception = None
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            text = response.choices[0].message['content']
            # Robust code extraction: prefer code block, fallback to all text
            code_blocks = re.findall(r"```(?:python)?\s*([\s\S]+?)```", text)
            if code_blocks:
                # If multiple code blocks, return the first non-empty one
                for block in code_blocks:
                    block = block.strip()
                    if block:
                        return block
            # Fallback: try to find indented code
            lines = text.splitlines()
            code_lines = [line for line in lines if line.strip() and (line.startswith('    ') or line.startswith('\t'))]
            if code_lines:
                return '\n'.join(code_lines)
            # Otherwise, return all text
            return text.strip()
        except Exception as e:
            last_exception = e
            time.sleep(retry_delay)
    # If all retries fail, return an error message
    return f"# LLM request failed: {last_exception}"
