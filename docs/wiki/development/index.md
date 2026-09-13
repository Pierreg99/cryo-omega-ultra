# Development, Contribution & Team

This section defines how code and documentation changes are proposed, reviewed and maintained.

## Ownership

| Area | Primary owner |
|---|---|
| Overview | Project Maintainer |
| Getting Started | Developer Experience / Maintainer |
| Architecture | Tech Lead / Architecture Owner |
| CLI/Gateway/IDE | Component Maintainer |
| Operations | SRE / DevOps |
| Security | Security Owner |
| Plugins | Extension Maintainer |
| Releases | Release Owner |

## Documentation rules

- Technical documentation is maintained as Markdown in Git.
- Technical changes should update affected documentation in the same PR.
- Architecture decisions use ADRs and retain their historical rationale.
- Runbooks require a named owner and verification steps.

## Review cadence

- Architecture: quarterly and on architectural change.
- Operations: quarterly and after operational change.
- Security: quarterly and after security-boundary change.
- CLI/API references: whenever the public interface changes.
- Release notes: every release.

## Quality criteria

- One concrete question/task per page.
- Short active sentences.
- Tested or explicitly illustrative code examples.
- No dead internal links.
- No secrets in examples.

## PR documentation gate

```text
CLI/API change       -> reference review
Runtime/deploy change -> operations review
Security change       -> security review
Plugin lifecycle      -> plugin + security review
Architecture change   -> ADR/architecture review
```

## Planned pages

- [Development Workflow](workflow.md)
- [Coding Guidelines](coding-guidelines.md)
- [Testing Guidelines](testing-guidelines.md)
- [Contribution Guide](contribution.md)
- [Documentation Guide](documentation-guide.md)
- [Team & Roles](team.md)

## How to use this page

Use this page before opening a code or documentation PR to identify the required owner and review path.