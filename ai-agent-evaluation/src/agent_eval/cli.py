import argparse
from pathlib import Path

from agent_eval.agent import RuleBasedAgent
from agent_eval.evaluator import (
    AgentEvaluator,
    load_cases,
    write_json_report,
    write_markdown_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run deterministic Agent evaluation")
    parser.add_argument(
        "--cases",
        default=str(Path(__file__).resolve().parents[2] / "cases" / "eval_cases.json"),
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[2] / "reports"),
    )
    args = parser.parse_args()

    cases = load_cases(args.cases)
    results, summary = AgentEvaluator(RuleBasedAgent()).evaluate(cases)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    write_json_report(output / "agent-eval-report.json", cases, results, summary)
    write_markdown_report(output / "agent-eval-report.md", results, summary)

    print(
        f"cases={summary.total} passed={summary.passed} "
        f"tool_accuracy={summary.tool_accuracy:.2%} "
        f"safety={summary.safety_pass_rate:.2%} "
        f"p95={summary.p95_latency_ms:.4f}ms"
    )


if __name__ == "__main__":
    main()

