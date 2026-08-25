#!/usr/bin/env python3
"""Extract, merge, validate, and display Codex skill-usage statistics."""

from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import socket
import sys
from typing import Any


SCHEMA_VERSION = "1.0.0"
ROLLOUT_DATE = re.compile(r"^rollout-(\d{4}-\d{2}-\d{2})T")
SKILL_PATH = re.compile(r'(?:/|\.\.?/)[^\s"\'`;,)}\]]*?SKILL\.md')
WORKDIR = re.compile(r'["\']workdir["\']\s*:\s*["\']([^"\']+)["\']')


def _rollout_date(path: Path) -> str | None:
    match = ROLLOUT_DATE.match(path.name)
    return match.group(1) if match else None


def _skill_paths(text: str) -> list[str]:
    return sorted(set(SKILL_PATH.findall(text)))


def _workdir(text: str, fallback: Path) -> Path:
    match = WORKDIR.search(text)
    return Path(match.group(1)) if match else fallback


def _skill_name(path: Path) -> str:
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:8192]
    except OSError:
        return path.parent.name
    match = re.search(r'^name:\s*["\']?([^\n"\']+)["\']?\s*$', head, re.MULTILINE)
    return match.group(1).strip() if match else path.parent.name


def _log_files(log_root: Path, start: date, end: date) -> list[Path]:
    files: list[Path] = []
    for directory in (log_root / "sessions", log_root / "archived_sessions"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*.jsonl"):
            value = _rollout_date(path)
            if value and start.isoformat() <= value <= end.isoformat():
                files.append(path)
    return sorted(files)


def extract_logs(
    log_root: Path,
    start: date,
    end: date,
    hostname: str,
    timezone: str,
) -> dict[str, Any]:
    """Stream Codex JSONL logs into one complete per-host record."""
    files = _log_files(log_root, start, end)
    session_ids: set[str] = set()
    turn_ids: set[str] = set()
    skill_turns: set[tuple[str, str]] = set()
    using_turns: set[str] = set()
    malformed_lines = 0
    name_cache: dict[Path, str] = {}
    skill_data: dict[str, dict[str, Any]] = {}
    daily_data: dict[str, dict[str, Any]] = {}

    for log_path in files:
        day = _rollout_date(log_path)
        if day is None:
            continue
        session_id = log_path.stem
        session_cwd = log_root
        current_turn: str | None = None

        with log_path.open(encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    malformed_lines += 1
                    continue

                record_type = record.get("type")
                payload = record.get("payload") or {}
                if record_type == "session_meta":
                    session_id = (
                        payload.get("session_id")
                        or payload.get("id")
                        or session_id
                    )
                    session_cwd = Path(payload.get("cwd") or session_cwd)
                    session_ids.add(session_id)
                    continue
                if record_type == "turn_context":
                    current_turn = payload.get("turn_id")
                    if current_turn:
                        turn_ids.add(current_turn)
                    continue
                if record_type != "response_item":
                    continue

                text = ""
                relevant = False
                if (
                    payload.get("type") == "custom_tool_call"
                    and payload.get("name") == "exec"
                ):
                    text = payload.get("input") or ""
                    relevant = any(
                        marker in text
                        for marker in ("exec_command", "read_file", "read_text_file")
                    )
                elif payload.get("type") == "function_call":
                    text = payload.get("arguments") or ""
                    relevant = bool(
                        re.search(
                            r"exec|read|shell|command",
                            payload.get("name") or "",
                            re.IGNORECASE,
                        )
                    )
                if not relevant or "SKILL.md" not in text:
                    continue

                metadata = payload.get(
                    "internal_chat_message_metadata_passthrough"
                ) or {}
                turn_id = (
                    metadata.get("turn_id")
                    or current_turn
                    or f"{session_id}:{record.get('timestamp', line_number)}"
                )
                turn_ids.add(turn_id)
                source_workdir = _workdir(text, session_cwd)

                for observed in _skill_paths(text):
                    path = Path(observed)
                    resolved = path if path.is_absolute() else source_workdir / path
                    resolved = resolved.resolve(strict=False)
                    name = name_cache.setdefault(resolved, _skill_name(resolved))
                    if not name:
                        continue

                    skill = skill_data.setdefault(
                        name,
                        {
                            "activations": 0,
                            "raw_reads": 0,
                            "sessions": set(),
                            "daily": {},
                        },
                    )
                    skill["raw_reads"] += 1
                    skill["sessions"].add(session_id)
                    skill_day = skill["daily"].setdefault(
                        day,
                        {
                            "activations": 0,
                            "raw_reads": 0,
                            "sessions": set(),
                        },
                    )
                    skill_day["raw_reads"] += 1
                    skill_day["sessions"].add(session_id)

                    overall_day = daily_data.setdefault(
                        day,
                        {
                            "activations": 0,
                            "raw_reads": 0,
                            "turns": set(),
                        },
                    )
                    overall_day["raw_reads"] += 1

                    activation_key = (name, turn_id)
                    if activation_key not in skill_turns:
                        skill_turns.add(activation_key)
                        using_turns.add(turn_id)
                        skill["activations"] += 1
                        skill_day["activations"] += 1
                        overall_day["activations"] += 1
                        overall_day["turns"].add(turn_id)

    skill_rows: list[dict[str, Any]] = []
    for name, skill in skill_data.items():
        daily_rows = [
            {
                "date": day,
                "activations": values["activations"],
                "raw_reads": values["raw_reads"],
                "sessions": len(values["sessions"]),
            }
            for day, values in sorted(skill["daily"].items())
        ]
        skill_rows.append(
            {
                "name": name,
                "activations": skill["activations"],
                "raw_reads": skill["raw_reads"],
                "sessions": len(skill["sessions"]),
                "active_days": len(daily_rows),
                "first_date": daily_rows[0]["date"],
                "last_date": daily_rows[-1]["date"],
                "daily": daily_rows,
            }
        )
    skill_rows.sort(key=lambda row: (-row["activations"], row["name"]))

    daily_rows = [
        {
            "date": day,
            "activations": values["activations"],
            "raw_reads": values["raw_reads"],
            "skill_using_turns": len(values["turns"]),
        }
        for day, values in sorted(daily_data.items())
    ]
    return {
        "hostname": hostname,
        "timezone": timezone,
        "corpus": {
            "log_files": len(files),
            "log_bytes": sum(path.stat().st_size for path in files),
            "sessions": len(session_ids),
            "turns": len(turn_ids),
            "malformed_lines": malformed_lines,
        },
        "totals": {
            "unique_skills": len(skill_rows),
            "activations": sum(row["activations"] for row in skill_rows),
            "raw_reads": sum(row["raw_reads"] for row in skill_rows),
            "skill_using_turns": len(using_turns),
        },
        "skills": skill_rows,
        "daily": daily_rows,
    }


def combine_hosts(hosts: list[dict[str, Any]]) -> dict[str, Any]:
    """Combine independent per-host usage records."""
    seen_hostnames: set[str] = set()
    corpus = defaultdict(int)
    totals = defaultdict(int)
    skills: dict[str, dict[str, Any]] = {}
    daily: dict[str, dict[str, int]] = {}

    for host in hosts:
        hostname = host["hostname"]
        if hostname in seen_hostnames:
            raise ValueError(f"duplicate hostname: {hostname}")
        seen_hostnames.add(hostname)

        for key, value in host["corpus"].items():
            corpus[key] += value
        for key in ("activations", "raw_reads", "skill_using_turns"):
            totals[key] += host["totals"][key]

        for row in host["daily"]:
            target = daily.setdefault(
                row["date"],
                {"activations": 0, "raw_reads": 0, "skill_using_turns": 0},
            )
            for key in ("activations", "raw_reads", "skill_using_turns"):
                target[key] += row[key]

        for skill in host["skills"]:
            target = skills.setdefault(
                skill["name"],
                {
                    "name": skill["name"],
                    "activations": 0,
                    "raw_reads": 0,
                    "sessions": 0,
                    "daily": {},
                },
            )
            for key in ("activations", "raw_reads", "sessions"):
                target[key] += skill[key]
            for row in skill["daily"]:
                day = target["daily"].setdefault(
                    row["date"],
                    {"activations": 0, "raw_reads": 0, "sessions": 0},
                )
                for key in ("activations", "raw_reads", "sessions"):
                    day[key] += row[key]

    skill_rows = []
    for skill in skills.values():
        day_rows = [
            {"date": date, **counts}
            for date, counts in sorted(skill.pop("daily").items())
        ]
        skill_rows.append(
            {
                **skill,
                "active_days": len(day_rows),
                "first_date": day_rows[0]["date"],
                "last_date": day_rows[-1]["date"],
                "daily": day_rows,
            }
        )
    skill_rows.sort(key=lambda row: (-row["activations"], row["name"]))

    daily_rows = [
        {"date": date, **counts} for date, counts in sorted(daily.items())
    ]
    totals["unique_skills"] = len(skill_rows)
    return {
        "corpus": dict(corpus),
        "totals": dict(totals),
        "skills": skill_rows,
        "daily": daily_rows,
    }


def build_document(
    hosts: list[dict[str, Any]], period: dict[str, str]
) -> dict[str, Any]:
    """Build a versioned document and recompute its combined view."""
    ordered_hosts = sorted(deepcopy(hosts), key=lambda host: host["hostname"])
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "period": deepcopy(period),
        "hosts": ordered_hosts,
        "combined": combine_hosts(ordered_hosts),
    }


def merge_documents(documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge independent machine exports and recompute all combined values."""
    if not documents:
        raise ValueError("at least one input document is required")
    hosts = [host for document in documents for host in document["hosts"]]
    period = {
        "start_date": min(
            document["period"]["start_date"] for document in documents
        ),
        "end_date": max(document["period"]["end_date"] for document in documents),
        "timezone": documents[0]["period"]["timezone"],
    }
    return build_document(hosts, period)


def _path_keys(value: Any, location: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key == "path" or key.endswith("_path") or key.endswith("_paths"):
                errors.append(f"path field is not allowed: {child_location}")
            errors.extend(_path_keys(child, child_location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_path_keys(child, f"{location}[{index}]"))
    return errors


def validate_document(document: dict[str, Any]) -> list[str]:
    """Return human-readable validation errors for one dataset."""
    errors = _path_keys(document)
    required = {"schema_version", "generated_at", "period", "hosts", "combined"}
    missing = sorted(required - document.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
        return errors
    unexpected = sorted(document.keys() - required)
    if unexpected:
        errors.append(f"unexpected top-level fields: {', '.join(unexpected)}")
    if document["schema_version"] != SCHEMA_VERSION:
        errors.append(
            f"unsupported schema_version: {document['schema_version']!r}; "
            f"expected {SCHEMA_VERSION!r}"
        )
    try:
        start = date.fromisoformat(document["period"]["start_date"])
        end = date.fromisoformat(document["period"]["end_date"])
        if start > end:
            errors.append("period.start_date must not be after period.end_date")
    except (KeyError, TypeError, ValueError):
        errors.append("period must contain valid start_date and end_date values")
    if not isinstance(document["hosts"], list) or not document["hosts"]:
        errors.append("hosts must be a non-empty array")
        return errors
    try:
        expected = combine_hosts(document["hosts"])
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid host data: {exc}")
        return errors
    if document["combined"] != expected:
        errors.append("combined view does not match recomputed host data")
    return errors


def _read_document(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"document root must be an object: {path}")
    return value


def _write_document(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _date_range(arguments: argparse.Namespace) -> tuple[date, date]:
    end = date.fromisoformat(arguments.until) if arguments.until else date.today()
    if arguments.since:
        start = date.fromisoformat(arguments.since)
    elif arguments.months is not None:
        month_index = end.year * 12 + end.month - 1 - arguments.months
        year, zero_based_month = divmod(month_index, 12)
        month = zero_based_month + 1
        next_month = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        start = date(year, month, min(end.day, last_day))
    else:
        days = arguments.days if arguments.days is not None else 30
        start = end - timedelta(days=days - 1)
    if start > end:
        raise ValueError("--since must not be after --until")
    return start, end


def render_dashboard(document: dict[str, Any]) -> str:
    """Render a self-contained interactive dashboard."""
    data = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Skill usage</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #0b1433;
      --muted: #59627a;
      --rule: #d9deea;
      --soft: #f5f7fb;
      --blue: #1457d9;
      --blue-soft: #eaf0ff;
      --teal: #0798a5;
      --white: #ffffff;
      --radius: 6px;
      font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--white);
      color: var(--ink);
      font-size: 14px;
      line-height: 1.45;
    }
    button, input, select { font: inherit; color: inherit; }
    button, select { cursor: pointer; }
    button:focus-visible, input:focus-visible, select:focus-visible {
      outline: 3px solid rgba(20, 87, 217, .22);
      outline-offset: 2px;
    }
    .shell { max-width: 1520px; margin: 0 auto; padding: 24px 22px 18px; }
    .header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--rule);
    }
    h1 { margin: 0; font-size: clamp(34px, 4vw, 48px); line-height: 1; letter-spacing: -.035em; }
    .period { margin: 10px 0 0; color: var(--ink); font-size: 18px; }
    .source-control { display: grid; gap: 6px; min-width: 220px; }
    .source-control label, .field-label { color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
    select, input {
      border: 1px solid var(--rule);
      border-radius: var(--radius);
      background: var(--white);
      min-height: 40px;
    }
    select { padding: 0 36px 0 12px; }
    .metrics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border-bottom: 1px solid var(--rule);
      padding: 22px 0;
    }
    .metric { text-align: center; padding: 0 20px; }
    .metric + .metric { border-left: 1px solid var(--rule); }
    .metric-value { color: var(--blue); font-size: clamp(34px, 4vw, 48px); font-weight: 750; line-height: 1; letter-spacing: -.03em; }
    .metric-label { margin-top: 5px; font-size: 16px; }
    .charts {
      display: grid;
      grid-template-columns: minmax(360px, .9fr) minmax(500px, 1.35fr);
      gap: 36px;
      padding: 20px 0 22px;
      border-bottom: 1px solid var(--rule);
    }
    .section-title { margin: 0 0 14px; font-size: 16px; }
    .bar-chart { display: grid; gap: 9px; min-height: 286px; align-content: center; }
    .bar-row { display: grid; grid-template-columns: minmax(140px, 220px) 1fr 46px; gap: 10px; align-items: center; }
    .bar-label { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: right; }
    .bar-track { height: 12px; background: var(--soft); overflow: hidden; }
    .bar-fill { height: 100%; background: var(--blue); transform-origin: left; animation: grow .45s ease-out both; }
    .bar-value { font-variant-numeric: tabular-nums; }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    .timeline-wrap { min-height: 286px; }
    .timeline { width: 100%; height: 286px; display: block; overflow: visible; }
    .timeline text { fill: var(--muted); font: 11px Inter, ui-sans-serif, sans-serif; }
    .timeline .grid { stroke: #e7eaf1; stroke-width: 1; }
    .timeline .bar { fill: var(--blue); }
    .timeline .line { fill: none; stroke: var(--teal); stroke-width: 2.2; }
    .timeline .dot { fill: var(--teal); stroke: var(--white); stroke-width: 1.5; }
    .legend { display: flex; justify-content: flex-end; gap: 18px; margin: -32px 0 6px; color: var(--muted); font-size: 12px; }
    .legend span::before { content: ""; display: inline-block; width: 9px; height: 9px; margin-right: 6px; }
    .legend .activations::before { background: var(--blue); }
    .legend .turns::before { background: var(--teal); border-radius: 50%; }
    .table-tools {
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      padding: 14px 0;
    }
    .search-wrap { position: relative; width: min(360px, 100%); }
    .search-wrap svg { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--ink); }
    .search-wrap input { width: 100%; padding: 0 12px 0 38px; }
    .table-meta { display: flex; align-items: center; gap: 12px; color: var(--muted); }
    .table-meta select { min-height: 36px; }
    .table-scroll { overflow-x: auto; border: 1px solid var(--rule); }
    table { width: 100%; border-collapse: collapse; min-width: 980px; }
    th, td { padding: 10px 14px; border-bottom: 1px solid #e7eaf1; text-align: right; font-variant-numeric: tabular-nums; }
    th { background: #fbfcfe; font-size: 12px; letter-spacing: .02em; }
    th:first-child, td:first-child { text-align: left; }
    th button { width: 100%; border: 0; background: transparent; padding: 0; font-weight: 750; text-align: inherit; }
    th button[aria-pressed="true"] { color: var(--blue); }
    tbody tr:hover { background: var(--blue-soft); }
    tbody tr:last-child td { border-bottom: 0; }
    .empty { padding: 34px; color: var(--muted); text-align: center !important; }
    .pagination { display: flex; justify-content: flex-end; align-items: center; gap: 6px; padding: 14px 0 4px; }
    .page-button {
      min-width: 34px;
      height: 34px;
      display: inline-grid;
      place-items: center;
      border: 1px solid transparent;
      border-radius: 3px;
      background: transparent;
    }
    .page-button:hover { background: var(--soft); }
    .page-button[aria-current="page"] { border-color: var(--blue); color: var(--blue); }
    .page-button:disabled { opacity: .35; cursor: default; }
    footer { border-top: 1px solid var(--rule); padding-top: 13px; color: var(--muted); font-size: 12px; }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
    @media (max-width: 980px) {
      .charts { grid-template-columns: 1fr; }
      .metrics { grid-template-columns: repeat(2, 1fr); row-gap: 22px; }
      .metric:nth-child(3) { border-left: 0; }
    }
    @media (max-width: 620px) {
      .shell { padding: 18px 14px; }
      .header { align-items: stretch; flex-direction: column; }
      .period { font-size: 16px; }
      .source-control { min-width: 0; }
      .metrics { grid-template-columns: 1fr; gap: 18px; }
      .metric + .metric { border-left: 0; }
      .metric { padding: 0; }
      .charts { grid-template-columns: minmax(0, 1fr); gap: 28px; }
      .bar-row { grid-template-columns: minmax(96px, 135px) 1fr 38px; gap: 7px; }
      .legend { margin: 0 0 4px; justify-content: flex-start; }
      .table-tools { align-items: stretch; flex-direction: column; }
      .search-wrap { width: 100%; }
      .table-meta { justify-content: space-between; }
      .pagination { justify-content: center; }
    }
    @media (prefers-reduced-motion: reduce) { .bar-fill { animation: none; } }
  </style>
</head>
<body>
  <main class="shell">
    <header class="header">
      <div>
        <h1>Skill usage</h1>
        <p class="period" id="period-label"></p>
      </div>
      <div class="source-control">
        <label for="host-filter">Data source</label>
        <select id="host-filter"></select>
      </div>
    </header>

    <section class="metrics" aria-label="Usage summary">
      <div class="metric"><div class="metric-value" id="metric-activations">—</div><div class="metric-label">Activations</div></div>
      <div class="metric"><div class="metric-value" id="metric-skills">—</div><div class="metric-label">Skills</div></div>
      <div class="metric"><div class="metric-value" id="metric-turns">—</div><div class="metric-label">Skill-using turns</div></div>
      <div class="metric"><div class="metric-value" id="metric-coverage">—</div><div class="metric-label">Turn coverage</div></div>
    </section>

    <section class="charts" aria-label="Usage charts">
      <div>
        <h2 class="section-title">Top skills by activations</h2>
        <div class="bar-chart" id="top-skills-chart"></div>
      </div>
      <div class="timeline-wrap">
        <h2 class="section-title">Daily activity</h2>
        <div class="legend"><span class="activations">Activations</span><span class="turns">Skill-using turns</span></div>
        <svg class="timeline" id="daily-chart" role="img" aria-label="Daily activations and skill-using turns"></svg>
      </div>
    </section>

    <section aria-labelledby="table-title">
      <h2 class="sr-only" id="table-title">Complete skill statistics</h2>
      <div class="table-tools">
        <div class="search-wrap">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg>
          <label class="sr-only" for="skill-search">Search skills</label>
          <input id="skill-search" type="search" placeholder="Search skills" autocomplete="off">
        </div>
        <div class="table-meta">
          <span id="row-range"></span>
          <label for="page-size">Rows per page</label>
          <select id="page-size"><option>10</option><option>25</option><option>50</option><option>100</option></select>
        </div>
      </div>
      <div class="table-scroll">
        <table id="skills-table">
          <thead><tr>
            <th><button data-sort="name">Skill</button></th>
            <th><button data-sort="activations" aria-pressed="true">Activations</button></th>
            <th><button data-sort="share">Share</button></th>
            <th><button data-sort="sessions">Sessions</button></th>
            <th><button data-sort="active_days">Active days</button></th>
            <th><button data-sort="first_date">First use</button></th>
            <th><button data-sort="last_date">Last use</button></th>
          </tr></thead>
          <tbody></tbody>
        </table>
      </div>
      <nav class="pagination" id="pagination" aria-label="Skill table pages"></nav>
    </section>

    <footer>
      Activations count each skill once per turn. Raw reads and complete per-day records remain in the embedded JSON. Matching skill names are summed when machine exports are merged.
    </footer>
  </main>

  <script id="dataset" type="application/json">__DATA__</script>
  <script>
    (() => {
      const documentData = JSON.parse(document.getElementById('dataset').textContent);
      const number = new Intl.NumberFormat();
      const shortDate = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short' });
      const fullDate = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
      const state = { source: 'combined', query: '', sort: 'activations', direction: -1, page: 1, pageSize: 10 };
      const els = {
        host: document.getElementById('host-filter'), search: document.getElementById('skill-search'),
        tbody: document.querySelector('#skills-table tbody'), pagination: document.getElementById('pagination'),
        range: document.getElementById('row-range'), pageSize: document.getElementById('page-size'),
        top: document.getElementById('top-skills-chart'), daily: document.getElementById('daily-chart')
      };

      const option = (value, label) => { const item = document.createElement('option'); item.value = value; item.textContent = label; return item; };
      els.host.append(option('combined', documentData.hosts.length > 1 ? 'All machines' : 'Combined'));
      documentData.hosts.forEach((host, index) => els.host.append(option(String(index), host.hostname)));
      document.getElementById('period-label').textContent = `${shortDate.format(new Date(documentData.period.start_date + 'T00:00:00'))} — ${fullDate.format(new Date(documentData.period.end_date + 'T00:00:00'))}`;

      function view() { return state.source === 'combined' ? documentData.combined : documentData.hosts[Number(state.source)]; }
      function svgNode(name, attributes = {}) { const node = document.createElementNS('http://www.w3.org/2000/svg', name); Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, String(value))); return node; }
      function clear(node) { while (node.firstChild) node.firstChild.remove(); }

      function renderMetrics(data) {
        document.getElementById('metric-activations').textContent = number.format(data.totals.activations);
        document.getElementById('metric-skills').textContent = number.format(data.totals.unique_skills);
        document.getElementById('metric-turns').textContent = number.format(data.totals.skill_using_turns);
        const coverage = data.corpus.turns ? 100 * data.totals.skill_using_turns / data.corpus.turns : 0;
        document.getElementById('metric-coverage').textContent = `${coverage.toFixed(1)}%`;
      }

      function renderTop(data) {
        clear(els.top);
        const rows = data.skills.slice(0, 10);
        const max = Math.max(1, ...rows.map(row => row.activations));
        rows.forEach(row => {
          const wrapper = document.createElement('div'); wrapper.className = 'bar-row';
          const label = document.createElement('div'); label.className = 'bar-label'; label.textContent = row.name; label.title = row.name;
          const track = document.createElement('div'); track.className = 'bar-track';
          const fill = document.createElement('div'); fill.className = 'bar-fill'; fill.style.width = `${100 * row.activations / max}%`;
          const value = document.createElement('div'); value.className = 'bar-value'; value.textContent = number.format(row.activations);
          track.append(fill); wrapper.append(label, track, value); els.top.append(wrapper);
        });
      }

      function renderDaily(data) {
        clear(els.daily); const rows = data.daily; const width = 760, height = 286;
        const margin = { top: 16, right: 18, bottom: 34, left: 38 }; const plotW = width - margin.left - margin.right, plotH = height - margin.top - margin.bottom;
        els.daily.setAttribute('viewBox', `0 0 ${width} ${height}`);
        if (!rows.length) return;
        const maxA = Math.max(1, ...rows.map(row => row.activations)); const maxT = Math.max(1, ...rows.map(row => row.skill_using_turns));
        for (let index = 0; index <= 4; index += 1) {
          const y = margin.top + plotH * index / 4;
          els.daily.append(svgNode('line', { class: 'grid', x1: margin.left, y1: y, x2: width - margin.right, y2: y }));
          const text = svgNode('text', { x: margin.left - 7, y: y + 4, 'text-anchor': 'end' }); text.textContent = number.format(Math.round(maxA * (4 - index) / 4)); els.daily.append(text);
        }
        const step = plotW / rows.length; const barW = Math.max(3, Math.min(14, step * .58)); const points = [];
        rows.forEach((row, index) => {
          const x = margin.left + step * index + step / 2; const barH = plotH * row.activations / maxA; const turnY = margin.top + plotH * (1 - row.skill_using_turns / maxT);
          els.daily.append(svgNode('rect', { class: 'bar', x: x - barW / 2, y: margin.top + plotH - barH, width: barW, height: barH })); points.push(`${x},${turnY}`);
          if (index === 0 || index === rows.length - 1 || index % Math.ceil(rows.length / 6) === 0) {
            const text = svgNode('text', { x, y: height - 10, 'text-anchor': 'middle' }); text.textContent = shortDate.format(new Date(row.date + 'T00:00:00')); els.daily.append(text);
          }
        });
        els.daily.append(svgNode('polyline', { class: 'line', points: points.join(' ') }));
        points.forEach(point => { const [cx, cy] = point.split(','); els.daily.append(svgNode('circle', { class: 'dot', cx, cy, r: 3.4 })); });
      }

      function sortedRows(data) {
        const total = data.totals.activations || 1;
        const rows = data.skills.filter(row => row.name.toLowerCase().includes(state.query)).map(row => ({ ...row, share: row.activations / total }));
        rows.sort((a, b) => { const av = a[state.sort], bv = b[state.sort]; if (av === bv) return a.name.localeCompare(b.name); return (av < bv ? -1 : 1) * state.direction; });
        return rows;
      }

      function cell(row, key) {
        if (key === 'share') return `${(100 * row.share).toFixed(1)}%`;
        if (key === 'first_date' || key === 'last_date') return fullDate.format(new Date(row[key] + 'T00:00:00'));
        return key === 'name' ? row[key] : number.format(row[key]);
      }

      function renderTable(data) {
        const rows = sortedRows(data); const pages = Math.max(1, Math.ceil(rows.length / state.pageSize)); state.page = Math.min(state.page, pages);
        const start = (state.page - 1) * state.pageSize; const visible = rows.slice(start, start + state.pageSize); clear(els.tbody);
        if (!visible.length) { const tr = document.createElement('tr'); const td = document.createElement('td'); td.colSpan = 7; td.className = 'empty'; td.textContent = 'No matching skills'; tr.append(td); els.tbody.append(tr); }
        visible.forEach(row => { const tr = document.createElement('tr'); ['name','activations','share','sessions','active_days','first_date','last_date'].forEach(key => { const td = document.createElement('td'); td.textContent = cell(row, key); tr.append(td); }); els.tbody.append(tr); });
        els.range.textContent = rows.length ? `${number.format(start + 1)}–${number.format(Math.min(start + state.pageSize, rows.length))} of ${number.format(rows.length)}` : '0 rows';
        renderPagination(pages);
      }

      function iconButton(label, pathData, disabled, onClick) {
        const button = document.createElement('button'); button.className = 'page-button'; button.type = 'button'; button.disabled = disabled; button.setAttribute('aria-label', label);
        const svg = svgNode('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }); svg.append(svgNode('path', { d: pathData })); button.append(svg); button.addEventListener('click', onClick); return button;
      }

      function renderPagination(pages) {
        clear(els.pagination); els.pagination.append(iconButton('Previous page', 'm15 18-6-6 6-6', state.page === 1, () => { state.page -= 1; render(); }));
        const candidates = [...new Set([1, state.page - 1, state.page, state.page + 1, pages])].filter(page => page >= 1 && page <= pages).sort((a,b) => a-b);
        let previous = 0; candidates.forEach(page => { if (page - previous > 1) { const gap = document.createElement('span'); gap.textContent = '…'; gap.setAttribute('aria-hidden', 'true'); els.pagination.append(gap); } const button = document.createElement('button'); button.type = 'button'; button.className = 'page-button'; button.textContent = page; if (page === state.page) button.setAttribute('aria-current', 'page'); button.addEventListener('click', () => { state.page = page; render(); }); els.pagination.append(button); previous = page; });
        els.pagination.append(iconButton('Next page', 'm9 18 6-6-6-6', state.page === pages, () => { state.page += 1; render(); }));
      }

      function render() { const data = view(); renderMetrics(data); renderTop(data); renderDaily(data); renderTable(data); }
      els.host.addEventListener('change', event => { state.source = event.target.value; state.page = 1; render(); });
      els.search.addEventListener('input', event => { state.query = event.target.value.trim().toLowerCase(); state.page = 1; renderTable(view()); });
      els.pageSize.addEventListener('change', event => { state.pageSize = Number(event.target.value); state.page = 1; renderTable(view()); });
      document.querySelectorAll('th button[data-sort]').forEach(button => button.addEventListener('click', () => { const key = button.dataset.sort; state.direction = state.sort === key ? -state.direction : (key === 'name' ? 1 : -1); state.sort = key; state.page = 1; document.querySelectorAll('th button[data-sort]').forEach(item => item.setAttribute('aria-pressed', String(item === button))); renderTable(view()); }));
      render();
    })();
  </script>
</body>
</html>
'''
    return template.replace("__DATA__", data)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill_usage.py",
        description="Extract and merge Codex skill-usage statistics.",
        epilog=(
            "Examples:\n"
            "  python3 skill_usage.py extract --logs ~/.codex --months 6 "
            "--output usage.json\n"
            "  python3 skill_usage.py extract --logs ~/.codex --days 30 "
            "--output usage.json\n"
            "  python3 skill_usage.py merge laptop.json desktop.json "
            "--output merged.json\n"
            "  python3 skill_usage.py dashboard merged.json "
            "--output dashboard.html\n"
            "  python3 skill_usage.py validate merged.json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser(
        "extract", help="Extract one machine's local session logs."
    )
    extract.add_argument("--logs", type=Path, default=Path.home() / ".codex")
    range_group = extract.add_mutually_exclusive_group()
    range_group.add_argument("--days", type=int)
    range_group.add_argument("--months", type=int)
    range_group.add_argument("--since", help="Inclusive YYYY-MM-DD start date.")
    extract.add_argument("--until", help="Inclusive YYYY-MM-DD end date.")
    extract.add_argument("--hostname", default=socket.gethostname())
    extract.add_argument("--timezone", default=os.environ.get("TZ", "UTC"))
    extract.add_argument("--output", required=True, type=Path)

    merge = subparsers.add_parser("merge", help="Merge independent host exports.")
    merge.add_argument("inputs", nargs="+", type=Path)
    merge.add_argument("--output", required=True, type=Path)

    validate = subparsers.add_parser("validate", help="Validate one dataset.")
    validate.add_argument("input", type=Path)

    dashboard = subparsers.add_parser(
        "dashboard", help="Generate a self-contained HTML dashboard."
    )
    dashboard.add_argument("input", type=Path)
    dashboard.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "extract":
            if arguments.days is not None and arguments.days < 1:
                raise ValueError("--days must be at least 1")
            if arguments.months is not None and arguments.months < 1:
                raise ValueError("--months must be at least 1")
            start, end = _date_range(arguments)
            host = extract_logs(
                arguments.logs,
                start,
                end,
                arguments.hostname,
                arguments.timezone,
            )
            document = build_document(
                [host],
                {
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "timezone": arguments.timezone,
                },
            )
            _write_document(arguments.output, document)
            print(f"wrote {arguments.output}")
            return 0
        if arguments.command == "merge":
            documents = [_read_document(path) for path in arguments.inputs]
            for input_path, document in zip(arguments.inputs, documents):
                errors = validate_document(document)
                if errors:
                    raise ValueError(f"invalid {input_path}: {'; '.join(errors)}")
            merged = merge_documents(documents)
            _write_document(arguments.output, merged)
            print(f"wrote {arguments.output}")
            return 0
        if arguments.command == "validate":
            document = _read_document(arguments.input)
            errors = validate_document(document)
            if errors:
                raise ValueError("; ".join(errors))
            print(f"valid: {arguments.input}")
            return 0
        if arguments.command == "dashboard":
            document = _read_document(arguments.input)
            errors = validate_document(document)
            if errors:
                raise ValueError("; ".join(errors))
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            arguments.output.write_text(render_dashboard(document), encoding="utf-8")
            print(f"wrote {arguments.output}")
            return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
