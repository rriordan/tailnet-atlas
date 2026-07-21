# Tailnet Atlas

A private, tailnet-only dashboard for finding, checking, and opening services across Tailscale-connected devices without remembering device names and ports.

> **Status:** Specification and implementation scaffold. The MVP has not been implemented yet.

## Problem

Self-hosted tools often live behind different device names, ports, and paths. Tailnet Atlas provides one memorable Tailscale URL that acts as a searchable launcher and lightweight health dashboard for those services.

## MVP scope

The first release is intentionally **tailnet-first**:

- Query the local Tailscale CLI for tailnet and device metadata.
- Let users confirm detected devices and enter missing values.
- Store services in an explicit YAML registry.
- Build service URLs from device, protocol, port, and path.
- Perform safe server-side health checks.
- Provide a responsive web dashboard and CLI.
- Bind locally and publish privately through Tailscale Serve.

The MVP does **not** inspect or control Docker, scan ports, restart services, expose the dashboard publicly, or act as an unrestricted URL-fetch proxy.

## Handoff to Hermes

Hermes should begin with [`HERMES_TASK.md`](HERMES_TASK.md), then read:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/implementation-spec.md`](docs/implementation-spec.md)
3. [`docs/architecture.md`](docs/architecture.md)
4. [`docs/security-model.md`](docs/security-model.md)
5. [`docs/roadmap.md`](docs/roadmap.md)

Suggested handoff prompt:

```text
Clone https://github.com/rriordan/tailnet-atlas, read HERMES_TASK.md and AGENTS.md first, inspect the repository and host environment, then present a Phase 0 assessment and implementation plan. Do not modify Tailscale Serve, install system packages, create systemd services, publish releases, or commit private tailnet data without explicit approval.
```

## Planned stack

- Python 3.11+
- FastAPI, Pydantic, HTTPX, Jinja2, Typer
- YAML configuration
- Pytest, Ruff, MyPy
- Tailscale CLI and Tailscale Serve
- Optional systemd user service

## Repository layout

```text
docs/                  Design and implementation requirements
examples/              Sanitized example configuration
src/tailnet_atlas/     Application package scaffold
tests/                  Test scaffold
HERMES_TASK.md          Primary implementation assignment
AGENTS.md               Repository working rules
```

## Current milestone

Prepare a tested `0.1.0` MVP that can:

1. Detect a local tailnet and its devices defensively.
2. Register at least three services manually.
3. Render a mobile-friendly dashboard.
4. Distinguish healthy, authenticated, unavailable, offline, disabled, and unknown health states.
5. Publish the dashboard through tailnet-only Tailscale Serve without overwriting unrelated routes.

See [`docs/implementation-spec.md`](docs/implementation-spec.md) for the full definition of done.

## License

MIT. See [`LICENSE`](LICENSE).
