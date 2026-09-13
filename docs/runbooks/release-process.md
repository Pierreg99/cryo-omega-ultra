# Runbook — Release Process

1. Branch from `main`; small commits; `pytest -q` green.
2. Bump `__version__` + CHANGELOG.
3. Open PR; wait for Python CI.
4. Merge; tag optional `vX.Y.Z`.
5. Rollback: revert merge commit or redeploy previous tag.
