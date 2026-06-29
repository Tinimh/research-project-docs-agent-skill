---
name: migrate-research-docs-branch
description: "Plan and execute safe branch-aware documentation for a custom research-route branch. Use when a user is creating or working in another scientific route branch whose files, scripts, metrics, or docs differ from main/master, and needs branch-local current docs while preserving main-branch docs as reference material for comparison and future merge. Supports custom branch names, separate worktrees, source-doc reference archives, branch/commit provenance, and safeguards against mixing main-branch reality with route-branch reality."
---

# Migrate Research Docs Branch

Create branch-aware documentation for an existing research project. The branch may be for a new scientific route, not merely for documentation cleanup. The goal is to make root docs accurate for the active branch while preserving source-branch docs as labeled reference material for comparison and future merge.

## First-turn contract

When this skill is invoked, do not directly switch branches or rewrite docs. Start with a read-only migration plan.

1. Resolve the target project root.
2. Run Git preflight:

   ```powershell
   git status --short --branch
   git rev-parse --show-toplevel
   git branch --show-current
   git rev-parse HEAD
   git worktree list
   ```

3. If the worktree is dirty, do not create a new branch/worktree until the user confirms how to handle the existing changes.
4. Run the bundled read-only planner with the user’s intended branch name:

   ```powershell
   python scripts/plan_docs_branch_migration.py `
     --project-root <PROJECT_ROOT> `
     --new-branch <CUSTOM_RESEARCH_BRANCH>
   ```

5. Report the plan: source branch/commit, proposed route branch, proposed worktree path, source-doc reference directory, docs files to preserve as reference, and docs files to become branch-local current truth.
6. Ask for explicit approval before any state-changing action:
   - `git worktree add`;
   - creating a branch;
   - moving/copying docs into `docs/branch_reference/*` or another reference archive;
   - replacing root `AGENTS.md` or root `docs/` entry files;
   - committing or pushing.

## Target model

Use this end state:

```text
AGENTS.md                         # current rules for the new docs branch
docs/
  SCOPE.yml                       # current write boundary
  HANDOFF.md                      # current branch status
  RESEARCH_LOG.md                 # current branch experiments
  COMMANDS.md                     # current reusable commands
  FILE_MAP.md                     # current file/resource map
  WRONG_TURNS.md                  # current negative results
  DOC_TEMPLATES.md                # current templates
  branch_reference/
    main/                         # source-branch docs, reference only
    README.md
    AGENTS.md                     # optional snapshot if useful
    HANDOFF.md
    RESEARCH_LOG.md
    COMMANDS.md
    FILE_MAP.md
    WRONG_TURNS.md
    DOC_TEMPLATES.md
    SCOPE.yml
```

The root `AGENTS.md` and root `docs/` entry files are the current operational truth for this branch. `docs/branch_reference/*` is reference material for comparison, merge planning, and historical context; it is not current status for the active branch.

## Source-reference archive contract

Every source-reference archive needs a `README.md` with:

```md
# Source branch docs reference

- source branch:
- source commit:
- captured on:
- captured by:
- status: reference only for this branch
- current branch:
- branch-current-docs location: root `AGENTS.md` and root `docs/`

## Boundary

Do not treat metrics, commands, paths, current best, or next actions in this directory as valid for the active branch unless re-verified in the active branch and recorded in root docs.

## Useful legacy material

- ...
```

Preserve useful source-branch facts, metrics, output paths, failure notes, and `待确认` labels. Do not silently delete evidence just because it belongs to another branch.

## Migration workflow

### 1. Plan only

Use `plan_docs_branch_migration.py` to collect:

- current branch and commit;
- dirty worktree status;
- standard docs present/missing;
- extra root `docs/*.md|*.yml`;
- topic directories already under `docs/`;
- proposed `git worktree add` command;
- proposed source-reference directory;
- recommended next steps.

### 2. Create isolated worktree after approval

Prefer a separate worktree instead of switching the current dirty checkout:

```powershell
git worktree add <WORKTREE_PATH> -b <NEW_BRANCH> <BASE_BRANCH_OR_COMMIT>
```

Use the branch name that describes the research route. Examples:

```text
codex/rase-v8
codex/yolov6-recall-sweep
experiment/new-calibration-route
```

### 3. Preserve source docs in the route branch

In the new worktree only:

1. create `docs/branch_reference/<source-branch>/`;
2. copy old root docs into that directory when they are useful for comparison or merge planning;
3. create `docs/branch_reference/<source-branch>/README.md` with source branch, commit, capture date, and boundary warning;
4. leave no ambiguity that source-reference docs are not current operational truth for the active route branch.

### 4. Create new current docs

Use `$init-research-project-docs` for missing skeletons and `$refactor-research-project-docs` for existing content. The active branch docs should:

- include a fixed startup report;
- include single-source-of-truth rules;
- include conversation-to-doc capture rules;
- clearly state that source-reference docs are not current truth for this branch;
- keep branch-specific claims labeled with branch and commit;
- mark unverified source-branch facts as `待确认`.

### 5. Validate before commit

Run:

```powershell
python <PATH_TO_REFRACTOR_SKILL>/scripts/audit_research_docs.py --project-root <NEW_WORKTREE>
git -C <NEW_WORKTREE> diff -- AGENTS.md docs
git -C <NEW_WORKTREE> status --short --branch
```

Check:

- root docs are current-truth docs for the active branch, not source docs copied in disguise;
- source-reference archive has provenance and warning;
- old current best / commands / paths are not treated as current unless reverified;
- moved evidence is still reachable;
- no datasets, checkpoints, weights, ground truth, large binaries, or historical eval outputs were overwritten.

## Handoff report

After migration, report:

```text
Source branch:
Source commit:
Active branch:
New worktree:
Source-reference archive:
Branch-current docs:
Files moved/copied:
Evidence preserved:
Facts still source-branch-only:
Remaining 待确认:
Next action:
```

## Bundled resources

- `scripts/plan_docs_branch_migration.py`: read-only planner for a custom research-route branch/worktree documentation migration.
