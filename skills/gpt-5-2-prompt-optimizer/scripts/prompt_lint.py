#!/usr/bin/env python3
"""
Heuristic prompt linter for GPT-5.2 prompts tuned for `reasoning_effort: none`.

Usage:
  prompt_lint.py <prompt_file>
  cat prompt.txt | prompt_lint.py -
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    level: str  # "ERROR" | "WARN" | "INFO"
    message: str


def read_text(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    return Path(path_arg).read_text()


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE | re.MULTILINE) for p in patterns)


def lint(prompt: str) -> list[Finding]:
    findings: list[Finding] = []
    text = prompt.strip()

    if not text:
        return [Finding("ERROR", "Empty prompt.")]

    # "None reasoning" mode does best with crisp constraints; chain-of-thought requests tend to add latency/verbosity.
    if has_any(text, [r"think step[- ]by[- ]step", r"show (your|the) reasoning", r"chain[- ]of[- ]thought"]):
        findings.append(
            Finding(
                "WARN",
                "Contains chain-of-thought style instructions; remove for `reasoning_effort: none` (prefer brief self-checks).",
            )
        )

    if not has_any(text, [r"definition of done", r"stop when", r"return only", r"done when"]):
        findings.append(
            Finding(
                "WARN",
                "No obvious stop condition / definition of done (add 'Stop when…' or 'Return only…').",
            )
        )

    if not has_any(
        text,
        [
            r"output format",
            r"return (json|yaml|markdown)",
            r"schema",
            r"^\\{\\s*\"",
            r"\\b(bullets|table)\\b",
        ],
    ):
        findings.append(
            Finding(
                "WARN",
                "No explicit output format detected (add 'OUTPUT FORMAT' section and/or a schema/example).",
            )
        )

    if not has_any(text, [r"\\b(max|≤|no more than|at most)\\b", r"\\b(sentences|bullets|words|tokens)\\b"]):
        findings.append(
            Finding(
                "INFO",
                "No explicit verbosity/length clamp detected (often improves consistency and latency).",
            )
        )

    # Basic contradiction heuristic.
    concise = has_any(text, [r"\\bconcise\\b", r"\\bbrief\\b", r"short(er)?\\b", r"no (extra|unnecessary)"])
    detailed = has_any(text, [r"\\bdetailed\\b", r"comprehensive", r"thorough", r"in-depth", r"as much detail"])
    if concise and detailed and not has_any(text, [r"unless", r"trade[- ]off", r"default", r"for complex"]):
        findings.append(
            Finding(
                "WARN",
                "Potential contradiction: both 'concise' and 'detailed/comprehensive' without a rule for when each applies.",
            )
        )

    # Ambiguity policy is crucial in fast mode.
    if not has_any(text, [r"clarifying question", r"if (uncertain|unsure|ambiguous)", r"assumption"]):
        findings.append(
            Finding(
                "INFO",
                "No explicit ambiguity policy detected (consider: ask 1–3 clarifying questions or label assumptions).",
            )
        )

    # Tool policy (only if tools appear to be mentioned).
    mentions_tooling = has_any(text, [r"\\btool\\b", r"web\\s*search", r"browse", r"call (a )?tool", r"function call"])
    has_tool_policy = has_any(text, [r"when to use", r"cap tool", r"prefer answering from context", r"after tool"])
    if mentions_tooling and not has_tool_policy:
        findings.append(
            Finding(
                "WARN",
                "Mentions tools but lacks an explicit tool-use policy (when to use tools, caps, and post-tool reporting).",
            )
        )

    return findings or [Finding("INFO", "No obvious issues detected by heuristics.")]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 2 if len(argv) != 2 else 0

    text = read_text(argv[1])
    findings = lint(text)

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings = sorted(findings, key=lambda f: order.get(f.level, 99))

    for f in findings:
        print(f"{f.level}: {f.message}")

    return 1 if any(f.level == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

