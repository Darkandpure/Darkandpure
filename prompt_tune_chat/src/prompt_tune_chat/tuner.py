"""Core prompt tuning primitives."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable, List


@dataclass(frozen=True)
class ScoredExample:
    """A single training/evaluation pair for prompt tuning."""

    user_input: str
    ideal_output: str


@dataclass(frozen=True)
class PromptEvaluation:
    """Result of evaluating one candidate prompt."""

    prompt: str
    average_similarity: float
    example_scores: List[float]


class PromptTuner:
    """Utility for proposing and evaluating prompt candidates.

    This class is intentionally light-weight and model-agnostic.
    You can integrate any model call in `run_candidate`.
    """

    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt.strip()

    def propose_prompt(self, objective: str, constraints: Iterable[str] | None = None) -> str:
        """Build a structured candidate prompt from objective + constraints."""
        safe_constraints = [c.strip() for c in (constraints or []) if c.strip()]

        lines = [
            self.system_prompt,
            "",
            "### Objective",
            objective.strip(),
        ]

        if safe_constraints:
            lines.extend(["", "### Constraints"])
            lines.extend(f"- {item}" for item in safe_constraints)

        lines.extend([
            "",
            "### Output style",
            "- Prefer clear wording over clever wording.",
            "- Be concise while preserving critical details.",
        ])

        return "\n".join(lines).strip()

    def evaluate_prompt(self, prompt: str, examples: Iterable[ScoredExample]) -> PromptEvaluation:
        """Evaluate a prompt with deterministic lexical similarity.

        The default `run_candidate` implementation is a placeholder echo behavior.
        Override it or subclass PromptTuner to call your preferred LLM.
        """
        example_scores: List[float] = []

        for sample in examples:
            candidate_response = self.run_candidate(prompt, sample.user_input)
            similarity = SequenceMatcher(None, candidate_response, sample.ideal_output).ratio()
            example_scores.append(round(similarity, 4))

        avg = round(sum(example_scores) / len(example_scores), 4) if example_scores else 0.0

        return PromptEvaluation(prompt=prompt, average_similarity=avg, example_scores=example_scores)

    def run_candidate(self, prompt: str, user_input: str) -> str:
        """Produce output for one test input.

        Default behavior is deterministic and local-only, making tests stable.
        Replace this method with an API-backed model call in real usage.
        """
        _ = prompt
        return user_input.strip()
