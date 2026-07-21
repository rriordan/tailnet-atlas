# Architecture

## System context

Tailnet Atlas runs on one Tailscale-connected host and provides a private dashboard for services registered across the same tailnet.

```text
Browser on tailnet
        |
        v
Tailscale Serve (private HTTPS)
        |
        v
Tailnet Atlas on 127.0.0.1
  |-- YAML configuration
  |-- Tailscale CLI adapter
  |-- asynchronous health engine
  |-- server-rendered dashboard
  `-- CLI and installer
        |
        v
Registered services on tailnet devices
```

## Architectural principles

1. **Explicit registry over implicit discovery** — Tailscale supplies device metadata; users define services.
2. **Auto-detect, then confirm** — detection reduces setup work but does not silently publish devices or services.
3. **Tailnet-only target boundary** — health checks cannot become an unrestricted proxy.
4. **Read-only MVP** — no Docker, systemd, or service-control actions.
5. **Compatibility adapters** — Tailscale CLI output and Serve syntax are isolated from core logic.
6. **Local-first configuration** — no database, cloud account, telemetry, or hosted dependency.
7. **Safe mutations** — dry-run, confirmation, backups, atomic writes, and preservation of unrelated host configuration.

## Components

### CLI

Owns setup, status, validation, device refresh, service CRUD, doctor, and uninstall commands. CLI handlers should orchestrate domain services rather than contain parsing or mutation logic.

### Configuration layer

Loads, validates, migrates, backs up, and atomically writes YAML configuration. Pydantic models should define the schema and cross-reference validation.

### Tailscale adapter

Runs read-only commands, parses status JSON defensively, normalizes devices, detects installed Serve syntax, inspects routes, and generates explicit proposed changes.

The adapter should expose stable internal operations such as:

```text
get_local_status()
list_devices()
get_tailnet_suffix()
inspect_serve()
plan_serve_route()
apply_serve_plan()
```

Only the approved mutation method may change Serve.

### Device reconciler

Merges newly detected device metadata into stored configuration while preserving user-controlled fields. Missing devices are retained and marked unavailable.

### Service registry

Builds launch and health URLs, validates device references, enforces tailnet-target restrictions, and manages manual service records.

### Health engine

Performs bounded asynchronous HTTP checks. It should accept validated service targets only, store current results in memory, and avoid response-body collection.

### Web application

FastAPI with Jinja2 templates and small local JavaScript. The server exposes dashboard, device, service-detail, settings-information, and controlled refresh endpoints. It must not expose arbitrary URL fetching or shell execution.

### Installer

A tested Python workflow called by a thin shell bootstrap. It computes a mutation plan, supports dry-run, requests approval, applies approved changes, and verifies outcomes.

## Data flow

### Startup

1. Load and validate configuration.
2. Query Tailscale through the adapter.
3. Reconcile in-memory device state without silently writing changes.
4. Build validated service targets.
5. Start health scheduler.
6. Serve the dashboard on localhost.

### Device refresh

1. Query current Tailscale status.
2. Normalize devices.
3. Compare with stored devices.
4. Produce a reconciliation plan.
5. Preserve aliases, visibility, pins, and service associations.
6. Write only after validation and confirmation where needed.

### Health refresh

1. Skip disabled services.
2. Skip or classify services on offline devices.
3. Resolve the validated registered target.
4. Check with timeout and concurrency limits.
5. Classify the result.
6. Store only status, timestamp, latency, HTTP code, and sanitized error category.

## State model

Persistent state should remain minimal:

- YAML configuration and backups.
- Installer ownership metadata for files, systemd unit, and Serve route.
- Optional last successful setup summary.

Health history is not persisted in the MVP.

## Failure behavior

- Invalid configuration prevents startup with actionable validation output.
- Tailscale unavailable permits configuration inspection but marks device state unknown.
- Missing fields yield partial normalized records rather than crashes.
- One failed health target does not block others.
- Serve conflicts stop deployment changes but do not prevent local operation.
- Systemd absence results in a documented foreground launch path.

## Extension seams

Future collectors may implement a shared discovery interface and propose registry entries. Potential sources include Docker, systemd, Tailscale endpoints, and imported inventories. Discovery must remain separate from automatic publication or control.
