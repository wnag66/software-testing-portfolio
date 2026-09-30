# AgentEval - LLM and Agent Evaluation Harness

AgentEval is a deterministic, dependency-light Python test harness for evaluating LLM and Agent behavior without depending on a paid model API.

## Coverage

- Task correctness and expected answer keywords.
- Tool selection and exact tool-call sequence.
- Grounding and unknown-information abstention.
- Prompt injection and unsafe permission handling.
- P95 latency thresholds.
- JSON and Markdown report generation.

The repository uses a rule-based Agent as the system under test so that failures are reproducible and CI does not require model credentials.

## Run

```powershell
python -m pip install -r requirements-test.txt
python -m pytest
python -m agent_eval.cli
```

The CLI writes:

- `reports/agent-eval-report.json`
- `reports/agent-eval-report.md`

