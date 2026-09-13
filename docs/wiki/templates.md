# Documentation Templates

All templates are deliberately compact. Add repository-specific details rather than copying generic prose.

## Decision Log / ADR

```markdown
# ADR-NNNN: <Decision title>

- Status: Proposed | Accepted | Superseded | Rejected
- Date: YYYY-MM-DD
- Owners: <role or person>

## Context
What problem or constraint requires a decision?

## Decision
State the chosen approach and its boundaries.

## Alternatives
- <alternative> — reason not selected
- <alternative> — reason not selected

## Consequences
- Positive: <effect>
- Negative: <trade-off>
- Operational: <impact>

## Verification
How will we know this decision is working?
```

Example decisions:

- Keep gateway execution authoritative instead of duplicating business logic in clients.
- Use a projected CRS for distance/area calculations rather than degrees when the workflow is geospatial.

## Runbook

```markdown
# Runbook: <Action>

## Purpose
What operational problem does this procedure solve?

## Preconditions
- Access
- Environment
- Safety checks

## Procedure
1. <command/action>
2. <command/action>

## Verification
Expected healthy state and exact checks.

## Rollback
How to return to the previous safe state.

## Escalation
When and where to escalate.

## Evidence
What logs, timestamps, versions, and artifacts to record.
```

Examples:

- Restart the gateway and verify status plus a smoke request.
- Collect logs and redact secrets before attaching them to an incident.

## Incident / Postmortem

```markdown
# Incident: <Title>

- Date: YYYY-MM-DD
- Severity: SEV-1 | SEV-2 | SEV-3 | SEV-4
- Status: Investigating | Mitigated | Resolved
- Owner: <role>

## Summary
What happened and what was affected?

## Impact
Users, components, data, duration.

## Timeline
- HH:MM — <event>
- HH:MM — <event>

## Detection
How was the incident detected?

## Root Cause
Technical cause, contributing factors, and missing controls.

## Mitigation
What reduced or stopped the impact?

## Corrective Actions
- [ ] <action> — owner — due date

## Lessons Learned
What should change in code, operations, tests, or documentation?
```

Examples:

- Gateway unavailable after deployment due to a configuration mismatch.
- Credential exposed in a log; credential rotation is mandatory corrective action.

## Meeting Notes

```markdown
# Meeting: <Topic>

- Date: YYYY-MM-DD
- Participants: <names/roles>

## Purpose
Why was the meeting held?

## Decisions
- <decision>

## Open Questions
- <question> — owner

## Actions
- [ ] <action> — owner — due date

## References
- <issue / PR / ADR / document>
```

## Release Notes

```markdown
# <Version> — YYYY-MM-DD

## Summary
What changed and why?

## Added
- <feature>

## Changed
- <behavior or interface>

## Fixed
- <bug>

## Security
- <security-relevant change>

## Breaking Changes
- <breaking change> or `None`

## Migration
1. <step>
2. <step>

## Verification
- <test suite / CI run / artifact>

## Known Issues
- <issue> or `None`
```
