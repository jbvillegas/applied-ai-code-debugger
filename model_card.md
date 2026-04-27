# Model Card: Auto-Debugger

## Model Details
- LLM: OpenAI GPT-3.5-turbo (or GPT-4o-mini)
- Used for: code fixing, confidence scoring

## Limitations & Biases
- May fail on logic errors without runtime traces
- May overfit to common bug patterns

## Misuse Potential
- Could generate malicious code if guardrails fail (pattern blocking implemented)

## Surprising Findings
- Agent sometimes fixed two bugs at once
- Confidence scores not always correlated with correctness

## AI Collaboration Log
- Helpful: using `ast` for safe parsing
- Flawed: trying to fix timeouts by removing loops (unsafe)
