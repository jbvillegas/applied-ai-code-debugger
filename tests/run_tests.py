import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agent import DebugAgent

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    test_cases = load_json(os.path.join(os.path.dirname(__file__), 'test_cases.json'))
    results = []
    for case in test_cases:
        agent = DebugAgent()
        outcome = agent.run(case["code"])
        passed = outcome["success"] == case["expected_success"]
        results.append({
            "name": case["name"],
            "passed": passed,
            "attempts": outcome["attempts"],
            "confidence": outcome["confidence"],
            "success": outcome["success"]
        })
    print("\nTest Results:")
    for r in results:
        print(f"{r['name']}: {'PASS' if r['passed'] else 'FAIL'} | Attempts: {r['attempts']} | Confidence: {r['confidence']}")
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    avg_conf = sum(r['confidence'] for r in results) / total
    avg_attempts = sum(r['attempts'] for r in results) / total
    print(f"\nSummary: {passed}/{total} passed | Avg confidence: {avg_conf:.2f} | Avg attempts: {avg_attempts:.2f}")

if __name__ == "__main__":
    main()
