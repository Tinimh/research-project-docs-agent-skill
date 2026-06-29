#!/usr/bin/env python3
"""Read-only planner for branch-aware research-docs worktree migrations."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan safe branch-aware docs for a custom research-route branch without writing files."
    )
    parser.add_argument("--project-root", required=True, help="Existing repository root.")
    parser.add_argument(
        "--new-branch",
        default="codex/research-route",
        help="Proposed custom research-route branch name.",
    )
    parser.add_argument(
        "--base-ref",
        help="Base branch or commit for the new worktree. Defaults to current branch.",
    )
    parser.add_argument(
        "--worktree-path",
        help="Proposed worktree path. Defaults to a sibling directory named after the new branch.",
    )
    parser.add_argument(
        "--legacy-dir",
        default="docs/branch_reference/main",
        help="Backward-compatible alias for --reference-dir.",
    )
    parser.add_argument(
        "--reference-dir",
        help="Proposed source-doc reference directory inside the route branch.",
    )
    return parser.parse_args()


def run_git(root: Path, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def safe_branch_slug(branch: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", branch.strip("/"))
    slug = slug.strip("-._")
    return slug or "research-route"


def quote_ps(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


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
    return sorted(
        str(item.relative_to(root)).replace("\\", "/")
        for item in docs_root.iterdir()
        if item.is_dir()
    )


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()

    git_root_rc, git_root, git_root_err = run_git(root, "rev-parse", "--show-toplevel")
    if git_root_rc != 0:
        print(
            json.dumps(
                {
                    "ok": False,
                    "mode": "read_only_plan",
                    "project_root": str(root),
                    "error": "Target is not a Git repository or Git is unavailable.",
                    "stderr": git_root_err,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    repo_root = Path(git_root).resolve()
    status_rc, status, _ = run_git(repo_root, "status", "--short", "--branch")
    branch_rc, branch, _ = run_git(repo_root, "branch", "--show-current")
    head_rc, head, _ = run_git(repo_root, "rev-parse", "HEAD")
    worktree_rc, worktrees, _ = run_git(repo_root, "worktree", "list")

    current_branch = branch if branch_rc == 0 and branch else "HEAD-detached"
    base_ref = args.base_ref or current_branch
    worktree_path = (
        Path(args.worktree_path).expanduser().resolve()
        if args.worktree_path
        else repo_root.parent / f"{repo_root.name}-{safe_branch_slug(args.new_branch)}"
    )
    missing = [rel for rel in STANDARD_DOCS if not (repo_root / rel).exists()]
    present = [rel for rel in STANDARD_DOCS if (repo_root / rel).exists()]
    dirty_lines = [
        line
        for line in status.splitlines()
        if line and not line.startswith("## ")
    ]
    legacy_dir = (args.reference_dir or args.legacy_dir).strip("/").replace("\\", "/")

    worktree_cmd = (
        "git worktree add "
        f"{quote_ps(str(worktree_path))} "
        f"-b {quote_ps(args.new_branch)} "
        f"{quote_ps(base_ref)}"
    )

    report = {
        "ok": True,
        "mode": "read_only_plan",
        "project_root": str(repo_root),
        "current_branch": current_branch,
        "head_commit": head if head_rc == 0 else "待确认",
        "status_short_branch": status if status_rc == 0 else "待确认",
        "dirty": bool(dirty_lines),
        "dirty_entries": dirty_lines,
        "worktrees": worktrees.splitlines() if worktree_rc == 0 else [],
        "proposed": {
            "new_branch": args.new_branch,
            "base_ref": base_ref,
            "worktree_path": str(worktree_path),
            "source_reference_dir": legacy_dir,
            "legacy_archive_dir": legacy_dir,
            "worktree_command": worktree_cmd,
        },
        "standard_docs_present": present,
        "standard_docs_missing": missing,
        "extra_root_docs_files": root_docs_extras(repo_root),
        "existing_topic_dirs": topic_dirs(repo_root),
        "source_reference_readme_fields": [
            "source branch",
            "source commit",
            "captured on",
            "captured by",
            "status: reference only for this branch",
            "active branch",
            "branch-current-docs location",
            "boundary warning",
        ],
        "legacy_archive_readme_fields": [
            "source branch",
            "source commit",
            "captured on",
            "captured by",
            "status: reference only for this branch",
            "active branch",
            "branch-current-docs location",
            "boundary warning",
        ],
        "recommended_steps": [
            "Get explicit approval before creating the worktree/branch.",
            "Create the new worktree instead of switching the current checkout.",
            f"Preserve useful source docs under {legacy_dir}/ with provenance.",
            "Use init-research-project-docs/refactor-research-project-docs to create branch-current root docs.",
            "Mark source-branch facts as reference-only until reverified in the active branch.",
            "Validate with audit_research_docs.py and git diff before commit.",
        ],
        "requires_confirmation": [
            "creating branch/worktree",
            "moving or copying docs into the source-reference directory",
            "replacing root AGENTS.md or docs entry files",
            "committing or pushing",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
