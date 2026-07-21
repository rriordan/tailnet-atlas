# Roadmap

## `0.1.0` — Tailnet launcher MVP

- Defensive local Tailscale discovery.
- Confirmed device inventory.
- Manual YAML service registry.
- CLI setup and service management.
- Searchable responsive dashboard.
- Server-side health checks.
- Localhost binding.
- Approval-gated Tailscale Serve setup.
- Optional systemd user service.
- Dry-run, doctor, validation, and safe uninstall.
- Tests, CI, documentation, and sanitized examples.

## `0.2.0` — Operational polish

Candidates after a stable MVP:

- Browser-assisted configuration with strict validation.
- Better device reconciliation UX.
- Import and export workflows.
- Health-check profiles and custom accepted status ranges.
- Expected-service warnings.
- WSL Doctor JSON integration.
- ntfy alerts for meaningful state changes.
- Installation and upgrade hardening.

Each feature must preserve the tailnet-only and least-privilege model.

## `0.3.0` — Read-only runtime discovery

Potential Docker phase:

- Optional read-only collector.
- Docker and Compose metadata discovery.
- Proposed registry additions requiring approval.
- Container state, image, and mapped-port metadata.
- No control actions by default.
- No unrestricted Docker socket exposure to the web process.

Potential systemd phase:

- Read-only service inventory.
- Proposed associations with registered services.
- No browser control actions by default.

## `0.4.0` — Controlled operations

Only after a dedicated security review:

- Narrow restart actions.
- Explicit confirmation and approval policies.
- Least-privilege helper process.
- Audit log.
- Role-aware access if multiple users are supported.
- Clear separation between launcher, observer, and controller modes.

## Future candidates

- Named Tailscale Services integration.
- Windows-host companion collector.
- Tailscale endpoint collection.
- Historical uptime and trends.
- Dependency maps.
- Prometheus-compatible metrics.
- Hermes MCP tools.
- Mobile installability improvements.
- Multi-host failover for the dashboard.

## Non-goals unless deliberately reconsidered

- Public service directory.
- Tailscale Funnel by default.
- General internet monitoring.
- Arbitrary command execution.
- Unrestricted reverse proxy.
- Automatic publication of discovered ports.
- Silent service-control actions.

## Release rule

Do not begin the Docker phase until `0.1.0` is useful in daily operation, documented, tested, and released. Scope expansion should solve observed needs rather than hypothetical ones.
