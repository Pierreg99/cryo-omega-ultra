# Runbook: Deployment

- **Owner:** Release / Operations
- **Environment:** Dev, Staging, Production as applicable

## Preconditions

- Intended commit/version is known.
- Tests and required CI checks are green.
- Configuration changes are reviewed.
- Rollback target is known.

## Procedure

### 1. Validate

```bash
./bin/omega doctor
```

### 2. Deploy

```bash
<project-specific deployment command>
```

### 3. Verify

```bash
./bin/omega gateway status
./bin/omega doctor
```

For Web IDE/API changes, perform a client smoke test as well.

## Rollback

```bash
<project-specific rollback command>
```

Then repeat health and smoke checks.

## Evidence

Record version, commit SHA, deployment time, operator, verification result and rollback outcome if used.