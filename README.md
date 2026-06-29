# Research Project Docs Agent Skill

[中文说明](README_CN.md)

A cross-agent skill for initializing research repositories with evidence-aware documentation, reproducible experiment records, safe write boundaries, and guided project onboarding.

The portable core is `SKILL.md`, `scripts/`, and `assets/`. `agents/openai.yaml` provides optional OpenAI/Codex UI metadata and may be ignored by other agents.

## Features

- Creates a compact documentation control plane for academic and experimental repositories.
- Protects datasets, labels, checkpoints, official ground truth, historical outputs, and large binaries by default.
- Separates current status, commands, file maps, research logs, and negative results.
- Uses `待确认` for unknown facts instead of inventing commands, metrics, or conclusions.
- Starts a guided post-initialization interview and writes answers back into durable project documentation.
- Supports safe preview, conflict detection, missing-file initialization, explicit overwrite, and validation.

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

## Usage with an agent

Example request:

```text
Use $init-research-project-docs in this repository: inspect git/root, preview the eight-file docs init, generate without overwriting, then ask the first three onboarding questions.
```

The agent should:

1. inspect the Git root, branch, and existing changes;
2. discover cheap repository facts and preview the initialization;
3. generate the documentation without silently overwriting existing files;
4. ask the first three onboarding questions instead of stopping at a generic clarification;
5. write the answers into the appropriate long-term documents;
6. validate the generated document set and report remaining `待确认` items.

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

Existing-file policies:

- `error` — default; abort before writing if any managed file already exists.
- `skip` — create only missing managed files.
- `overwrite` — replace all managed files; use only after explicit approval and review.

## Repository structure

```text
SKILL.md
agents/openai.yaml
assets/templates/
scripts/init_research_project_docs.py
```

## Validation

The release is checked with the skill validator and a temporary-project smoke test covering:

- generation of all eight managed files;
- unresolved-placeholder detection;
- YAML parsing of `docs/SCOPE.yml`;
- post-initialization question output;
- default conflict protection.

## License

[MIT](LICENSE)
