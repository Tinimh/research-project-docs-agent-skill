---
name: init-research-project-docs
description: "Initialize a new academic or experimental code repository with a safe, evidence-aware documentation system: AGENTS.md plus docs/COMMANDS.md, DOC_TEMPLATES.md, FILE_MAP.md, HANDOFF.md, RESEARCH_LOG.md, SCOPE.yml, and WRONG_TURNS.md. Use when a user asks an AI coding agent or a new Codex/agent window to scaffold, bootstrap, standardize, or audit documentation for a research project, reproducible experiment repository, thesis codebase, or lab prototype; especially when the agent needs a concrete first-turn procedure, safe existing-file behavior, and a post-init onboarding interview."
---

# Initialize Research Project Docs

Create a compact documentation control plane for a research repository. Generate portable templates, then adapt them to evidence already present in the target repository without inventing commands, paths, metrics, or conclusions.

## First-turn contract

When this skill is invoked, do not answer with a generic “what should I do next?” question. Act as the initialization operator.

1. Resolve the target project root from the user request or current working directory. If only one plausible root exists, state that assumption and continue. If the Git root differs from the requested target, stop and ask for confirmation.
2. If the target is a Git repository, run the Git safety checks in the workflow below and report branch, root, and dirty files before writing.
3. Discover cheap durable facts from filenames and obvious repository metadata. Use `待确认` for unknowns; do not block initialization waiting for a perfect project brief.
4. Run the bundled script once with `--dry-run`, using verified facts and `待确认` placeholders.
5. If no managed files exist and the user asked to initialize, rerun without `--dry-run`. If conflicts exist, do not overwrite; report the conflicts and ask whether to skip existing files, audit/edit existing docs, or overwrite after explicit approval.
6. Report a compact startup summary with: `Project`, `Research goal`, `Git/root`, `Current baseline/best`, `Open unknowns`, `Safe writable scope`, and `Next action`.
7. After generation or safe skip, ask the first onboarding round instead of stopping. Start with exactly these three questions unless the answers are already known:
   - What is the exact research question or falsifiable hypothesis, and what result counts as success or failure?
   - Which dataset/split/sample scope, official evaluator, primary metrics, and baseline are authoritative?
   - Which datasets, labels, checkpoints, raw measurements, manuscripts, historical outputs, or external repos must remain read-only?
8. Write user answers back into the appropriate long-term documents. If the user defers an answer, keep `待确认` in the files and add a concrete next action in `docs/HANDOFF.md`.

## Output set

Create exactly these long-term entry files by default:

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

Keep detailed experiment artifacts under `experiments/` or a topic-specific subdirectory. Do not turn root `docs/` into a chronological dump.

## Single source of truth

Keep each durable fact in exactly one canonical place, then link or summarize it elsewhere.

- `AGENTS.md`: stable agent rules, reading order, evidence policy, Git safety, and workflow expectations. Do not maintain current experiment status here.
- `docs/SCOPE.yml`: write boundaries, protected assets, approval-required paths, and forbidden actions.
- `docs/HANDOFF.md`: current status, current best/baseline, blockers, next actions, and unresolved onboarding items.
- `docs/RESEARCH_LOG.md`: reproducible experiments, commands, inputs, outputs, metrics, conclusions, and decisions.
- `docs/COMMANDS.md`: stable or currently reusable commands only.
- `docs/FILE_MAP.md`: durable resource map: code roots, datasets, evaluators, model/checkpoint locations, output/log roots, manuscript roots, and evidence locations.
- `docs/WRONG_TURNS.md`: negative results, failed routes, evidence strength, stop reasons, and reconsideration conditions.
- `docs/DOC_TEMPLATES.md`: reusable snippets and optional task/experiment card templates.

Before adding repeated status, baseline, path, or command information to multiple files, update the canonical file and add a short pointer from the other file. Avoid parallel copies of the same current state.

## Conversation-to-doc capture

Capture user clarifications from the chat when they affect future agent decisions. Do not write every conversation turn into the repository.

Record a clarification when the user provides or corrects:

- current status, blockers, priorities, next actions, or deadlines;
- dataset/split/evaluator/metric/baseline facts;
- paths for code, data, checkpoints, outputs, logs, papers, or external repositories;
- assets that must remain read-only or require explicit approval;
- historical decisions, failed routes, stop reasons, or reconsideration conditions;
- environment, command, branch/worktree, or workflow conventions.

