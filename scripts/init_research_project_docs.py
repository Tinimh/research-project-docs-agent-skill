#!/usr/bin/env python3
"""Safely initialize the documentation control plane for a research repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path


TEMPLATE_MAP = {
    "AGENTS.md.tmpl": "AGENTS.md",
    "docs/COMMANDS.md.tmpl": "docs/COMMANDS.md",
    "docs/DOC_TEMPLATES.md.tmpl": "docs/DOC_TEMPLATES.md",
    "docs/FILE_MAP.md.tmpl": "docs/FILE_MAP.md",
    "docs/HANDOFF.md.tmpl": "docs/HANDOFF.md",
    "docs/RESEARCH_LOG.md.tmpl": "docs/RESEARCH_LOG.md",
    "docs/SCOPE.yml.tmpl": "docs/SCOPE.yml",
    "docs/WRONG_TURNS.md.tmpl": "docs/WRONG_TURNS.md",
}

POST_INIT_QUESTIONS = [
    "研究问题或可证伪假设是什么？什么结果算成功或失败？",
    "权威 dataset、split、sample scope、official evaluator 和 primary metrics 是什么？",
    "当前 baseline / best 是什么，对应命令、config 和证据输出在哪里？",
    "哪些数据、标签、checkpoint、论文源文件和历史输出必须保持只读？",
    "环境安装、正式 runner、evaluation command、seed 和硬件约束是什么？",
    "训练、推理、分析、评估的主入口，以及 outputs / logs / experiments 目录分别是什么？",
    "当前 blocker、已知失败路线、下一项实验和时间边界是什么？",
]

TOKEN_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize AGENTS.md and a standard research docs/ control plane."
    )
    parser.add_argument("--project-root", required=True, help="Target repository root.")
    parser.add_argument("--project-name", help="Project name; defaults to root folder name.")
    parser.add_argument(
        "--research-goal",
        default="待确认",
        help="One-sentence research objective.",
    )
    parser.add_argument(
        "--primary-metrics",
        default="待确认",
        help="Primary evaluation metric(s) or criterion.",
    )
    parser.add_argument("--code-root", default="src", help="Relative code root.")
    parser.add_argument("--data-dir", default="data", help="Relative dataset root.")
    parser.add_argument(
        "--output-dir", default="outputs", help="Relative generated-output root."
    )
    parser.add_argument("--log-dir", default="run_logs", help="Relative run-log root.")
    parser.add_argument(
        "--communication-language", default="中文", help="Language used with the user."
    )
    parser.add_argument("--shell", default="PowerShell", help="Default command shell.")
    parser.add_argument(
        "--project-type", default="academic_experiment", help="SCOPE.yml project type."
    )
    parser.add_argument(
        "--existing-policy",
        choices=("error", "skip", "overwrite"),
        default="error",
        help="How to handle managed files that already exist.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the plan only.")
    parser.add_argument(
        "--check", action="store_true", help="Validate an initialized project without writing."
    )
    return parser.parse_args()


def normalize_relative(value: str, field: str) -> str:
    normalized = value.strip().replace("\\", "/").strip("/")
    if not normalized:
        raise ValueError(f"{field} must not be empty")
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"{field} must be a safe project-relative path: {value!r}")
    return normalized


def templates_root() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "templates"


def render_all(args: argparse.Namespace, root: Path) -> dict[str, str]:
    project_name = args.project_name or root.name or "research-project"
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{RESEARCH_GOAL}}": args.research_goal.strip() or "待确认",
        "{{PRIMARY_METRICS}}": args.primary_metrics.strip() or "待确认",
        "{{CODE_ROOT}}": normalize_relative(args.code_root, "code-root"),
        "{{DATA_DIR}}": normalize_relative(args.data_dir, "data-dir"),
        "{{OUTPUT_DIR}}": normalize_relative(args.output_dir, "output-dir"),
        "{{LOG_DIR}}": normalize_relative(args.log_dir, "log-dir"),
        "{{COMMUNICATION_LANGUAGE}}": args.communication_language.strip() or "中文",
        "{{DEFAULT_SHELL}}": args.shell.strip() or "PowerShell",
        "{{PROJECT_TYPE}}": args.project_type.strip() or "academic_experiment",
        "{{DATE}}": date.today().isoformat(),
    }

    rendered: dict[str, str] = {}
    source_root = templates_root()
    for source_rel, target_rel in TEMPLATE_MAP.items():
        source = source_root / source_rel
        if not source.is_file():
            raise FileNotFoundError(f"Missing bundled template: {source}")
        text = source.read_text(encoding="utf-8")
        for token, value in replacements.items():
            text = text.replace(token, value)
        unresolved = sorted(set(TOKEN_RE.findall(text)))
        if unresolved:
            raise ValueError(f"Unresolved tokens in {source_rel}: {unresolved}")
        rendered[target_rel] = text.rstrip() + "\n"
    return rendered


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def validate(root: Path) -> tuple[bool, dict[str, object]]:
    missing: list[str] = []
    unresolved: dict[str, list[str]] = {}
    empty: list[str] = []

    for target_rel in TEMPLATE_MAP.values():
        path = root / target_rel
        if not path.is_file():
            missing.append(target_rel)
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            empty.append(target_rel)
        tokens = sorted(set(TOKEN_RE.findall(text)))
        if tokens:
            unresolved[target_rel] = tokens

    report: dict[str, object] = {
        "mode": "check",
        "project_root": str(root),
        "managed_files": list(TEMPLATE_MAP.values()),
        "missing": missing,
        "empty": empty,
        "unresolved_placeholders": unresolved,
    }
    ok = not missing and not empty and not unresolved
    report["ok"] = ok
    return ok, report


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()

    if args.check:
        ok, report = validate(root)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    try:
        rendered = render_all(args, root)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    existing = [rel for rel in rendered if (root / rel).exists()]
    if existing and args.existing_policy == "error":
        report = {
            "ok": False,
            "mode": "dry-run" if args.dry_run else "write",
            "project_root": str(root),
            "existing_policy": args.existing_policy,
            "conflicts": existing,
            "planned_files": list(rendered),
            "message": "No files written because managed targets already exist.",
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    to_write = [
        rel
        for rel in rendered
        if not (root / rel).exists() or args.existing_policy == "overwrite"
    ]
    skipped = [rel for rel in rendered if rel not in to_write]
    report = {
        "ok": True,
        "mode": "dry-run" if args.dry_run else "write",
        "project_root": str(root),
        "existing_policy": args.existing_policy,
        "write": to_write,
        "skip": skipped,
        "overwrite": [rel for rel in to_write if rel in existing],
        "next_questions": POST_INIT_QUESTIONS,
    }

    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)
        for rel in to_write:
            atomic_write(root / rel, rendered[rel])
        report["message"] = f"Wrote {len(to_write)} file(s)."
    else:
        report["message"] = "Preview only; no files written."

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
