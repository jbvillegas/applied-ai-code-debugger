import re
import ast

# Expanded dangerous patterns (regex)
DANGEROUS_PATTERNS = [
    r'os\.system', r'subprocess\.', r'eval\(', r'exec\(', r'compile\(',
    r'__import__', r'open\(.*[\'\"]w[\'\"]', r'rm ', r'del ', r'socket\.', r'ftplib\.',
    r'shutil\.', r'pickle\.', r'input\(', r'globals\(', r'locals\(', r'setattr\(', r'getattr\(',
    r'__dict__', r'__class__', r'__globals__', r'__subclasses__', r'__mro__', r'__code__', r'__base__',
    r'Popen', r'fork', r'threading\.', r'multiprocessing\.', r'os\.environ', r'os\.walk', r'os\.remove',
    r'os\.rmdir', r'os\.unlink', r'os\.chmod', r'os\.chown', r'os\.chroot', r'os\.kill',
    r'sys\.exit', r'sys\.modules', r'sys\.path', r'sys\.argv', r'base64\.', r'binascii\.',
    r'ctypes\.', r'__file__', r'__loader__', r'__package__', r'__builtins__', r'\bimport\b', r'\bfrom\b'
]

# Configurable blocklist for modules
BLOCKED_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'shutil', 'ftplib', 'pickle', 'threading', 'multiprocessing',
    'ctypes', 'base64', 'binascii', 'resource', 'signal', 'inspect', 'importlib', 'builtins', 'tempfile',
    'glob', 'pathlib', 'concurrent', 'asyncio', 'selectors', 'ssl', 'http', 'urllib', 'xml', 'xmlrpc', 'faulthandler'
}

def _ast_guardrails(code: str) -> tuple[bool, str]:
    """
    Use AST to block dangerous nodes: Import, ImportFrom, Exec, Call to dangerous builtins, etc.
    """
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # Block import of dangerous modules
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] in BLOCKED_MODULES:
                        return False, f"Blocked by guardrail: import of '{alias.name}'"
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] in BLOCKED_MODULES:
                    return False, f"Blocked by guardrail: import from '{node.module}'"
            # Block exec, eval, compile, open, input, setattr, getattr, delattr, etc.
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in {'exec', 'eval', 'compile', 'open', 'input', 'setattr', 'getattr', 'delattr', 'globals', 'locals'}:
                        return False, f"Blocked by guardrail: call to '{node.func.id}'"
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in {'system', 'popen', 'fork', 'kill', 'remove', 'rmdir', 'unlink', 'chmod', 'chown', 'chroot', 'walk', 'exit'}:
                        return False, f"Blocked by guardrail: call to '{node.func.attr}'"
            # Block lambda, exec, etc.
            if isinstance(node, ast.Lambda):
                return False, "Blocked by guardrail: lambda expressions not allowed"
            # Block dunder/magic method access/definition
            if isinstance(node, ast.Attribute):
                if node.attr.startswith('__') and node.attr.endswith('__'):
                    return False, f"Blocked by guardrail: dunder attribute '{node.attr}'"
            if isinstance(node, ast.Name):
                if node.id.startswith('__') and node.id.endswith('__'):
                    return False, f"Blocked by guardrail: dunder name '{node.id}'"
    except Exception as e:
        return False, f"Guardrail AST parse error: {e}"
    return True, ""

def is_safe(code: str, extra_blocklist: set = None) -> tuple[bool, str]:
    """
    Returns (safe, reason_if_not). Checks code for dangerous patterns, AST nodes, unicode, and blocklist.
    """
    # Regex pattern checks
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False, f"Blocked by guardrail: pattern '{pattern}' detected."
    # AST-based checks
    safe, reason = _ast_guardrails(code)
    if not safe:
        # If the error is due to AST parse error (likely syntax), allow agent to attempt fix
        if reason.startswith("Guardrail AST parse error"):
            return True, "Warning: AST parse error, allowing agent to attempt fix."
        return False, reason
    # Unicode/obfuscation check
    if any(ord(c) > 127 for c in code):
        return False, "Blocked by guardrail: non-ASCII/unicode characters detected."
    # Length/complexity check
    if len(code) > 5000:
        return False, "Code too long."
    # Configurable extra blocklist
    if extra_blocklist:
        for word in extra_blocklist:
            if word in code:
                return False, f"Blocked by guardrail: '{word}' in extra blocklist."
    return True, ""
