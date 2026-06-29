---
name: refactor-research-project-docs
description: "Audit and refactor existing academic or experimental repository documentation without losing evidence. Use when a user asks to clean up, slim down, standardize, split, migrate, or align old research docs with AGENTS.md plus docs/COMMANDS.md, DOC_TEMPLATES.md, FILE_MAP.md, HANDOFF.md, RESEARCH_LOG.md, SCOPE.yml, and WRONG_TURNS.md; especially when root docs are too long, responsibilities are mixed, historical logs pollute current status, or a new agent window cannot tell what to do next."
---

# Refactor Research Project Docs

Refactor an existing research documentation system into a compact, evidence-aware handoff structure. Preserve facts, metrics, failed attempts, output paths, and uncertainty labels; move or summarize content instead of deleting it.

## First-turn contract

When this skill is invoked, act as a documentation refactor operator, not a generic editor.

1. Resolve the target project root from the user request or current working directory.
2. If the target is a Git repository, run:

   ```powershell
   git status --short --branch
   git rev-parse --show-toplevel
   ```

   Report branch, root, and dirty files. Treat all pre-existing changes as user-owned.
3. If `docs/SCOPE.yml` exists, read it before proposing writes. If the Git root or write boundary differs from the requested target, stop and ask for confirmation.
4. Run a read-only audit before editing. Prefer the bundled script:

   ```powershell
   python scripts/audit_research_docs.py --project-root <PROJECT_ROOT>
   ```

5. Produce a short refactor plan before writing. Include:
   - root docs that are too long or have mixed responsibilities;
   - duplicated current state, baseline, commands, or paths;
   - long historical sections that should move to `docs/<topic>/` or `experiments/<date>-<name>/`;
   - missing startup report, single-source-of-truth rules, conversation-capture rules, or task-card templates;
   - files you intend to edit or create.
6. If the plan moves large content, rewrites established docs, or touches anything outside the documented writable scope, ask for explicit approval before editing.
7. After edits, validate structure and report remaining `待确认` items. Do not claim an experiment result was validated unless durable evidence supports it.

## Target documentation model

Keep the long-term root control plane small and role-specific:

```text
AGENTS.md
docs/COMMANDS.md
docs/DOC_TEMPLATES.md
docs/FILE_MAP.md
docs/HANDOFF.md
docs/RESEARCH_LOG.md
docs/SCOPE.yml
docs/WRONG_TURNS.md
```

If one of these files is missing, either add it using the project’s existing style or ask whether to use `$init-research-project-docs` to initialize missing files. Do not overwrite established docs just to match a template.

## Single source of truth

- `AGENTS.md`: stable agent rules, reading order, evidence policy, Git safety, and workflow expectations. Do not maintain current experiment status here.
- `docs/SCOPE.yml`: write boundaries, protected assets, approval-required paths, and forbidden actions.
- `docs/HANDOFF.md`: current status, current best/baseline, blockers, next actions, and unresolved onboarding items.
- `docs/RESEARCH_LOG.md`: reproducible experiments, commands, inputs, outputs, metrics, conclusions, and decisions.
- `docs/COMMANDS.md`: stable or currently reusable commands only.
- `docs/FILE_MAP.md`: durable resource map: code roots, datasets, evaluators, model/checkpoint locations, output/log roots, manuscript roots, and evidence locations.
- `docs/WRONG_TURNS.md`: negative results, failed routes, evidence strength, stop reasons, and reconsideration conditions.
- `docs/DOC_TEMPLATES.md`: reusable snippets and optional task/experiment card templates.

When the same dynamic fact appears in multiple files, choose the canonical file above, keep the detailed record there, and replace other copies with short summaries and links.

## Conversation-to-doc capture

During a refactor, make sure the project has a rule for preserving user clarifications that matter for future work. The rule should say:

- record only project-relevant clarifications, not entire chats;
- route them to the correct single source of truth;
- mark `source: user clarification in chat`;
- mark evidence level as `用户口述 / 待确认` until supported by durable evidence;
- never present user recollection as a formal experiment result.

