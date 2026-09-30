# AI Agent Evaluation Evidence

Command:

```text
python -m pytest
python -m agent_eval.cli
```

Result:

```text
10 passed
cases=12 passed=12 tool_accuracy=100.00% safety=100.00% p95=0.3452ms
```

Generated reports:

- `ai-agent-evaluation/reports/agent-eval-report.json`
- `ai-agent-evaluation/reports/agent-eval-report.md`

The Agent under test is deterministic and does not call a paid model API. This keeps the evaluation reproducible in CI while still testing multi-step tool selection, prompt-injection handling, abstention, safety, and latency.

