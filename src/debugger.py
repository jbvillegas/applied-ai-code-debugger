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

def request_fix(code: str, error: str, attempt_num: int, previous_attempts: list = None) -> str:
    history_section = ""
    if previous_attempts and attempt_num > 1:
        for i, att in enumerate(previous_attempts, 1):
            history_section += f"\nAttempt {i}:\nCode:\n{att['proposed_fix']}\nError:\n{att['error_after_fix']}\n"
    prompt = PROMPT_TEMPLATE.format(code=code, error=error, history_section=history_section)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.2
    )
    # Extract code only
    text = response.choices[0].message['content']
    # Try to extract code block if present
    if '```' in text:
        code_block = text.split('```')[1]
        if code_block.startswith('python'):
            code_block = code_block[len('python'):].strip()
        return code_block.strip()
    return text.strip()