Route each clarification to the canonical file from the single-source-of-truth rules. Mark `source: user clarification in chat` and use evidence level `用户口述 / 待确认` unless the repository contains durable supporting evidence. Never turn a user recollection into a formal experimental result without commands, outputs, metrics, and an evidence path.

## Workflow

### 1. Inspect before writing

Resolve the target project root. If it is a Git repository, run:

```powershell
git status --short --branch
git rev-parse --show-toplevel
```

Report the branch, worktree root, and existing changes. Treat all pre-existing changes as user-owned. If the resolved Git root differs from the requested target, stop and ask for confirmation.

Check whether any output file already exists. For an existing repository, start with `--dry-run` and use `--existing-policy skip` only when the user wants missing files added. Never overwrite existing documentation without explicit user approval.

### 2. Gather only durable project facts

Determine or ask for:

- project name;
- one-sentence research goal;
- primary metric or evaluation criterion;
- code root;
- dataset path;
- generated-output path;
- run-log path;
- communication language and default shell.

Discover cheap facts from the repository when possible. Mark unknown facts as `待确认`; do not fabricate environment names, installation commands, checkpoints, datasets, results, or evaluation protocols.

### 3. Preview the initialization

Run the bundled script from this skill directory:

```powershell
python scripts/init_research_project_docs.py `
  --project-root <PROJECT_ROOT> `
  --project-name "<PROJECT_NAME>" `
  --research-goal "<ONE_SENTENCE_GOAL>" `
  --primary-metrics "<METRIC_OR_待确认>" `
  --code-root "<CODE_ROOT>" `
  --data-dir "<DATA_DIR>" `
  --output-dir "<OUTPUT_DIR>" `
  --log-dir "<LOG_DIR>" `
  --dry-run