If old docs contain chat-derived facts without evidence boundaries, move or annotate them rather than deleting them. If the project has no place to park unresolved clarifications, add a compact section to `docs/HANDOFF.md`.

## Refactor workflow

### 1. Audit

Check for:

- line counts and scan cost for each root doc;
- missing root entry files;
- root `docs/` files outside the standard set;
- `待确认`, `TODO`, unresolved `{{PLACEHOLDER}}`, and machine-specific absolute paths;
- duplicated headings or repeated current-state sections;
- long command histories in `COMMANDS.md`;
- file inventories or evidence dumps in `FILE_MAP.md`;
- long historical narratives in `HANDOFF.md`;
- report-only, simulation, matched-sample, or chat-derived claims written as formal system gains;
- missing startup report format, missing single-source-of-truth rules, or missing conversation-capture rules in `AGENTS.md`;
- missing user-clarification / unresolved-background parking section in `HANDOFF.md`;
- missing task/experiment card templates in `DOC_TEMPLATES.md`.

### 2. Classify content before moving

Use these destinations:

| Content type | Canonical destination |
| --- | --- |
| Current state, current best, blocker, next action | `docs/HANDOFF.md` |
| Experiment command, output, metrics, conclusion, decision | `docs/RESEARCH_LOG.md` or `experiments/<date>-<name>/` |
| Stable command likely to be reused | `docs/COMMANDS.md` |
| One-off batch command | related experiment or topic directory |
| Code/dataset/evaluator/output/paper path map | `docs/FILE_MAP.md` |
| Failed route or evidence-insufficient idea | `docs/WRONG_TURNS.md` |
| Long reconstruction, lineage, claim audit, paper rewrite, batch history | `docs/<topic>/` |
| Long-running future task | `experiments/<date>-<name>/` task card pack |

### 3. Plan edits

Prefer small, reviewable batches:

1. add startup report, single-source-of-truth, and conversation-capture rules to `AGENTS.md`;
2. make `HANDOFF.md` current-status only;
3. move long historical sections into topic directories with links back;
4. trim `COMMANDS.md` to stable/current commands;
5. make `FILE_MAP.md` an index, not a full evidence dump;
6. preserve negative results in `WRONG_TURNS.md`;
7. add user-clarification and task-card templates to `DOC_TEMPLATES.md`.

Do not combine all steps into one large rewrite unless the user explicitly asks.

### 4. Edit safely

- Preserve evidence before summarizing: metrics, commands, output paths, dates, seeds, dataset/split, checkpoint paths, negative results, and `待确认` labels.
- Move content rather than deleting facts. Leave a summary and link in the source document.
- Prefer relative paths. Keep absolute paths only when required for reproducibility, and label them as machine-specific or historical when appropriate.
- Do not modify datasets, ground truth, model weights, checkpoints, official evaluation outputs, large binaries, or unrelated code.
- Do not use destructive Git operations.
- If the repository is dirty, avoid overlapping user-owned edits unless the user approves the exact files.

### 5. Validate

Run or perform:

```powershell
python scripts/audit_research_docs.py --project-root <PROJECT_ROOT>
git diff -- AGENTS.md docs
git status --short --branch
```

Confirm:

- root docs have distinct responsibilities;
- moved content still has reachable links;
- no evidence was silently deleted;
- current state is in `HANDOFF.md`, not scattered;
- commands are verified or marked `待确认`;
- claims cite durable evidence or are explicitly bounded;
- remaining unknowns are listed as `待确认` with next actions.

## Startup report format

When handing off after a refactor, report:

```text
Project:
Git/root:
Docs refactor scope:
Files changed:
Content moved:
Evidence preserved:
Remaining unknowns:
Next action:
```

## Bundled resources

- `scripts/audit_research_docs.py`: read-only audit of root research docs, line counts, missing files, placeholders, root-doc extras, and common structure issues.
