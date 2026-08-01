#!/usr/bin/env python3
"""Format supplied findings as a commit-anchored inline GitHub review."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import PurePosixPath
from typing import Any


SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
PRIORITY_COLORS = {
    "P0": "red",
    "P1": "red",
    "P2": "yellow",
    "P3": "blue",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value.strip()


def validate_path(value: Any) -> str:
    path = require_text(value, "path").replace("\\", "/")
    parsed = PurePosixPath(path)
    if parsed.is_absolute() or ".." in parsed.parts:
        fail("path must be repository-relative and must not contain '..'")
    return path


def validate_line(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        fail(f"{field} must be a positive integer")
    return value


def review_body(commit_id: str) -> str:
    short_sha = commit_id[:10]
    return f"""### Code Review

**Reviewed commit:** `{short_sha}`"""


def finding_body(priority: str, title: str, body: str) -> str:
    color = PRIORITY_COLORS[priority]
    badge = f"https://img.shields.io/badge/{priority}-{color}?style=flat"
    return (
        f"**<sub><sub>![{priority} Badge]({badge})</sub></sub>  {title}**\n\n"
        f"{body}"
    )


def load_input(path: str) -> tuple[str, list[dict[str, Any]]]:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        fail("input must be a JSON object")

    commit_id = require_text(data.get("commit_id"), "commit_id")
    if not SHA_RE.fullmatch(commit_id):
        fail("commit_id must be a full 40-character hexadecimal SHA")

    findings = data.get("findings")
    if not isinstance(findings, list):
        fail("findings must be an array")
    return commit_id.lower(), findings


def build_comment(finding: Any, index: int) -> dict[str, Any]:
    if not isinstance(finding, dict):
        fail(f"findings[{index}] must be an object")

    priority = require_text(finding.get("priority"), f"findings[{index}].priority").upper()
    if priority not in PRIORITY_COLORS:
        fail(f"findings[{index}].priority must be one of P0, P1, P2, P3")
    title = require_text(finding.get("title"), f"findings[{index}].title")
    body = require_text(finding.get("body"), f"findings[{index}].body")
    line = validate_line(finding.get("line"), f"findings[{index}].line")
    side = require_text(finding.get("side", "RIGHT"), f"findings[{index}].side").upper()
    if side not in {"LEFT", "RIGHT"}:
        fail(f"findings[{index}].side must be LEFT or RIGHT")

    comment: dict[str, Any] = {
        "path": validate_path(finding.get("path")),
        "line": line,
        "side": side,
        "body": finding_body(priority, title, body),
    }
    if "start_line" in finding and finding["start_line"] is not None:
        start_line = validate_line(finding["start_line"], f"findings[{index}].start_line")
        if start_line >= line:
            fail(f"findings[{index}].start_line must be less than line; omit it for one line")
        comment["start_line"] = start_line
        comment["start_side"] = side
    return comment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file containing a commit_id and supplied findings")
    args = parser.parse_args()

    try:
        commit_id, findings = load_input(args.input)
        if not findings:
            fail("at least one supplied finding is required")
        payload = {
            "body": review_body(commit_id),
            "commit_id": commit_id,
            "event": "COMMENT",
            "comments": [build_comment(item, i) for i, item in enumerate(findings)],
        }
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