```

Review the JSON plan. The default existing-file policy is `error`, so a conflict aborts before any file is written.

### 4. Generate safely

After the preview is correct, rerun without `--dry-run`.

Use one of these policies deliberately:

- `--existing-policy error`: safest default; write nothing if any target exists.
- `--existing-policy skip`: create only missing files; preserve all existing files.
- `--existing-policy overwrite`: replace the eight managed files. Use only after explicit user approval and after reviewing the diff or backup strategy.

Do not use overwrite merely to “refresh” an established project. For an established repository, perform a document audit and edit surgically.

### 5. Run the post-initialization onboarding interview

Do not stop immediately after reporting that the files were generated. If the user is available, proactively collect the unresolved project facts and use the answers to finish the first useful version of the documentation.

Ask only 3–5 short questions at a time. Start with the highest-impact unknowns and avoid asking for facts that can be discovered cheaply from repository files. Cover these groups across one or more rounds:

1. **Research contract**: What exact question or hypothesis is being tested? What observable result counts as success or failure?
2. **Evaluation contract**: Which dataset, split, sample scope, official evaluator, primary metrics, statistical repeats, and comparison baseline are authoritative?
3. **Asset protection**: Which datasets, labels, checkpoints, raw measurements, manuscripts, historical outputs, or external repositories must remain read-only?
4. **Reproduction contract**: What environment, installation command, runner, config, seed, model/checkpoint, evaluation command, hardware constraint, and expected runtime are required?
5. **Repository map**: Which files are the actual training, inference, analysis, and evaluation entrypoints? Where should outputs, logs, and experiment records go?
6. **Workflow contract**: Which branch/worktree convention, review rule, and long-run approval boundary should agents follow?
7. **Current state**: Is there already a baseline, current best, known blocker, failed route, paper deadline, or next experiment that should be recorded?

Use a conversational intake, not a questionnaire dump. Explain briefly why a question changes the generated policy when that is not obvious. Accept partial answers; preserve unknowns as `待确认` and keep an explicit checklist in `docs/HANDOFF.md`.

After each answer batch, update the relevant files rather than leaving the information only in chat:

- research goal and success criteria -> `AGENTS.md`, `HANDOFF.md`, `RESEARCH_LOG.md`;
- evaluator, metrics, baseline, and commands -> `COMMANDS.md`, `RESEARCH_LOG.md`, `HANDOFF.md`;
- protected assets and approval boundaries -> `SCOPE.yml`, `AGENTS.md`;
- entrypoints and durable paths -> `FILE_MAP.md`;
- known failed routes -> `WRONG_TURNS.md`;
- next experiment and blockers -> `HANDOFF.md`.

If a user clarification is useful but not yet backed by durable evidence, add a short entry to `docs/HANDOFF.md` with source, impact, evidence level, and the next confirmation action.

Finish the onboarding phase only when the user says the remaining unknowns can stay deferred, or when every high-risk unknown is either answered or explicitly marked `待确认` with a next action.

### 6. Adapt the generated files

Inspect the repository and replace generic rows with verified facts:

- In `AGENTS.md`, set the actual project nature, required reading order, evidence rules, and verification workflow.
- In `docs/SCOPE.yml`, narrow writable paths and explicitly protect datasets, official ground truth, checkpoints, model weights, historical outputs, and large binaries.
- In `docs/HANDOFF.md`, keep only current status, current best/baseline, blockers, next steps, and links to detailed history.
- In `docs/RESEARCH_LOG.md`, record reproducible experiments with commands, inputs, outputs, metrics, conclusions, and decisions.
- In `docs/COMMANDS.md`, retain stable or current commands; move one-off batch commands into their experiment or topic directory.
- In `docs/FILE_MAP.md`, index durable entrypoints and evidence locations; do not inventory every generated file.
- In `docs/WRONG_TURNS.md`, preserve negative results, evidence strength, stop reasons, and reconsideration conditions.
- In `docs/DOC_TEMPLATES.md`, keep reusable record snippets aligned with the project’s actual metric schema.

Prefer relative paths. Keep machine-specific absolute paths only when required for reproducibility, and label historical or uncertain paths.

For a non-trivial experiment or research task, suggest using the task card pack in `docs/DOC_TEMPLATES.md` under `experiments/YYYY-MM-DD-short-name/`. Do not create every task-card file mechanically; create only the pieces needed for the task’s risk and duration.

### 7. Validate

Run:

```powershell
python scripts/init_research_project_docs.py --project-root <PROJECT_ROOT> --check
```

Then inspect:

```powershell
git diff -- AGENTS.md docs
git status --short --branch
```

Confirm that:

- all eight entry files exist;
- no unresolved `{{PLACEHOLDER}}` tokens remain;
- no pre-existing evidence was overwritten unexpectedly;
- `SCOPE.yml` matches real repository paths;
- commands are verified or marked `待确认`;
- result claims point to durable evidence;
- current status is not mixed with long historical reconstruction.

## Evidence hierarchy

Use this default order and tailor it to the field:

1. official evaluation reports, raw measurements, diagnostics, and run manifests;
2. code, configuration, scripts, environment lockfiles, and version-control history;
3. manuscript drafts and maintained project documentation;
4. meeting notes, chat reconstruction, and user recollection;
5. inference.

Never present simulation, report-only analysis, matched-sample analysis, or chat history as a formal system gain unless the project’s official evaluation reproduces it.

## Growth guardrails

Treat these as prompts to split, not hard limits:

- `HANDOFF.md`: aim for 150–250 lines;
- `COMMANDS.md`: keep only commands likely to be reused;
- `FILE_MAP.md`: keep an index, not an evidence dump;
- `RESEARCH_LOG.md`: move long method-specific histories to `docs/<topic>/` or `experiments/<date>-<name>/`;
- `WRONG_TURNS.md`: split by topic when scanning becomes difficult.

When moving content, preserve facts, metrics, output paths, negative results, uncertainty labels, and evidence boundaries. Leave a concise summary and link in the root document.

## Cross-agent portability

Treat `SKILL.md`, `scripts/`, and `assets/` as the portable core. Any coding agent that can read these instructions and execute Python can use the workflow, even when it does not auto-discover Agent Skills.

- Install the folder in the agent's current supported skills directory, or explicitly ask the agent to read this `SKILL.md`.
- Treat `agents/openai.yaml` as optional OpenAI/Codex UI metadata. Other agents may ignore it safely.
- Do not assume every agent automatically reads generated `AGENTS.md`. When needed, add a minimal native instruction file for that agent that points back to `AGENTS.md` and the root `docs/` entry files.
- Verify platform-specific discovery paths against the installed agent version. Mark an unverified path or invocation rule as `待确认` instead of guessing.
- Keep the generated research documentation platform-neutral; do not introduce agent-specific policy unless the target project requests it.

## Bundled resources

- `scripts/init_research_project_docs.py`: render, preview, safely write, and validate the document set.
- `assets/templates/`: UTF-8 templates copied into the target project. Edit these assets when changing the generated contract.
