# Security & Threat Model

## Purpose

Define the security boundaries for CryoOmega ULTRA and provide a practical checklist for developers and operators.

## Primary attack surfaces

- CLI input and local command execution
- Gateway HTTP/API exposure
- Web IDE requests and browser integration
- Plugins executing in the application process
- Agents and skills consuming instructions or external content
- Provider credentials and runtime configuration
- GitHub Actions and repository automation
- Dependency and release supply chain

## Trust boundaries

```text
User / browser
      ↓
Client surfaces
      ↓
Gateway
      ↓
Agents / skills / plugins
      ↓
External providers
```

Each boundary needs explicit validation, permissions, and error handling.

## Access control

Default to local, least-privilege operation. Remote gateway access should be an explicit operational decision, not an accidental default. Protect administrative or state-changing interfaces with authentication and authorization before exposing them beyond a trusted local environment.

## Secrets handling

- Keep API keys in environment configuration or a dedicated secret store.
- Never commit real credentials.
- Do not copy secrets into logs, issues, screenshots, or artifacts.
- Rotate exposed credentials immediately and document the incident.

## Plugin trust

Plugins are executable code and therefore represent a privileged extension boundary. Review provenance, requested capabilities, dependency changes, and runtime behavior before enabling an untrusted plugin.

## Agent and skill safety

Treat external instructions, downloaded files, repository content, and generated tool parameters as untrusted until validated. Skills must have clear trigger boundaries and must not silently expand permissions.

## GitHub Actions security

Use minimum required `GITHUB_TOKEN` permissions and review workflow changes carefully. Protect workflow files with CODEOWNERS where practical. Dependency review can block pull requests that introduce known vulnerable packages when configured as a required check. citeturn318453search0turn318453search2

## Incident checklist

- [ ] Identify affected component and trust boundary.
- [ ] Preserve relevant logs and timestamps.
- [ ] Revoke or rotate exposed credentials.
- [ ] Contain remote exposure if necessary.
- [ ] Record scope and impact.
- [ ] Patch and verify.
- [ ] Document root cause and prevention.

## Planned subpages

- [Threat Model](threat-model.md)
- [Trust Boundaries](trust-boundaries.md)
- [Secrets](secrets.md)
- [Remote Gateway](remote-gateway.md)
- [Plugin Trust](plugin-trust.md)
- [Security Checklist](checklist.md)

## How to use this page

Use this page before exposing a component, adding a plugin, changing workflow permissions, or handling credentials. Detailed controls belong in the corresponding security reference pages.
