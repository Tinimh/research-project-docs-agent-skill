#!/usr/bin/env python3
"""Read-only audit for research-project documentation refactors."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STANDARD_DOCS = [
    "AGENTS.md",
    "docs/COMMANDS.md",
    "docs/DOC_TEMPLATES.md",
    "docs/FILE_MAP.md",
    "docs/HANDOFF.md",
    "docs/RESEARCH_LOG.md",
    "docs/SCOPE.yml",
    "docs/WRONG_TURNS.md",
]

ROOT_DOC_ALLOWLIST = {
    "COMMANDS.md",
    "DOC_TEMPLATES.md",
    "FILE_MAP.md",
    "HANDOFF.md",
    "RESEARCH_LOG.md",
    "SCOPE.yml",
    "WRONG_TURNS.md",
}

LINE_HINTS = {
    "docs/HANDOFF.md": 250,
    "docs/COMMANDS.md": 350,
    "docs/FILE_MAP.md": 350,
    "docs/RESEARCH_LOG.md": 700,
    "docs/WRONG_TURNS.md": 700,
}

ABSOLUTE_PATH_RE = re.compile(
    r"([A-Za-z]:[\\/][^\s)`\"'>]+|/(?:home|Users|mnt|data|Dataset|var|tmp)/[^\s)`\"'>]+)"
)
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
UNCERTAIN_RE = re.compile(r"待确认|TODO|FIXME|TBD", re.IGNORECASE)
FORMAL_GAIN_RISK_RE = re.compile(
    r"simulation|report-only|matched[- ]sample|chatgpt|share reconstruction",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit existing research docs before refactoring them."
    )
    parser.add_argument("--project-root", required=True, help="Target repository root.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON only. Default is already JSON; kept for explicit callers.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def heading_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = match.group(2).strip()
        counts[heading] = counts.get(heading, 0) + 1
    return {heading: count for heading, count in counts.items() if count > 1}


def audit_file(root: Path, rel: str) -> dict[str, object]:
    path = root / rel
    if not path.is_file():
        return {"path": rel, "exists": False}
    text = read_text(path)
    lines = line_count(text)
    over_hint = LINE_HINTS.get(rel)
    issues: list[str] = []
    if over_hint and lines > over_hint:
        issues.append(f"line_count_over_hint:{lines}>{over_hint}")
    if PLACEHOLDER_RE.search(text):
        issues.append("unresolved_template_placeholders")
    if UNCERTAIN_RE.search(text):
        issues.append("contains_uncertainty_markers")
    if ABSOLUTE_PATH_RE.search(text):
        issues.append("contains_absolute_paths")
    duplicate_headings = heading_counts(text)
    if duplicate_headings:
        issues.append("duplicate_headings")
    if rel == "AGENTS.md":
        if "启动汇报" not in text and "startup report" not in text.lower():
            issues.append("missing_startup_report_format")
        if "单一真相源" not in text and "single source of truth" not in text.lower():
            issues.append("missing_single_source_of_truth")
    if rel == "docs/DOC_TEMPLATES.md":
        if "任务 / 实验卡片包" not in text and "task card" not in text.lower():
            issues.append("missing_task_card_template")
    if rel == "docs/HANDOFF.md" and lines > 250:
        issues.append("handoff_may_contain_history_dump")
    if rel == "docs/COMMANDS.md" and lines > 350:
        issues.append("commands_may_contain_one_off_history")
    if rel == "docs/FILE_MAP.md" and lines > 350:
        issues.append("file_map_may_be_evidence_dump")
    if FORMAL_GAIN_RISK_RE.search(text):
        issues.append("claim_evidence_boundary_review_needed")
    return {
        "path": rel,
        "exists": True,
        "lines": lines,
        "issues": issues,
        "duplicate_headings": duplicate_headings,
    }


def root_docs_extras(root: Path) -> list[str]:
    docs_root = root / "docs"
    if not docs_root.is_dir():
        return []
    extras: list[str] = []
    for item in docs_root.iterdir():
        if item.is_file() and item.suffix.lower() in {".md", ".yml", ".yaml"}:
            if item.name not in ROOT_DOC_ALLOWLIST:
                extras.append(str(item.relative_to(root)).replace("\\", "/"))
    return sorted(extras)


def topic_dirs(root: Path) -> list[str]:
    docs_root = root / "docs"
    if not docs_root.is_dir():
        return []
    dirs = [
        str(item.relative_to(root)).replace("\\", "/")
        for item in docs_root.iterdir()
        if item.is_dir()
    ]
    return sorted(dirs)


def build_recommendations(files: list[dict[str, object]], extras: list[str]) -> list[str]:
    recs: list[str] = []
    missing = [entry["path"] for entry in files if not entry.get("exists")]
    if missing:
        recs.append("Initialize or add missing standard docs without overwriting existing files.")
    if extras:
        recs.append("Review extra root docs files; move long topic-specific material into docs/<topic>/ and link from root docs.")
    for entry in files:
        path = str(entry["path"])
        issues = set(entry.get("issues", []))
        if "missing_startup_report_format" in issues:
            recs.append("Add a fixed startup report format to AGENTS.md.")
        if "missing_single_source_of_truth" in issues:
            recs.append("Add single-source-of-truth rules to AGENTS.md.")
        if "missing_task_card_template" in issues:
            recs.append("Add optional task/experiment card templates to docs/DOC_TEMPLATES.md.")
        if "handoff_may_contain_history_dump" in issues:
            recs.append("Slim docs/HANDOFF.md to current state and move history into topic or experiment directories.")
        if "commands_may_contain_one_off_history" in issues:
            recs.append("Keep only stable/current commands in docs/COMMANDS.md; move one-off commands to experiment records.")
        if "file_map_may_be_evidence_dump" in issues:
            recs.append("Convert docs/FILE_MAP.md back to a durable index; move evidence lists into topic directories.")
        if "claim_evidence_boundary_review_needed" in issues:
            recs.append(f"Review evidence boundary language in {path}; do not present report-only/chat-derived evidence as formal results.")
        if "contains_absolute_paths" in issues:
            recs.append(f"Review absolute paths in {path}; prefer relative paths or label machine-specific paths.")
    return sorted(set(recs))


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()
    files = [audit_file(root, rel) for rel in STANDARD_DOCS]
    extras = root_docs_extras(root)
    topics = topic_dirs(root)
    report = {
        "ok": True,
        "mode": "read_only_audit",
        "project_root": str(root),
        "standard_docs": files,
        "missing": [entry["path"] for entry in files if not entry.get("exists")],
        "extra_root_docs_files": extras,
        "topic_dirs": topics,
        "recommendations": build_recommendations(files, extras),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
