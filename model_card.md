# Model Card: Auto-Debugger Agent

## Model Details
- **Base Model**: OpenAI GPT-4o (or [your actual model])
- **Task**: Code debugging and correction
- **Capabilities**: Analyze buggy Python code, propose fixes, test them, and iterate up to 3 times.

## Limitations & Biases
- [Describe known limitations, e.g., struggles with multi‑file projects, certain logical bugs, or non‑Python languages.]
- [Note any biases, e.g., over‑reliance on common error patterns, verbosity, or tendency to over‑engineer fixes.]

## Potential Misuse & Prevention
- **Misuse scenarios**: [e.g., generating malicious code, bypassing security checks]
- **Prevention mechanisms**: [e.g., guardrails that block dangerous operations, audit logging, sandboxed execution]

## Surprising Findings from Testing
- [Example: “The agent sometimes introduced syntax errors (like missing colons) while fixing runtime errors. The test harness caught them immediately.”]
- [Another finding: “Confidence scores were high even for incomplete fixes before adding test results to the scoring.”]

## AI Collaboration Log

### Helpful Suggestion from AI
- **Prompt / Context**: [Describe what you asked the AI]
- **Suggestion**: [What the AI proposed]
- **Why it was helpful**: [How it improved your project, e.g., “It suggested using a structured prompt template with sections for Analysis, Fix, and Tests, which made the agent’s output more reliable.”]

### Flawed / Incorrect Suggestion from AI
- **Prompt / Context**: [Describe what you asked]
- **Suggestion**: [What the AI incorrectly proposed]
- **Why it was flawed**: [Explain the error, e.g., “It told me to use `exec` to run untrusted code, which would be a major security hole.”]
- **How you corrected it**: [e.g., “I replaced it with `subprocess.run` in a sandbox.”]

## Testing Summary (Model‑Specific)
- **Test harness results**: [e.g., 6/6 test cases passed by harness; agent fixed 5/6 real bugs]
- **Average confidence score**: [e.g., 0.85]
- **Iterations per bug**: [e.g., average 1.8 attempts before success or failure]

## Ethical Considerations
- The tool should not be used for high‑stakes systems without human review.