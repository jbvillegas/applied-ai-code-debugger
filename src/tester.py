import sys
import threading
import io
import builtins

SAFE_BUILTINS = {'print': print, 'len': len, 'range': range, 'str': str, 'int': int, 'float': float, 'bool': bool, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple, 'enumerate': enumerate}

def safe_execute(code: str, timeout_sec: int = 5) -> dict:
    result = {"success": False, "output": "", "error": None, "error_type": None}
    def run_code():
        nonlocal result
        try:
            local_stdout = io.StringIO()
            sys_stdout, sys_stderr = sys.stdout, sys.stderr
            sys.stdout = sys.stderr = local_stdout
            exec(code, {'__builtins__': SAFE_BUILTINS}, {})
            result["success"] = True
            result["output"] = local_stdout.getvalue()
        except SyntaxError as e:
            result["error"] = str(e)
            result["error_type"] = "SyntaxError"
        except Exception as e:
            result["error"] = str(e)
            result["error_type"] = "RuntimeError"
        finally:
            sys.stdout, sys.stderr = sys_stdout, sys_stderr
    thread = threading.Thread(target=run_code)
    thread.start()
    thread.join(timeout=timeout_sec)
    if thread.is_alive():
        result["error"] = "Timeout"
        result["error_type"] = "Timeout"
        result["success"] = False
    return result
