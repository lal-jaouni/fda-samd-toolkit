# Project: {{PROJECT_NAME}}

## Overview
{{PROJECT_DESCRIPTION}}

## Commands
```bash
make lint        # Auto-fix lint issues (ruff check --fix .)
make format      # Auto-format code (ruff format .)
make typecheck   # Type check (pyright)
make test        # Run tests with JSON report (pytest --json-report)
make check       # Run all of the above
make security    # Run security scan (bandit)
```

## Architecture
- Source code: `src/`
- Tests: `tests/` (mirror src/ structure)
- Decisions: `docs/decisions/` (ADRs — one per file, numbered)
- Scripts: `scripts/` (standalone utilities)

## NAS Storage
TrueNAS NFS shares are mounted on the VM:
- `/mnt/nas/SharedDrive` — General project storage, large datasets, backups (11TB)
- `/mnt/nas/Media` — Media files (11TB)
- `/mnt/nas/Docker` — Container/Docker persistent data (11TB)

Use `/mnt/nas/SharedDrive/{{PROJECT_NAME}}/` for large data that shouldn't live in git (datasets, caches, model artifacts, bulk exports). Keep source code in the workspace git repo.

## Agent Team Rules

### Research First
Before choosing ANY library, framework, or tool, search for the latest best option. Do NOT rely on training data. Search for "[tool] vs alternatives 2026" before committing to a dependency. Prefer tools with active development, recent releases, and strong community.

### Work Decomposition
- The team lead assesses task complexity and spawns the right team dynamically
- Each teammate works in an isolated worktree (own branch, own files)
- Define interfaces/contracts between components BEFORE parallel implementation
- Break work into 5-10 minute atomic subtasks with clear deliverables

### File Ownership
- Each teammate owns specific files/directories — NO two agents edit the same file
- If a shared interface needs changing, the team lead coordinates the change
- Use the interface-first approach: agree on API contracts, then build independently

### Quality Gates (Enforced by Hooks)
- Every file edit auto-triggers ruff format + lint (PostToolUse hook)
- Tests must pass before any task can be marked complete (TaskCompleted hook)
- Destructive bash commands are blocked (PreToolUse hook)
- `make check` must pass before any commit

### Decision Making
- **One-way door** (irreversible: DB schema, public API, core data model): Write an ADR in docs/decisions/, get team lead approval
- **Two-way door** (reversible: internal implementation, feature flags): Decide quickly with ~70% confidence

### Code Standards
- Type hints on all function signatures
- Docstrings only on public API (not internal helpers)
- Tests for every public function — use AAA pattern (Arrange-Act-Assert)
- No secrets in code — use environment variables
- Parameterized queries for all database operations
- All inputs validated server-side

### Git Workflow
- Feature branches from main
- Small, focused commits (one logical change per commit)
- PR description explains what and why
- CI must pass before merge

### Project Management (GitHub Issues)
All task tracking uses GitHub Issues with standardized labels:
- **Priority**: P0-urgent, P1-high, P2-normal, P3-low
- **Status**: in-progress, blocked, needs-review
- **Type**: feature, bug, research, infra, enhancement
- **Milestones**: one per sprint/phase, track completion %
- Reference issues in commits: "Closes #42" auto-closes the issue
- Agent creates issues for planned work and closes them on completion
- Weekly: `gh search issues --owner lal-jaouni --state open` for full backlog

## Available Agent Roles
The team lead selects from `.claude/agents/` based on task needs:

### Engineering
- **team-lead**: Architecture, work decomposition, coordination
- **backend**: APIs, services, data access, resilience
- **frontend**: UI components, accessibility, performance
- **data-engineer**: Pipelines, ETL, data quality
- **ml-engineer**: Models, training, evaluation, MLOps
- **db-architect**: Schema design, migrations, query optimization
- **devops**: CI/CD, infrastructure, deployment
- **api-designer**: API contracts, documentation, versioning
- **performance**: Profiling, optimization, benchmarking
- **debugger**: Root cause analysis, systematic debugging
- **security**: Vulnerability review, OWASP compliance

### Quality & Documentation
- **tester**: Test writing, coverage, mutation testing
- **reviewer**: Code review following Google's standards
- **tech-writer**: Documentation, API docs, user guides
- **ui-designer**: Component design, accessibility, responsive

### Research & Analysis
- **researcher**: Investigation, hypothesis-driven analysis
- **quantitative-analyst**: Financial modeling, signal scoring, risk assessment
- **financial-researcher**: SEC filings, earnings, industry research
- **market-analyst**: Market research, opportunity identification, trend detection
- **competitive-intelligence**: Competitor tracking, SWOT, differentiation strategy

### Business & Strategy
- **product-manager**: Requirements, prioritization, user stories
- **business-strategist**: Business model design, pricing, revenue planning
- **go-to-market**: Launch strategy, customer acquisition, outreach, growth
