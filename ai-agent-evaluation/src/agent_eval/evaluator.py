import json
import math
from dataclasses import asdict
from pathlib import Path

from agent_eval.agent import Agent
from agent_eval.models import CaseResult, EvalCase, EvaluationSummary


def load_cases(path: str | Path) -> list[EvalCase]:
    raw_cases = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        EvalCase(
            case_id=item["case_id"],
            prompt=item["prompt"],
            expected_tools=item.get("expected_tools", []),
            expected_answer_keywords=item.get("expected_answer_keywords", []),
            forbidden_terms=item.get("forbidden_terms", []),
            max_latency_ms=item.get("max_latency_ms", 100.0),
            tags=item.get("tags", []),
        )
        for item in raw_cases
    ]


class AgentEvaluator:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def evaluate_case(self, case: EvalCase) -> CaseResult:
        result = self.agent.run(case.prompt)
        failures: list[str] = []
        actual_tools = [call.name for call in result.tool_calls]

        if actual_tools != case.expected_tools:
            failures.append(f"tool mismatch: expected={case.expected_tools}, actual={actual_tools}")

        answer = result.final_answer.lower()
        for keyword in case.expected_answer_keywords:
            if keyword.lower() not in answer:
                failures.append(f"missing answer keyword: {keyword}")

        for term in case.forbidden_terms:
            if term.lower() in answer:
                failures.append(f"forbidden term returned: {term}")

        if result.latency_ms > case.max_latency_ms:
            failures.append(
                f"latency exceeded: {result.latency_ms:.3f}ms > {case.max_latency_ms:.3f}ms"
            )

        return CaseResult(case.case_id, not failures, failures, result)

    def evaluate(self, cases: list[EvalCase]) -> tuple[list[CaseResult], EvaluationSummary]:
        results = [self.evaluate_case(case) for case in cases]
        passed = sum(1 for result in results if result.passed)
        tool_passed = sum(
            1
            for case, result in zip(cases, results, strict=True)
            if [call.name for call in result.result.tool_calls] == case.expected_tools
        )
        safety_cases = [case for case in cases if "safety" in case.tags]
        safety_results = [
            result
            for case, result in zip(cases, results, strict=True)
            if case.case_id in {item.case_id for item in safety_cases}
        ]
        safety_passed = sum(1 for result in safety_results if result.passed)
        latencies = sorted(result.result.latency_ms for result in results)

        summary = EvaluationSummary(
            total=len(cases),
            passed=passed,
            task_success_rate=round(passed / len(cases), 4) if cases else 0.0,
            tool_accuracy=round(tool_passed / len(cases), 4) if cases else 0.0,
            safety_pass_rate=round(safety_passed / len(safety_results), 4)
            if safety_results
            else 1.0,
            p95_latency_ms=round(_p95(latencies), 4),
            failed_cases=[result.case_id for result in results if not result.passed],
        )
        return results, summary


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    index = max(0, math.ceil(len(values) * 0.95) - 1)
    return values[index]


def write_json_report(
    path: str | Path,
    cases: list[EvalCase],
    results: list[CaseResult],
    summary: EvaluationSummary,
) -> None:
    payload = {
        "summary": asdict(summary),
        "cases": [
            {
                "case": asdict(case),
                "result": asdict(result.result),
                "passed": result.passed,
                "failures": result.failures,
            }
            for case, result in zip(cases, results, strict=True)
        ],
    }
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_markdown_report(
    path: str | Path,
    results: list[CaseResult],
    summary: EvaluationSummary,
) -> None:
    lines = [
        "# Agent Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Cases: {summary.total}",
        f"- Passed: {summary.passed}",
        f"- Task success rate: {summary.task_success_rate:.2%}",
        f"- Tool accuracy: {summary.tool_accuracy:.2%}",
        f"- Safety pass rate: {summary.safety_pass_rate:.2%}",
        f"- P95 latency: {summary.p95_latency_ms:.4f} ms",
        f"- Failed cases: {', '.join(summary.failed_cases) or 'none'}",
        "",
        "## Case Results",
        "",
        "| Case | Result | Tool calls | Latency |",
        "| --- | --- | --- | ---: |",
    ]
    for result in results:
        tools = ", ".join(call.name for call in result.result.tool_calls) or "none"
        status = "PASS" if result.passed else "FAIL"
        lines.append(
            f"| {result.case_id} | {status} | {tools} | {result.result.latency_ms:.4f} ms |"
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

