import time
import pickle
import os
import subprocess
import tracemalloc
from .guardrails import is_safe
from .tester import safe_execute
from .debugger import request_fix
from .confidence import score_confidence

from typing import Optional, List, Dict, Any, Callable

import concurrent.futures

class DebugAgent:
    """
    An agent that attempts to automatically debug and fix Python code using an agentic workflow and LLM.
    Includes verbose/planning mode, error handling, extensibility, and metrics.
    """
    def __init__(
        self,
        max_attempts: int = 3,
        verbose: bool = False,
        llm_params: Optional[Dict[str, Any]] = None,
        test_cases: Optional[List[str]] = None,
        timeout_sec: int = 5,
        fix_strategy: Optional[Callable] = None,
        planning_mode: bool = False,
        fix_strategies: Optional[List[Callable]] = None,
        adaptive_attempts: bool = False,
        user_feedback_callback: Optional[Callable[[dict], str]] = None,
        explainability: bool = False,
        test_runner: Optional[Callable[[str, List[str], int], dict]] = None,
        plugins: Optional[List[Callable]] = None,
        session_file: Optional[str] = None
    ):
        """
        Args:
            max_attempts: Maximum number of fix attempts.
            verbose: If True, print/log intermediate steps and LLM prompts/responses.
            llm_params: Dict of LLM parameters (model, temperature, max_tokens, etc).
            test_cases: Optional list of test case strings to run after each fix.
            timeout_sec: Timeout for code execution.
            fix_strategy: Optional custom fix function (for extensibility).
            planning_mode: If True, ask LLM for step-by-step plan before each fix.
        """
        self.max_attempts = max_attempts
        self.verbose = verbose
        self.llm_params = llm_params or {}
        self.test_cases = test_cases
        self.timeout_sec = timeout_sec
        self.fix_strategy = fix_strategy or request_fix
        self.fix_strategies = fix_strategies  # List of fix strategies for parallel execution
        self.adaptive_attempts = adaptive_attempts
        self.user_feedback_callback = user_feedback_callback
        self.explainability = explainability
        self.test_runner = test_runner  # Custom test runner (e.g., pytest)
        self.planning_mode = planning_mode
        self.history: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {"fixes": 0, "successes": 0, "failures": 0, "confidences": [], "api_calls": 0, "exec_times": [], "mem_usages": []}
        self.plugins = plugins or []
        self.session_file = session_file
        if self.session_file and os.path.exists(self.session_file):
            self._load_session()

    def run(self, code: str) -> dict:
        """
        Run the agentic debug loop on the provided code.
        Returns a dict with final_code, success, attempts, log, confidence, and metrics.
        """
        safe, reason = is_safe(code)
        if not safe:
            if self.verbose:
                print(f"[GUARDRAIL] Blocked: {reason}")
            return {
                "final_code": code,
                "success": False,
                "attempts": 0,
                "log": [],
                "confidence": 0.0,
                "error": reason,
                "metrics": self.metrics
            }
        attempt = 1
        current_code = code
        best = None
        # Adaptive attempt limit based on code length/complexity
        max_attempts = self.max_attempts
        if self.adaptive_attempts:
            code_len = len(code)
            if code_len > 2000:
                max_attempts += 1
            elif code_len < 200:
                max_attempts = max(2, max_attempts - 1)
        for attempt in range(1, max_attempts + 1):
            # Resource usage tracking
            tracemalloc.start()
            start_time = time.time()
            if self.verbose:
                print(f"\n[ATTEMPT {attempt}]\nCode:\n{current_code}")
            # Step-by-step reasoning (planning mode)
            if self.planning_mode:
                plan = self._get_plan(current_code)
                if self.verbose:
                    print(f"[PLAN] {plan}")
            # Test code (optionally with user test cases or advanced test runner)
            if self.test_runner and self.test_cases:
                test_result = self.test_runner(current_code, self.test_cases, self.timeout_sec)
            else:
                test_result = self._test_code(current_code)
            # Code quality checks (linting)
            lint_result = self._lint_code(current_code)
            # Security auditing (bandit)
            security_result = self._security_audit(current_code)
            # Plugin hooks (validators, etc.)
            for plugin in self.plugins:
                plugin_result = plugin(current_code, self.history)
                if plugin_result is not None and isinstance(plugin_result, dict):
                    if self.verbose:
                        print(f"[PLUGIN] {plugin.__name__}: {plugin_result}")
            if test_result["success"]:
                conf = score_confidence(code, current_code, "", test_result)
                explanation = self._get_explanation(code, current_code) if self.explainability else None
                exec_time = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.metrics["exec_times"].append(exec_time)
                self.metrics["mem_usages"].append(peak)
                self.metrics["api_calls"] += 1
                entry = {
                    "attempt": attempt,
                    "proposed_fix": current_code,
                    "error_after_fix": None,
                    "confidence": conf,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "plan": plan if self.planning_mode else None,
                    "explanation": explanation,
                    "lint": lint_result,
                    "security": security_result,
                    "exec_time": exec_time,
                    "mem_usage": peak
                }
                self.history.append(entry)
                self.metrics["fixes"] += 1
                self.metrics["successes"] += 1
                self.metrics["confidences"].append(conf)
                # User feedback loop
                if self.user_feedback_callback:
                    feedback = self.user_feedback_callback(entry)
                    entry["user_feedback"] = feedback
                if self.session_file:
                    self._save_session()
                return {
                    "final_code": current_code,
                    "success": True,
                    "attempts": attempt,
                    "log": self.history,
                    "confidence": conf,
                    "metrics": self.metrics
                }
            else:
                conf = score_confidence(code, current_code, test_result["error"], test_result)
                explanation = self._get_explanation(code, current_code) if self.explainability else None
                exec_time = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.metrics["exec_times"].append(exec_time)
                self.metrics["mem_usages"].append(peak)
                self.metrics["api_calls"] += 1
                entry = {
                    "attempt": attempt,
                    "proposed_fix": current_code,
                    "error_after_fix": test_result["error"],
                    "confidence": conf,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "plan": plan if self.planning_mode else None,
                    "explanation": explanation,
                    "lint": lint_result,
                    "security": security_result,
                    "exec_time": exec_time,
                    "mem_usage": peak
                }
                self.history.append(entry)
                self.metrics["fixes"] += 1
                self.metrics["failures"] += 1
                self.metrics["confidences"].append(conf)
                if self.user_feedback_callback:
                    feedback = self.user_feedback_callback(entry)
                    entry["user_feedback"] = feedback
                if self.session_file:
                    self._save_session()
                if not best or conf > best["confidence"]:
                    best = entry.copy()
                # Parallel fix strategies (if provided)
                if self.fix_strategies:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        futures = [executor.submit(
                            strat, current_code, test_result["error"], attempt, self.history, **self.llm_params
                        ) for strat in self.fix_strategies]
                        results = [f.result() for f in futures]
                        # Pick the fix with the highest confidence after testing
                        best_fix = None
                        best_conf = -1
                        for fix in results:
                            fix_test = self._test_code(fix)
                            fix_conf = score_confidence(code, fix, test_result["error"], fix_test)
                            if fix_conf > best_conf:
                                best_conf = fix_conf
                                best_fix = fix
                        current_code = best_fix
                else:
                    # Request fix from LLM (with error handling and retries)
                    for retry in range(2):
                        try:
                            if self.verbose:
                                print(f"[LLM REQUEST] Attempt {retry+1}")
                            current_code = self.fix_strategy(
                                current_code, test_result["error"], attempt, self.history, **self.llm_params
                            )
                            if not current_code or not isinstance(current_code, str):
                                raise ValueError("Malformed LLM output: No code returned.")
                            break
                        except Exception as e:
                            if self.verbose:
                                print(f"[LLM ERROR] {e}")
                            if retry == 1:
                                # On repeated failure, abort
                                return {
                                    "final_code": best["proposed_fix"] if best else code,
                                    "success": False,
                                    "attempts": attempt,
                                    "log": self.history,
                                    "confidence": best["confidence"] if best else 0.0,
                                    "error": str(e),
                                    "metrics": self.metrics
                                }
            def _get_explanation(self, original_code: str, fixed_code: str) -> Optional[str]:
                """
                Ask LLM to explain the changes made in the fix.
                """
                try:
                    from .debugger import openai
                    prompt = f"Explain in 1-2 sentences what was changed to fix the code.\nOriginal:\n{original_code}\nFixed:\n{fixed_code}\nExplanation:"
                    response = openai.ChatCompletion.create(
                        model=self.llm_params.get("model", "gpt-3.5-turbo"),
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=100,
                        temperature=0.2
                    )
                    return response.choices[0].message['content'].strip()
                except Exception as e:
                    return f"[EXPLANATION ERROR] {e}"
        # After max attempts, return best
        if self.session_file:
            self._save_session()
        return {
                def _lint_code(self, code: str) -> dict:
                    """
                    Run flake8 and pylint on the code and return results.
                    """
                    result = {}
                    try:
                        with open(".tmp_lint.py", "w") as f:
                            f.write(code)
                        flake8 = subprocess.run(["flake8", ".tmp_lint.py"], capture_output=True, text=True)
                        pylint = subprocess.run(["pylint", "--disable=all", "--enable=errors", ".tmp_lint.py"], capture_output=True, text=True)
                        result["flake8"] = flake8.stdout + flake8.stderr
                        result["pylint"] = pylint.stdout + pylint.stderr
                    except Exception as e:
                        result["error"] = str(e)
                    finally:
                        try:
                            os.remove(".tmp_lint.py")
                        except Exception:
                            pass
                    return result

                def _security_audit(self, code: str) -> dict:
                    """
                    Run bandit security scan on the code and return results.
                    """
                    result = {}
                    try:
                        with open(".tmp_bandit.py", "w") as f:
                            f.write(code)
                        bandit = subprocess.run(["bandit", "-r", ".tmp_bandit.py", "-f", "json"], capture_output=True, text=True)
                        result["bandit"] = bandit.stdout + bandit.stderr
                    except Exception as e:
                        result["error"] = str(e)
                    finally:
                        try:
                            os.remove(".tmp_bandit.py")
                        except Exception:
                            pass
                    return result

                def _save_session(self):
                    try:
                        with open(self.session_file, "wb") as f:
                            pickle.dump({
                                "history": self.history,
                                "metrics": self.metrics
                            }, f)
                    except Exception as e:
                        if self.verbose:
                            print(f"[SESSION SAVE ERROR] {e}")

                def _load_session(self):
                    try:
                        with open(self.session_file, "rb") as f:
                            data = pickle.load(f)
                            self.history = data.get("history", [])
                            self.metrics = data.get("metrics", self.metrics)
                    except Exception as e:
                        if self.verbose:
                            print(f"[SESSION LOAD ERROR] {e}")
            "final_code": best["proposed_fix"] if best else code,
            "success": False,
            "attempts": self.max_attempts,
            "log": self.history,
            "confidence": best["confidence"] if best else 0.0,
            "metrics": self.metrics
        }

    def _test_code(self, code: str) -> dict:
        """
        Test code using safe_execute and/or user test cases.
        """
        if self.test_cases:
            # Run all test cases and aggregate results
            for test in self.test_cases:
                # For simplicity, just exec code + test (could be improved)
                combined = code + '\n' + test
                result = safe_execute(combined, timeout_sec=self.timeout_sec)
                if not result["success"]:
                    return result
            return {"success": True, "output": "All tests passed.", "error": None, "error_type": None}
        else:
            return safe_execute(code, timeout_sec=self.timeout_sec)

    def _get_plan(self, code: str) -> str:
        """
        Ask LLM for a step-by-step plan for fixing the code (planning mode).
        """
        try:
            from .debugger import openai
            plan_prompt = f"You are an expert Python debugger. Given the code below, outline a step-by-step plan to fix any errors.\nCODE:\n{code}\nPLAN:"
            response = openai.ChatCompletion.create(
                model=self.llm_params.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": plan_prompt}],
                max_tokens=200,
                temperature=0.2
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"[PLAN ERROR] {e}"
