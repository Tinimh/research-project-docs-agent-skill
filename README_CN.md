# 科研项目文档 Agent Skills

[English](README.md)

这是一组跨 agent 使用的科研项目文档 skills，用于初始化新项目文档体系，也用于审计、瘦身和重构已有老文档。

仓库根目录仍保持为可直接安装的 `init-research-project-docs` skill，以兼容之前的安装方式。配套的 `refactor-research-project-docs` skill 放在 `skills/refactor-research-project-docs/`。

## 包含的 skills

| Skill | 位置 | 使用场景 |
| --- | --- | --- |
| `init-research-project-docs` | 仓库根目录 | 新科研项目初始化，或补齐标准文档控制面 |
| `refactor-research-project-docs` | `skills/refactor-research-project-docs/` | 清理、瘦身、拆分和标准化已有老文档 |

每个 skill 的可移植核心是自己的 `SKILL.md`、`scripts/` 和可选 `assets/`。`agents/openai.yaml` 仅提供可选的 OpenAI/Codex UI 元数据，其他 agent 可以安全忽略。

## 主要能力

- 为学术研究和实验型代码仓库创建紧凑的长期文档控制面。
- 默认保护 dataset、label、checkpoint、official ground truth、历史输出和大体积二进制文件。
- 分离当前状态、可复用命令、文件地图、研究日志和负结果记录。
- 对未知事实使用 `待确认`，不编造环境、命令、指标或研究结论。
- 初始化后主动进行项目访谈，并把用户回答写回长期文档。
- 把聊天中影响项目判断的用户澄清记录到文档，并标注来源和证据等级。
- 为新 agent 窗口提供固定启动汇报格式，明确项目状态和下一步动作。
- 为跨窗口或长周期科研任务提供可选任务 / 实验卡片模板。
- 支持 dry-run、冲突检测、仅补缺失文件、显式覆盖和完整性检查。
- 对老项目根级文档做只读审计，报告缺失文件、过长文档、职责重复、缺少用户澄清记录规则、绝对路径、占位符和证据边界风险。

## 生成文件

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

| 文件 | 职责 |
| --- | --- |
| `AGENTS.md` | Agent 工作流、证据规则、Git 安全和文档规范 |
| `docs/SCOPE.yml` | 默认可写、只读和需要确认的路径边界 |
| `docs/HANDOFF.md` | 当前状态、baseline/best、卡点、下一步和初始化清单 |
| `docs/RESEARCH_LOG.md` | 可复现实验、指标、结论和研究决策 |
| `docs/COMMANDS.md` | 稳定且仍会复用的命令 |
| `docs/FILE_MAP.md` | 长期项目入口和证据位置 |
| `docs/WRONG_TURNS.md` | 负结果、停止原因和重新考虑条件 |
| `docs/DOC_TEMPLATES.md` | 可复制的实验与专题文档模板 |

## 安装

### 支持 Agent Skill 的工具

把仓库克隆到目标 agent 当前支持的 skills 目录。如果平台要求目录名与 skill name 一致，请把安装目录命名为 `init-research-project-docs`。

Codex Windows 示例：

```powershell
git clone https://github.com/Tinimh/research-project-docs-agent-skill.git `
  "$env:USERPROFILE\.codex\skills\init-research-project-docs"
```

Codex macOS / Linux 示例：

```bash
git clone https://github.com/Tinimh/research-project-docs-agent-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/init-research-project-docs"
```

Claude Code、Trae 或其他 agent 的自动发现目录可能随版本变化，请以当前版本文档为准。如果不支持自动发现，可以明确要求 agent 读取本仓库的 `SKILL.md` 并按其执行。不要假设所有 agent 都会自动加载 `AGENTS.md`。

克隆本仓库后，如需把配套重构 skill 安装到 Codex：

```powershell
Copy-Item `
  -Recurse `
  -LiteralPath .\skills\refactor-research-project-docs `
  -Destination "$env:USERPROFILE\.codex\skills\refactor-research-project-docs"
```

## 通过 agent 使用

初始化新项目：

```text
Use $init-research-project-docs in this repository: inspect git/root, preview the eight-file docs init, generate without overwriting, report the startup summary, then ask the first three onboarding questions.
```

重构已有老文档：

```text
Use $refactor-research-project-docs to audit this existing research repository docs, propose a safe refactor plan, then apply approved documentation-only changes.
```

Agent 应当：

1. 检查 Git 根目录、分支和已有改动；
2. 从仓库中发现容易确认的事实，并先预览初始化计划；
3. 安全生成文档，不静默覆盖现有文件；
4. 输出固定启动汇报字段；
5. 主动询问首轮 3 个高影响项目问题，而不是停在泛泛澄清；
6. 把回答写入对应长期文档；
7. 验证生成结果并报告剩余的 `待确认` 项。

## 直接运行脚本

只预览，不写文件：

```powershell
python scripts/init_research_project_docs.py `
  --project-root <PROJECT_ROOT> `
  --project-name "我的科研项目" `
  --research-goal "验证方法 A 是否改善结果 B" `
  --primary-metrics "accuracy, latency" `
  --code-root src `
  --data-dir data `
  --output-dir outputs `
  --log-dir run_logs `
  --dry-run
```

确认预览后生成：

```powershell
python scripts/init_research_project_docs.py `
  --project-root <PROJECT_ROOT> `
  --project-name "我的科研项目" `
  --research-goal "验证方法 A 是否改善结果 B" `
  --primary-metrics "accuracy, latency"
```

检查已经初始化的项目：

```powershell
python scripts/init_research_project_docs.py --project-root <PROJECT_ROOT> --check
```

重构前只读审计老文档：

```powershell
python skills/refactor-research-project-docs/scripts/audit_research_docs.py `
  --project-root <PROJECT_ROOT>
```

已有文件策略：

- `error`：默认策略；只要存在受管理文件，就在写入前整体停止。
- `skip`：只创建缺失文件，保留所有现有文件。
- `overwrite`：替换全部受管理文件；必须在明确批准和审查后使用。

## 仓库结构

```text
SKILL.md                                      # init-research-project-docs
agents/openai.yaml
assets/templates/
scripts/init_research_project_docs.py
skills/refactor-research-project-docs/
  SKILL.md
  agents/openai.yaml
  scripts/audit_research_docs.py
```

## 验证

发布版本通过 skill validator 和临时项目 smoke test，检查内容包括：

- 八个受管理文件全部生成；
- 未替换占位符检测；
- `docs/SCOPE.yml` YAML 解析；
- 初始化后主动问题输出；
- 默认冲突保护；
- 配套重构 skill 的只读老文档审计。

## License

[MIT](LICENSE)
