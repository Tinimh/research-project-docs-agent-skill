# Research Project Docs Agent Skills

[中文说明](README_CN.md)

A cross-agent skill set for initializing, refactoring, and branch-aware research-route documentation with evidence-aware handoff rules, reproducible experiment records, safe write boundaries, and guided project onboarding.

The repository root remains the installable `init-research-project-docs` skill for backward compatibility. Companion skills live under `skills/`.

## Included skills

| Skill | Location | Use it when |
| --- | --- | --- |
| `init-research-project-docs` | repository root | Starting a new research project or adding the standard docs control plane |
| `refactor-research-project-docs` | `skills/refactor-research-project-docs/` | Cleaning up, slimming, splitting, or standardizing existing old research docs |
| `migrate-research-docs-branch` | `skills/migrate-research-docs-branch/` | Preparing branch-local docs for a custom research-route branch while keeping main docs as reference |

The portable core of each skill is its `SKILL.md`, `scripts/`, and optional `assets/`. `agents/openai.yaml` provides optional OpenAI/Codex UI metadata and may be ignored by other agents.

## Features

- Creates a compact documentation control plane for academic and experimental repositories.
- Protects datasets, labels, checkpoints, official ground truth, historical outputs, and large binaries by default.
- Separates current status, commands, file maps, research logs, and negative results.
- Uses `待确认` for unknown facts instead of inventing commands, metrics, or conclusions.
- Starts a guided post-initialization interview and writes answers back into durable project documentation.
- Captures project-relevant user clarifications from chat with source and evidence-level labels.
- Gives new agent windows a fixed startup report format so they can state project status and next action clearly.
- Provides optional task/experiment cards for long-running or cross-window research work.
- Supports safe preview, conflict detection, missing-file initialization, explicit overwrite, and validation.
- Audits old root docs before refactoring and reports missing files, overlong docs, duplicate responsibilities, missing conversation-capture rules, absolute paths, placeholders, and evidence-boundary risks.
- Plans branch-aware docs for custom research-route branches without switching branches or rewriting docs until explicitly approved.

## Generated files

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

| File | Responsibility |
| --- | --- |
| `AGENTS.md` | Agent workflow, evidence rules, Git safety, and documentation policy |
| `docs/SCOPE.yml` | Default writable, read-only, and confirmation-required boundaries |
| `docs/HANDOFF.md` | Current status, baseline/best, blockers, next steps, and onboarding checklist |
| `docs/RESEARCH_LOG.md` | Reproducible experiments, metrics, conclusions, and decisions |
| `docs/COMMANDS.md` | Stable and currently reusable commands |
| `docs/FILE_MAP.md` | Durable project entrypoints and evidence locations |
| `docs/WRONG_TURNS.md` | Negative results, stop reasons, and reconsideration conditions |
| `docs/DOC_TEMPLATES.md` | Copy-ready records for future experiments and topic directories |

## Installation

### Agent Skill-aware tools

Clone the repository into the skills directory supported by your agent, using `init-research-project-docs` as the installed folder name when the platform requires the folder to match the skill name.

Codex example on Windows:

```powershell
git clone https://github.com/Tinimh/research-project-docs-agent-skill.git `
  "$env:USERPROFILE\.codex\skills\init-research-project-docs"
```

Codex example on macOS or Linux:

```bash
git clone https://github.com/Tinimh/research-project-docs-agent-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/init-research-project-docs"
```

For Claude Code, Trae, or another agent, verify the skill discovery directory supported by the installed version. If automatic discovery is unavailable, explicitly ask the agent to read this repository's `SKILL.md` and follow it. Do not assume every agent automatically loads `AGENTS.md`.

To install companion skills into Codex after cloning this repository:

```powershell
Copy-Item `
  -Recurse `
  -LiteralPath .\skills\refactor-research-project-docs `
  -Destination "$env:USERPROFILE\.codex\skills\refactor-research-project-docs"

Copy-Item `
  -Recurse `
  -LiteralPath .\skills\migrate-research-docs-branch `
  -Destination "$env:USERPROFILE\.codex\skills\migrate-research-docs-branch"
```

## Usage with an agent

Initialize a new project:

```text
Use $init-research-project-docs in this repository: inspect git/root, preview the eight-file docs init, generate without overwriting, report the startup summary, then ask the first three onboarding questions.
```

Refactor existing old docs:

```text
Use $refactor-research-project-docs to audit this existing research repository docs, propose a safe refactor plan, then apply approved documentation-only changes.
```

Plan branch-aware docs for a custom research-route branch:

```text
Use $migrate-research-docs-branch to plan branch-aware docs for my custom research-route branch: preserve source docs as reference, keep branch-local docs current, and do not change state before approval.
```

The agent should:

1. inspect the Git root, branch, and existing changes;
2. discover cheap repository facts and preview the initialization;
3. generate the documentation without silently overwriting existing files;
4. report the fixed startup summary fields;
5. ask the first three onboarding questions instead of stopping at a generic clarification;
6. write the answers into the appropriate long-term documents;
7. validate the generated document set and report remaining `待确认` items.

## Direct script usage

Preview without writing:

```powershell
python scripts/init_research_project_docs.py `
  --project-root <PROJECT_ROOT> `
  --project-name "My Research Project" `
  --research-goal "Test whether method A improves outcome B" `
  --primary-metrics "accuracy, latency" `
  --code-root src `
  --data-dir data `
  --output-dir outputs `
  --log-dir run_logs `
  --dry-run
```

Generate after reviewing the preview:

```powershell
python scripts/init_research_project_docs.py `
  --project-root <PROJECT_ROOT> `
  --project-name "My Research Project" `
  --research-goal "Test whether method A improves outcome B" `
  --primary-metrics "accuracy, latency"
```

Validate an initialized project:

```powershell
python scripts/init_research_project_docs.py --project-root <PROJECT_ROOT> --check
```

Audit existing docs before refactoring:

```powershell
python skills/refactor-research-project-docs/scripts/audit_research_docs.py `
  --project-root <PROJECT_ROOT>
```

Plan branch-aware route docs without writing:

```powershell
python skills/migrate-research-docs-branch/scripts/plan_docs_branch_migration.py `
  --project-root <PROJECT_ROOT> `
  --new-branch <CUSTOM_RESEARCH_BRANCH> `
  --reference-dir docs/branch_reference/main
```

Existing-file policies:

- `error` — default; abort before writing if any managed file already exists.
- `skip` — create only missing managed files.
- `overwrite` — replace all managed files; use only after explicit approval and review.

## Repository structure

```text
SKILL.md                                      # init-research-project-docs
agents/openai.yaml
assets/templates/
scripts/init_research_project_docs.py
skills/refactor-research-project-docs/
  SKILL.md
  agents/openai.yaml
  scripts/audit_research_docs.py
skills/migrate-research-docs-branch/
  SKILL.md
  agents/openai.yaml
  scripts/plan_docs_branch_migration.py
```

## Validation

The release is checked with the skill validator and a temporary-project smoke test covering:

- generation of all eight managed files;
- unresolved-placeholder detection;
- YAML parsing of `docs/SCOPE.yml`;
- post-initialization question output;
- default conflict protection;
- read-only old-docs audit for the companion refactor skill;
- read-only branch-aware route-doc planning for the companion branch-migration skill.

## License

[MIT](LICENSE)
