# Hermes Implementation Task: Tailnet Atlas MVP

## Assignment

Implement, test, document, and locally deploy the `0.1.0` MVP of **Tailnet Atlas**.

Tailnet Atlas gives users one memorable, tailnet-only web address for finding, checking, and opening services running across their Tailscale-connected devices. Users should not need to remember device names, ports, or paths.

## Immediate instruction

Do not start coding immediately.

First perform **Phase 0: environment assessment**:

1. Inspect the repository and read all linked specifications.
2. Inspect the local Tailscale CLI version and available `status`, `serve`, and help output.
3. Run only read-only Tailscale inspection commands.
4. Confirm whether systemd user services are available.
5. Identify the relevant Python and `uv` environment.
6. Inspect whether the preferred local port is free.
7. Inspect current Tailscale Serve state without changing it.
8. Capture only sanitized structural examples of Tailscale JSON; never commit private values.
9. Return a concise assessment, risks, proposed architecture, phased plan, and list of mutations that would require approval.
10. Wait for approval before host mutations.

## Core MVP

Build:

- Defensive Tailscale CLI discovery using `tailscale status --json`.
- Interactive setup that auto-detects first and prompts only when necessary.
- An explicit YAML registry for devices and services.
- A CLI for setup, validation, status, device refresh, service management, diagnostics, and uninstall.
- Safe asynchronous health checks restricted to registered tailnet targets.
- A responsive web dashboard with search and filters.
- Localhost-only binding.
- Optional, explicitly approved Tailscale Serve configuration.
- Optional, explicitly approved systemd user service.
- Dry-run setup and safe uninstall.
- Tests, CI, documentation, and sanitized examples.

## Explicit non-goals for `0.1.0`

Do not add:

- Docker discovery or Docker API access.
- Docker socket access.
- Docker or systemd control actions.
- Automatic port scanning.
- LAN discovery.
- Internet monitoring.
- Tailscale Funnel or public access.
- Tailscale API keys or admin-console integration.
- Historical uptime storage.
- Prometheus, Grafana, or ntfy integration.
- WSL Doctor integration.
- Hermes MCP integration.
- Browser-based configuration editing.
- User accounts or role-based access.
- Multi-tailnet support.
- An arbitrary server-side URL fetch endpoint.

Docker-hosted services may be manually registered as normal service URLs. Their runtime is out of scope.

## Required implementation phases

### Phase 0 — Assessment

No host mutation. Return findings and wait for approval.

### Phase 1 — Foundation

Implement package structure, models, configuration loading, validation, backups, atomic writes, CLI skeleton, linting, typing, and tests.

### Phase 2 — Tailscale adapter

Implement command execution, defensive JSON parsing, normalized device models, DNS suffix detection, device refresh, reconciliation, fixtures, and tests.

### Phase 3 — Service registry

Implement add, edit, remove, list, URL construction, target validation, and configuration dry-runs.

### Phase 4 — Health engine

Implement asynchronous checks, concurrency limits, timeouts, TLS verification, health classification, sanitized errors, and tests.

### Phase 5 — Web dashboard

Implement dashboard, devices view, service detail, search, filters, responsive styling, accessibility, and themes.

### Phase 6 — Installation and deployment

Implement setup, systemd user service support, Tailscale Serve compatibility adapter, route-conflict handling, doctor command, verification, and uninstall.

### Phase 7 — Release preparation

Complete README, security documentation, CI, screenshots or sanitized mockups, changelog, and release notes. Do not publish or tag without approval.

## Required commands

The installed CLI should provide:

```text
tailnet-atlas setup
tailnet-atlas setup --dry-run
tailnet-atlas serve
tailnet-atlas validate
tailnet-atlas status
tailnet-atlas devices refresh
tailnet-atlas devices list
tailnet-atlas services list
tailnet-atlas services add
tailnet-atlas services edit
tailnet-atlas services remove
tailnet-atlas config path
tailnet-atlas config show
tailnet-atlas doctor
tailnet-atlas uninstall
tailnet-atlas uninstall --purge
```

## Critical safety requirements

- Bind to `127.0.0.1`, never `0.0.0.0`, by default.
- Expose privately through Tailscale Serve only after approval.
- Never enable Funnel.
- Inspect and preserve existing Serve routes.
- Never perform a global Serve reset unless it is proven safe and separately approved.
- Keep service health targets limited to registered tailnet devices and localhost.
- Do not collect response bodies, credentials, environment values, or `.env` files.
- Do not log request bodies or secrets.
- Verify TLS by default.
- Make writes atomic and retain a previous valid configuration backup.
- Keep systemd user-level; do not run the service as root.

## Definition of done

Do not report completion until:

- Tailscale status parsing works on the target environment.
- Missing fields and disconnected states fail gracefully.
- Automatic detection and manual fallback both work.
- At least three real services can be registered locally without committing private data.
- Launch links work from another tailnet device.
- Health states distinguish healthy, authentication required, warning, unavailable, device offline, disabled, and unknown.
- The dashboard is usable on desktop and mobile.
- The backend binds only to localhost.
- Tailscale Serve exposure is private and preserves unrelated configuration.
- Setup dry-run makes no changes.
- The app can start automatically when systemd is available, with a documented fallback otherwise.
- Unit and integration tests pass.
- Ruff, MyPy, package build, smoke tests, and CI pass.
- Examples and fixtures contain no private infrastructure data.
- Uninstall behavior is tested.
- Release tagging is withheld pending approval.

## Required final report

Return:

1. What was built and where.
2. Installed version, local bind address, dashboard URL, and configuration path.
3. What was auto-detected versus manually supplied.
4. A redacted service verification table.
5. Tests and quality checks actually executed.
6. Every host file, package, service, and Tailscale setting changed.
7. Deferred features and confirmation that Docker integration was not added.
8. Honest limitations and unresolved issues.

The complete technical requirements are in `docs/implementation-spec.md`.
