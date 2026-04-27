import argparse
import sys
from .agent import DebugAgent

def main():
    parser = argparse.ArgumentParser(description="Auto-Debugger: Self-Correcting Agentic Code Fixer")
    parser.add_argument("--file", type=str, help="Path to Python file to debug")
    parser.add_argument("--code", type=str, help="Python code as a string")
    parser.add_argument("--verbose", action="store_true", help="Show intermediate steps")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            code = f.read()
    elif args.code:
        code = args.code
    else:
        print("Enter your Python code below. Press Ctrl-D (Ctrl-Z on Windows) when done:")
        try:
            code = sys.stdin.read()
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            sys.exit(1)
        if not code.strip():
            print("No code entered. Exiting.")
            sys.exit(1)

    agent = DebugAgent()
    result = agent.run(code)
    if args.verbose:
        for entry in result["log"]:
            print(f"[Attempt {entry['attempt']}] Confidence: {entry['confidence']}\nError: {entry['error_after_fix']}\n---")
    print("\n=== Final Output ===")
    print(result["final_code"])
    print(f"\nSuccess: {result['success']} | Attempts: {result['attempts']} | Confidence: {result['confidence']}")
    if not result["success"] and "error" in result:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
