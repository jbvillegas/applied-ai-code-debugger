import sys
import io
import builtins
import traceback
import time
import multiprocessing
import platform

try:
    import resource  # Unix only
except ImportError:
    resource = None

from .guardrails import is_safe

SAFE_BUILTINS = {
    'print': print, 'len': len, 'range': range, 'str': str, 'int': int, 'float': float, 'bool': bool,
    'list': list, 'dict': dict, 'set': set, 'tuple': tuple, 'enumerate': enumerate, 'abs': abs, 'min': min, 'max': max, 'sum': sum
}

def safe_execute(
    code: str,
    timeout_sec: int = 5,
    input_vars: dict = None,
    output_limit: int = 4096,
    use_guardrails: bool = True,
    resource_limits: bool = True
) -> dict:
    """
    Safely execute Python code in a restricted environment.
    - Uses multiprocessing for hard timeouts.
    - Restricts builtins and globals.
    - Optionally checks guardrails (AST, regex).
    - Limits output size and system resources (Unix).
    - Captures full traceback on error.
    - Allows passing input variables.
    Returns dict with success, output, error, error_type, exec_time, and metadata.
    """
    if use_guardrails:
        safe, reason = is_safe(code)
        if not safe:
            return {"success": False, "output": "", "error": reason, "error_type": "Guardrail", "exec_time": 0, "meta": {}}

    def run_code_child(code, input_vars, output_limit, queue):
        start = time.time()
        local_stdout = io.StringIO()
        sys_stdout, sys_stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = local_stdout
        result = {"success": False, "output": "", "error": None, "error_type": None, "exec_time": 0, "meta": {}}
        try:
            # Set resource limits (Unix only)
            if resource_limits and resource is not None:
                resource.setrlimit(resource.RLIMIT_CPU, (max(1, int(timeout_sec)), max(1, int(timeout_sec))))
                resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))  # 256MB
                resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))  # 1MB file
            safe_globals = {'__builtins__': SAFE_BUILTINS}
            if input_vars:
                safe_globals.update(input_vars)
            exec(code, safe_globals, {})
            result["success"] = True
            out = local_stdout.getvalue()
            if len(out) > output_limit:
                out = out[:output_limit] + "\n...output truncated..."
            result["output"] = out
        except SyntaxError as e:
            result["error"] = traceback.format_exc()
            result["error_type"] = "SyntaxError"
        except Exception as e:
            result["error"] = traceback.format_exc()
            result["error_type"] = "RuntimeError"
        finally:
            sys.stdout, sys.stderr = sys_stdout, sys_stderr
            result["exec_time"] = round(time.time() - start, 4)
            queue.put(result)

    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=run_code_child, args=(code, input_vars, output_limit, queue))
    proc.start()
    proc.join(timeout=timeout_sec)
    if proc.is_alive():
        proc.terminate()
        return {"success": False, "output": "", "error": "Timeout", "error_type": "Timeout", "exec_time": timeout_sec, "meta": {"platform": platform.system()}}
    try:
        result = queue.get(timeout=1)
    except Exception:
        result = {"success": False, "output": "", "error": "No result returned", "error_type": "Unknown", "exec_time": 0, "meta": {}}
    result["meta"] = {"platform": platform.system()}
    return result
