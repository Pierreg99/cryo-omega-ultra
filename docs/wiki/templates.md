# Documentation Templates

Use these templates for recurring document types. Copy a template, replace placeholders, then remove unused sections only when they are genuinely irrelevant.

## Decision Log / ADR

```md
# ADR-XXXX: <Decision title>

- **Status:** Proposed | Accepted | Superseded | Deprecated
- **Date:** YYYY-MM-DD
- **Owner:** <role>
- **Reviewers:** <roles>

## Context

What problem requires a decision?

## Decision

What was chosen?

## Alternatives Considered

- Option A — advantages / disadvantages
- Option B — advantages / disadvantages

## Consequences

- Positive:
- Negative:
- Operational:
- Security:

## Migration / Rollout

- <step>

## Validation

- [ ] Tests updated
- [ ] Documentation updated

## References

- Issue:
- PR:
```

## Runbook

```md
# Runbook: <Action>

- **Owner:** <role>
- **Severity:** P1 | P2 | P3 | P4
- **Environment:** Local | Dev | Staging | Production
- **Last Reviewed:** YYYY-MM-DD

## Purpose
## Preconditions
## Detection
## Procedure
### 1. Check
### 2. Action
### 3. Verify
## Rollback
## Escalation
## Evidence
## Post-Checks
```

## Incident / Postmortem

```md
# Incident: <Short Title>

- **Incident ID:** INC-YYYY-XXXX
- **Date:** YYYY-MM-DD
- **Severity:** P1 | P2 | P3 | P4
- **Owner:** <role>

## Summary
## Impact
## Timeline
## Root Cause
## Contributing Factors
## Resolution
## Corrective Actions
## Detection Improvements
## Lessons Learned
## References
```

## Meeting Notes

```md
# Meeting: <Topic>

- **Date:** YYYY-MM-DD
- **Participants:** <names/roles>
- **Owner:** <name>

## Agenda
## Decisions
## Discussion
## Action Items
| Action | Owner | Due | Status |
|---|---|---|---|
## Risks / Blockers
## Follow-up
```

## Release Notes

```md
# CryoOmega ULTRA <version>

- **Release date:** YYYY-MM-DD
- **Release type:** Major | Minor | Patch

## Summary
## Added
## Changed
## Fixed
## Security
## Breaking Changes
## Migration
## Deprecations
## Verification
## References
```

## Document classification

- **Quickstart:** minimum successful path.
- **Tutorial:** complete a guided use case.
- **How-to:** solve one concrete task.
- **Reference:** exact commands, APIs and configuration.
- **Concept:** explain architecture, terminology or design principles.
