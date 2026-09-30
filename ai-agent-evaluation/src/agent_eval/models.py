from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    output: str = ""


@dataclass(frozen=True)
class AgentResult:
    final_answer: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    latency_ms: float = 0.0


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str
    expected_tools: list[str]
    expected_answer_keywords: list[str]
    forbidden_terms: list[str] = field(default_factory=list)
    max_latency_ms: float = 100.0
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    failures: list[str]
    result: AgentResult


@dataclass(frozen=True)
class EvaluationSummary:
    total: int
    passed: int
    task_success_rate: float
    tool_accuracy: float
    safety_pass_rate: float
    p95_latency_ms: float
    failed_cases: list[str]

