# Security Model

## Security objective

Tailnet Atlas should reduce the need to remember internal service addresses without creating a new public exposure, command surface, or unrestricted request proxy.

The `0.1.0` MVP is a private launcher and read-only status dashboard. It is not a service-control plane.

## Trust boundaries

### Trusted

- The local user who owns the configuration.
- The local Tailnet Atlas process.
- The installed Tailscale client and its authenticated local identity.
- Explicitly registered devices and services after validation.

### Partially trusted

- Other devices on the same tailnet.
- Service HTTP responses.
- Tailscale CLI output, which is trusted as local metadata but parsed defensively.
- Manually edited YAML, which must be validated before use.

### Untrusted

- Arbitrary public internet domains.
- Unregistered addresses and ports.
- Service response bodies.
- Browser-supplied arbitrary URLs.
- Values that resemble credentials, cookies, tokens, or environment secrets.

## Mandatory controls

### Network exposure

- Bind the backend to `127.0.0.1` by default.
- Use Tailscale Serve for private access only after explicit approval.
- Never configure or invoke Tailscale Funnel.
- Never default to `0.0.0.0`.
- Preserve unrelated Serve routes and require approval for conflicts.

### Health-check restrictions

- Build targets only from validated registered service records.
- Allow only localhost, registered Tailscale DNS names, and registered Tailscale IPs.
- Reject arbitrary internet domains and unregistered IPs.
- Do not expose a generic URL-fetch endpoint.
- Do not display or persist response bodies.
- Apply timeouts, redirect limits, and concurrency limits.
- Verify TLS by default.

### Secrets and privacy

- Do not store credentials, API keys, cookies, passwords, or tokens.
- Do not read `.env` files.
- Do not inventory environment-variable values.
- Do not log request bodies.
- Sanitize command output and errors before display.
- Do not commit real tailnet suffixes, Tailscale IPs, internal URLs, or private topology.
- Use fictional values in examples and sanitized fixtures in tests.

### Host mutation

- Setup must support a no-change dry-run.
- Show planned files and commands before mutation.
- Require approval before Serve or systemd changes.
- Use user-level systemd units only.
- Do not run the web service as root.
- Make configuration writes atomic and keep backups.
- Track ownership metadata for changes made by Tailnet Atlas.

### Explicitly prohibited in the MVP

- Docker socket or Docker API access.
- Container or systemd controls.
- Port scanning.
- Shell execution through the web app.
- Package updates.
- Tailscale API keys.
- Public exposure.
- External analytics or telemetry.

## Threat scenarios

### SSRF through health checks

**Risk:** A user or browser submits an arbitrary URL and uses the server to reach unintended targets.

**Mitigation:** No generic fetch route; all targets derive from validated registry entries tied to detected devices. Validate DNS names and Tailscale IPs before each check.

### Accidental public exposure

**Risk:** The dashboard is published using Funnel or bound to all interfaces.

**Mitigation:** Localhost default, explicit Serve-only integration, command capability detection, and a hard prohibition on Funnel.

### Destructive Serve changes

**Risk:** Setup overwrites existing routes.

**Mitigation:** Inspect before-state, detect conflicts, generate a plan, require approval, apply only the owned route, and verify afterward.

### Leaking internal topology

**Risk:** Public repository examples or screenshots reveal device names, IPs, or service addresses.

**Mitigation:** Fictional examples, fixture sanitization, documentation warnings, and final pre-release review.

### Malicious or surprising service responses

**Risk:** A registered service returns large, sensitive, or hostile content.

**Mitigation:** Do not render response bodies; collect only status code, latency, timestamps, and sanitized error categories. Limit redirects and response handling.

### Configuration tampering

**Risk:** Invalid or malicious YAML changes targets or breaks startup.

**Mitigation:** Strict schema validation, cross-reference validation, target allowlisting, atomic writes, backups, and actionable startup failure.

## Information displayed

The dashboard may display:

- Service and device names.
- Internal launch URLs.
- Tailscale IPs when enabled in the UI.
- Health state, latency, and last-check time.
- Operating system and last-seen metadata.

Users should be warned that screenshots may reveal private infrastructure even though the dashboard is tailnet-only.

## Vulnerability reporting

`SECURITY.md` should document a private reporting path before a public release. Do not ask reporters to include credentials, full configuration files, or unredacted tailnet data.
