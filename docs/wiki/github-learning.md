# GitHub Learning & Engineering Roadmap

This page defines the practical learning path for maintaining CryoOmega ULTRA as a disciplined GitHub engineering project.

## Goals

- Learn GitHub through the real repository rather than isolated exercises.
- Make repository structure, review, CI, security, releases, and agent workflows reproducible.
- Keep documentation technical and source-oriented.

## Current repository baseline

CryoOmega ULTRA is a public Python repository with CLI, TUI, and Web IDE components. Issues, Projects, Wiki, Pull Requests, and Discussions are enabled. GitHub Pages is not currently enabled.

## Learning levels

### Level 1 — Git and GitHub Core

Learn branches, commits, tags, issues, pull requests, reviews, Projects, milestones, releases, and artifacts.

Practice flow:

```text
issue → branch → commit → pull request → CI → review → merge → release
```

### Level 2 — Repository Engineering

Learn repository layout, contribution rules, CODEOWNERS, issue templates, PR templates, documentation navigation, and conventions.

Recommended targets:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/`
- `.github/ISSUE_TEMPLATE/`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `CODEOWNERS`

### Level 3 — CI and Testing

Learn GitHub Actions workflow structure, job boundaries, permissions, caching, matrices, artifacts, test reporting, and reusable workflows.

Minimum pipeline:

```text
lint → syntax/type checks → unit tests → integration checks → artifacts
```

### Level 4 — Security and Supply Chain

Learn least-privilege `GITHUB_TOKEN` permissions, dependency review, action pinning policy, secret handling, CODEOWNERS protection for workflow files, and deployment environments.

### Level 5 — Agent Engineering

Learn the difference between persistent repository instructions and task-specific skills. Use skills for bounded workflows and `AGENTS.md` / instruction files for durable repository context.

### Level 6 — Advanced Automation

Progressively evaluate agentic workflows, Testkube, WebMCP, GeoAI, automated documentation checks, and release intelligence.

## Practical milestones

| Milestone | Evidence |
|---|---|
| Git Core | feature branch with reviewable commits |
| PR Engineering | complete PR with tests and docs |
| CI | green workflow on push and pull request |
| Security | permissions and dependency baseline documented |
| Documentation | changed behavior has linked documentation |
| Releases | reproducible tagged release with notes |
| Agent Context | repository and path-specific agent instructions |
| Skill Engineering | positive and negative trigger evaluations |
| WebMCP | registered tool with explicit side-effect semantics |
| Testkube | reproducible Kubernetes TestWorkflow |
| GeoAI | CRS/validity/spatial-validation report |

## CryoOmega target operating model

```text
Code + Tests + Docs + Security + Governance + Agents + Automation + Releases
                               ↓
                    Engineering Platform
```

## Priority

### P0 — Foundation

Repository governance, README/CONTRIBUTING alignment, agent context, baseline CI, testing, security, and release conventions.

### P1 — Engineering maturity

CODEOWNERS, path-specific instructions, Dependabot, advanced CI, artifacts, release automation, and Projects discipline.

### P2 — Agent and platform integration

Agentic workflows, WebMCP, Testkube, GeoAI, and AI/ML integration.

### P3 — Advanced autonomy

Multi-agent workflows, repository intelligence, automated documentation maintenance, and cross-repository orchestration.

## Study method

Every learning topic should produce a repository artifact: a document, test, workflow, issue, PR, or release. Avoid learning paths that do not leave an inspectable result.
