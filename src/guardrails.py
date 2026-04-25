import re

DANGEROUS_PATTERNS = [
    r'os\\.system', r'subprocess\\.', r'eval\\(', r'exec\\(',
    r'__import__', r'open\\(.*[\'\"]w[\'\"]', r'rm ', r'del '
]

def is_safe(code: str) -> tuple[bool, str]:
    """
    Returns (safe, reason_if_not). Checks code for dangerous patterns.
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False, f"Blocked by guardrail: pattern '{pattern}' detected."
    if len(code) > 5000:
        return False, "Code too long."
    return True, ""
