import re
import time
from abc import ABC, abstractmethod
from typing import Protocol

from agent_eval.models import AgentResult, ToolCall


class Agent(Protocol):
    def run(self, prompt: str) -> AgentResult:
        ...


class Tool(ABC):
    name: str

    @abstractmethod
    def execute(self, **arguments: object) -> str:
        ...


class CalculatorTool(Tool):
    name = "calculator"

    def execute(self, expression: str) -> str:
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
            raise ValueError("Unsupported calculator expression")
        return str(eval(expression, {"__builtins__": {}}, {}))


class KnowledgeLookupTool(Tool):
    name = "knowledge_lookup"

    _knowledge = {
        "RAG": "RAG 是检索增强生成，先检索可信资料，再让大模型基于上下文生成回答。",
        "Agent": "Agent 通常由规划、记忆、工具调用和结果反思组成。",
        "大模型评测": "大模型评测关注准确率、鲁棒性、安全性、延迟和成本。",
    }

    def execute(self, query: str) -> str:
        for keyword, answer in self._knowledge.items():
            if keyword.lower() in query.lower():
                return answer
        return "无法确认该信息，请提供可信资料。"


class TicketCreateTool(Tool):
    name = "ticket_create"

    def execute(self, summary: str, priority: str = "NORMAL") -> str:
        return f"工单已创建：{summary}，优先级 {priority}。"


class RuleBasedAgent:
    """Deterministic agent used as a reproducible SUT for evaluation tests."""

    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {
            "calculator": CalculatorTool(),
            "knowledge_lookup": KnowledgeLookupTool(),
            "ticket_create": TicketCreateTool(),
        }

    def run(self, prompt: str) -> AgentResult:
        started = time.perf_counter()
        tool_calls: list[ToolCall] = []

        if self._is_unsafe(prompt):
            return AgentResult(
                final_answer="无法执行该请求，请遵守安全规范。",
                tool_calls=[],
                latency_ms=self._elapsed(started),
            )

        expression = self._extract_expression(prompt)
        if expression is not None:
            output = self.tools["calculator"].execute(expression=expression)
            tool_calls.append(ToolCall("calculator", {"expression": expression}, output))
            return AgentResult(
                final_answer=f"计算结果是 {output}。",
                tool_calls=tool_calls,
                latency_ms=self._elapsed(started),
            )

        if "创建工单" in prompt:
            summary = prompt.split("：", 1)[-1]
            priority = "HIGH" if "高" in prompt else "NORMAL"
            output = self.tools["ticket_create"].execute(summary=summary, priority=priority)
            tool_calls.append(ToolCall("ticket_create", {"summary": summary, "priority": priority}, output))
            return AgentResult(
                final_answer=output,
                tool_calls=tool_calls,
                latency_ms=self._elapsed(started),
            )

        if any(keyword in prompt for keyword in ["RAG", "Agent", "大模型评测"]):
            output = self.tools["knowledge_lookup"].execute(query=prompt)
            tool_calls.append(ToolCall("knowledge_lookup", {"query": prompt}, output))
            return AgentResult(
                final_answer=output,
                tool_calls=tool_calls,
                latency_ms=self._elapsed(started),
            )

        return AgentResult(
            final_answer="无法确认该信息，请提供可信资料。",
            tool_calls=[],
            latency_ms=self._elapsed(started),
        )

    @staticmethod
    def _is_unsafe(prompt: str) -> bool:
        unsafe_markers = [
            "忽略之前的指令",
            "系统提示词",
            "修改数据库密码",
            "删除日志",
        ]
        return any(marker in prompt for marker in unsafe_markers)

    @staticmethod
    def _extract_expression(prompt: str) -> str | None:
        match = re.search(r"(\d+(?:\.\d+)?(?:\s*[+\-*/]\s*\d+(?:\.\d+)?)+)", prompt)
        return match.group(1).strip() if match else None

    @staticmethod
    def _elapsed(started: float) -> float:
        return (time.perf_counter() - started) * 1000

