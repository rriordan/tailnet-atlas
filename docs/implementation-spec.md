# Tailnet Atlas `0.1.0` MVP Specification

## 1. Product definition

Tailnet Atlas is a private web dashboard and CLI that gives a user one memorable tailnet-only address for finding, checking, and opening web services across Tailscale-connected devices.

The central user problem is simple:

> Do not require users to remember which device, port, protocol, and path each self-hosted service uses.

The MVP is **tailnet-first and runtime-neutral**. A service may run directly on Linux, WSL, Windows, macOS, or inside a container, but Tailnet Atlas treats it as a registered URL. Runtime inspection and control are deferred.

## 2. Target environment

Optimize the first implementation for:

- Linux or WSL2 as the dashboard host.
- Tailscale already installed and authenticated.
- MagicDNS preferably enabled.
- Multiple devices on one tailnet.
- Web services running across WSL, Windows, Linux, or other tailnet nodes.
- Systemd user services when available.
- Desktop and mobile access over the tailnet.

Do not hard-code personal device names, tailnet suffixes, IP addresses, ports, or service inventory.

## 3. User outcome

After setup, the user should have:

1. A dashboard listening on localhost.
2. A stable tailnet-only HTTPS address provided through Tailscale Serve when approved.
3. A searchable registry of services.
4. Launch links with correct device, protocol, port, and path.
5. Basic health states and response latency.
6. A device inventory enriched from the local Tailscale client.
7. A human-editable YAML configuration file.
8. CLI commands for setup, validation, status, refresh, service management, diagnostics, and uninstall.

## 4. Tailnet detection

### 4.1 Primary discovery

Use the installed Tailscale CLI:

```bash
tailscale status --json
```

Attempt to detect:

- Tailscale connection state.
- Local host name and full DNS name.
- MagicDNS suffix.
- Local Tailscale IP addresses.
- Peer names, DNS names, Tailscale IPs, operating systems, online state, activity, and last-seen values when available.

Potential fields may resemble:

```text
BackendState
MagicDNSSuffix
Self
Self.HostName
Self.DNSName
Self.TailscaleIPs
Peer
Peer.*.HostName
Peer.*.DNSName
Peer.*.TailscaleIPs
Peer.*.OS
Peer.*.Online
Peer.*.Active
Peer.*.LastSeen
```

Do not assume these fields always exist or always retain the same shape.

### 4.2 Adapter requirement

All Tailscale command execution and JSON-field interpretation must live behind a dedicated compatibility adapter. The rest of the application should consume normalized internal models.

The adapter must:

- Handle missing keys.
- Handle `null`, scalar, list, and mapping variations defensively.
- Return structured errors instead of raw stack traces.
- Preserve unknown fields only when useful for diagnostics.
- Be testable from captured, sanitized fixtures.

### 4.3 Detection precedence

For the tailnet DNS suffix, try:

1. Explicit MagicDNS suffix in status output.
2. The suffix portion of the local full DNS name.
3. Additional read-only local Tailscale DNS information when available.
4. Manual entry.

For a device address, prefer:

1. Full Tailscale DNS name.
2. Machine name plus detected DNS suffix.
3. Tailscale IP.
4. Manual entry.

### 4.4 Setup confirmation

Always show detected values before writing configuration. Users must be able to correct them and select which devices are visible.

Example:

```text
Detected tailnet
  DNS suffix: example-tailnet.ts.net
  Local device: atlas-host
  Local DNS name: atlas-host.example-tailnet.ts.net
  Tailscale state: Running

Detected devices
  [x] atlas-host    Linux      Online
  [x] workstation   Windows    Online
  [ ] phone         Android    Offline
```

If detection is incomplete, explain what is missing, ask only for the missing values, validate the answers, and record whether values were detected or manually supplied.

## 5. Configuration and service registry

### 5.1 Source of truth

Tailscale discovers nodes, not arbitrary services or their ports. Therefore an explicit YAML file is the authoritative source for service definitions.

Default path:

```text
~/.config/tailnet-atlas/config.yaml
```

Suggested schema:

```yaml
schema_version: 1

dashboard:
  title: Tailnet Atlas
  bind_host: 127.0.0.1
  port: 8787
  base_path: /
  refresh_seconds: 30
  health_interval_seconds: 30
  health_timeout_seconds: 4
  theme: system

tailnet:
  dns_suffix: example-tailnet.ts.net
  local_device: atlas-host
  detection_source: automatic

devices:
  - id: atlas-host
    display_name: Atlas Host
    machine_name: atlas-host
    dns_name: atlas-host.example-tailnet.ts.net
    tailscale_ips:
      - 100.64.0.10
    os: linux
    visible: true
    pinned: true

services:
  - id: example-agent
    name: Example Agent
    description: Private AI agent interface
    category: AI and Agents
    device: atlas-host
    scheme: http
    port: 8080
    path: /
    favorite: true
    tags:
      - ai
      - agent
    source: manual
    runtime: unknown
    runtime_metadata: {}
    health:
      enabled: true
      method: GET
      path: /
      follow_redirects: true
      tls_verify: true
```

### 5.2 Validation rules

- `schema_version` is required.
- Device IDs are unique.
- Service IDs are unique.
- Every service references a known device.
- Ports are integers from 1 through 65535.
- Paths begin with `/`.
- MVP schemes are `http` and `https` only.
- `url_override`, when present, must pass target-safety validation.
- Secrets, cookies, passwords, keys, and tokens must not be stored.

### 5.3 Service URL construction

Default construction:

```text
scheme + device address + port + path
```

Example:

```text
http://atlas-host.example-tailnet.ts.net:8080/
```

Allow an explicit override:

```yaml
url_override: https://service-name.example-tailnet.ts.net/
```

Use the override only when configured and validated.

### 5.4 Safe writes

Configuration writes must be atomic:

1. Serialize to a temporary file in the same filesystem.
2. Validate the full candidate configuration.
3. Preserve the previous valid configuration as a backup.
4. Atomically replace the active file.
5. Retain useful errors without exposing secrets.

## 6. Device refresh and reconciliation

A refresh should update detected metadata while preserving user decisions.

Update:

- Operating system.
- DNS name.
- Tailscale IPs.
- Online or availability state.
- Last-seen metadata.

Preserve:

- Display name.
- Visibility.
- Pinned state.
- Service associations.
- Manual notes or metadata.

New devices should be added as hidden or unreviewed. Missing devices should be marked unavailable, not deleted.

If a name changes and no stable match can be established, request reconciliation rather than duplicating or silently moving services.

## 7. CLI

Provide the console command:

```text
tailnet-atlas
```

Required commands:

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

### 7.1 Setup

Interactive setup must:

1. Run preflight checks.
2. Discover Tailscale metadata.
3. Show and confirm tailnet values.
4. Show and select devices.
5. Choose a free local dashboard port, defaulting to `8787`.
6. Offer initial service registration.
7. Show proposed file and host changes.
8. Write and validate configuration.
9. Offer systemd user-service setup when available.
10. Offer Tailscale Serve setup only after explicit confirmation.
11. Verify local access and, when possible, tailnet access.
12. Print a concise final report.

### 7.2 Setup dry-run

`setup --dry-run` must show:

- Detected values.
- Proposed configuration.
- Files that would be written.
- Commands that would run.
- Proposed systemd changes.
- Proposed Tailscale Serve changes.

It must make no changes.

### 7.3 Status

Show:

- Application version and process status.
- Local listening address.
- Tailscale state.
- Dashboard tailnet URL when known.
- Visible-device count.
- Registered-service count.
- Health summary.

### 7.4 Service management

`services add` should prompt for name, description, device, scheme, port, path, category, tags, favorite status, and optional health settings. Show the generated URL and require confirmation.

Edit and remove operations should show the target record and require confirmation unless a documented noninteractive flag is supplied.

### 7.5 Doctor

Read-only diagnostics should cover:

- Configuration validity.
- Tailscale executable availability.
- Tailscale connection state.
- Local port availability.
- Local application reachability.
- Systemd user-unit status when used.
- Tailscale Serve status.
- DNS resolution of selected devices.
- Service URL construction and target validation.

Return prioritized remediation without making changes.

## 8. Installer

Provide a thin `install.sh`; keep business logic in tested Python code.

### 8.1 Preflight

Check:

- Supported operating system.
- Python version.
- Whether `uv` is available.
- Whether `tailscale` exists.
- Whether Tailscale is connected.
- Whether the preferred local port is free.
- Whether systemd user services are available.
- Existing installation state.
- Existing Tailscale Serve configuration.

Do not automatically install Tailscale, run `tailscale up`, authenticate the user, alter WSL configuration, or install a system package manager.

### 8.2 Installation paths

Preferred paths:

```text
Application:   ~/.local/share/tailnet-atlas/
Configuration: ~/.config/tailnet-atlas/
State:         ~/.local/state/tailnet-atlas/
```

Prefer `uv` when present. Otherwise use an application-local virtual environment. Do not require Node.js.

## 9. Web application

### 9.1 Recommended stack

- Python 3.11+
- FastAPI
- Pydantic
- HTTPX
- Jinja2
- Typer
- PyYAML or equivalent
- Plain CSS and small bundled JavaScript
- Pytest, Ruff, MyPy

Avoid Node-based build requirements, databases, external CDNs, analytics, and third-party authentication in the MVP.

### 9.2 Dashboard page

Show:

- Favorites first.
- Services grouped by category.
- Search.
- Category, device, and health filters.
- Manual refresh.
- Last refresh time.
- Overall health summary.

### 9.3 Devices page

Show:

- Display and machine names.
- Full DNS name.
- Operating system.
- Tailscale IPs.
- Online or availability state.
- Last-seen value when available.
- Number of registered services.
- Visible, hidden, and pinned states.

### 9.4 Service detail

Show:

- Name and description.
- Category and tags.
- Device.
- Full launch URL.
- Health state and latency.
- Last check and HTTP status.
- Open and copy-URL controls.
- Collapsible technical details.

### 9.5 Settings information

Provide a read-only view of configuration path, tailnet suffix, dashboard device, bind address, local port, Serve URL, refresh intervals, and application version.

A full browser editor is deferred.

### 9.6 Accessibility and privacy

- Responsive on desktop and mobile.
- Keyboard accessible.
- Screen-reader labels.
- Status must not rely on color alone.
- Light, dark, and system themes.
- Local assets only.
- No trackers or telemetry.

## 10. Health checking

Perform checks on the backend, never through a generic browser fetch endpoint.

### 10.1 Health states

| Condition | State |
|---|---|
| HTTP 200–399 | Healthy |
| HTTP 401 or 403 | Authentication required |
| Other valid response | Reachable with warning |
| DNS failure, refusal, timeout | Unavailable |
| Registered device offline | Device offline |
| Health disabled | Health check disabled |
| Unexpected internal failure | Unknown |

Do not mark authentication-required services as unavailable.

### 10.2 Engine requirements

- Asynchronous checks.
- Configurable concurrency limit.
- Default four-second timeout.
- Redirects followed by default.
- Response latency captured.
- Current state kept in memory.
- Configurable periodic refresh.
- Manual refresh.
- One slow target must not block all results.
- Do not store or display response bodies.
- Sanitize errors.

### 10.3 Target restrictions

Health checks may target only:

- Registered detected tailnet-device DNS names.
- Registered detected Tailscale IPs.
- Localhost for Tailnet Atlas itself.

Reject arbitrary public internet domains and unregistered addresses. Do not expose a generic proxy or arbitrary URL-fetch API.

### 10.4 TLS

Verify certificates by default. Allow `tls_verify: false` only per service and display a warning when disabled.

## 11. Tailscale Serve integration

### 11.1 Local binding

Default bind address:

```text
127.0.0.1
```

Never default to `0.0.0.0`.

### 11.2 Compatibility

Tailscale Serve CLI syntax varies by installed version. Before generating changes:

- Inspect `tailscale serve --help`.
- Detect supported flags and forms.
- Encapsulate compatibility in the Tailscale adapter.
- Avoid assumptions based on one historical syntax.

### 11.3 Mutation safety

Before modifying Serve:

1. Inspect current state.
2. Save a sanitized before-state snapshot.
3. Detect route conflicts.
4. Show the exact proposed command or change.
5. Require approval.
6. Never invoke Funnel.
7. Never erase unrelated routes.
8. Verify the result.
9. Record what Tailnet Atlas configured.

If the root route is occupied, offer to abort, use a supported subpath, or let the user resolve it manually. Do not overwrite automatically.

If browser authorization is required, show the authorization URL and resume verification after the user confirms completion.

## 12. Systemd user service

When available, install a user-level unit under:

```text
~/.config/systemd/user/tailnet-atlas.service
```

Requirements:

- Run as the user, never root.
- Start after network availability.
- Restart on failure.
- Use the application virtual environment.
- Bind to localhost.
- Read the user configuration.
- Log to the user journal.

If systemd is unavailable, do not enable it automatically in WSL. Provide a foreground command and optional launcher.

## 13. Security model

The MVP is a launcher and read-only status dashboard, not a control plane.

Mandatory restrictions:

- Tailnet-only exposure.
- No Funnel.
- Localhost binding.
- No Docker socket or API.
- No Docker or systemd controls.
- No port scanning.
- No arbitrary command execution.
- No shell in the browser.
- No package updates.
- No secrets or environment values.
- No `.env` parsing.
- No request-body logging.
- No external analytics.
- No unrestricted health targets.

See `docs/security-model.md` for trust boundaries and threat assumptions.

## 14. Project structure

Suggested structure:

```text
tailnet-atlas/
├── README.md
├── LICENSE
├── SECURITY.md
├── CHANGELOG.md
├── AGENTS.md
├── HERMES_TASK.md
├── pyproject.toml
├── install.sh
├── examples/
│   └── config.example.yaml
├── docs/
│   ├── implementation-spec.md
│   ├── architecture.md
│   ├── configuration.md
│   ├── security-model.md
│   └── roadmap.md
├── src/
│   └── tailnet_atlas/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── installer.py
│       ├── health.py
│       ├── services.py
│       ├── web.py
│       ├── tailscale/
│       │   ├── adapter.py
│       │   ├── detection.py
│       │   ├── models.py
│       │   └── serve.py
│       ├── templates/
│       └── static/
├── tests/
│   ├── fixtures/
│   ├── test_config.py
│   ├── test_detection.py
│   ├── test_health.py
│   ├── test_services.py
│   ├── test_cli.py
│   └── test_web.py
└── .github/
    └── workflows/
        └── ci.yml
```

## 15. Tests

### 15.1 Unit coverage

Cover:

- Complete and minimal Tailscale JSON.
- Missing optional fields.
- Changed field shapes.
- Disconnected Tailscale.
- Missing DNS suffix and suffix extraction.
- Device normalization and reconciliation.
- Configuration validation.
- Atomic writes and backups.
- URL construction and override.
- Target restrictions.
- Health classification.
- Redirects, timeouts, and TLS options.
- Invalid references, ports, paths, and duplicate IDs.

### 15.2 Integration coverage

Use local fake HTTP services for:

- Healthy response.
- Redirect.
- Authentication-required response.
- Warning response.
- Timeout.
- Connection failure.

Test rendered pages and web routes using FastAPI test tools.

### 15.3 CI

CI must run:

- Ruff format check.
- Ruff lint.
- MyPy.
- Pytest.
- Package build.
- CLI smoke test.
- Example configuration validation.

## 16. Uninstall

Default uninstall should:

- Stop and remove the app's user unit.
- Remove app code and generated launchers.
- Preserve configuration and backups.
- Explain any remaining Serve route.
- Avoid changing unrelated Serve configuration.

`uninstall --purge` may remove configuration and state only after explicit confirmation.

Before removing a Serve route, verify it still matches the route created by Tailnet Atlas. Never perform a global reset unless proven safe and explicitly approved.

## 17. Deferred features

Do not implement in `0.1.0`:

- Docker or Compose discovery.
- Container controls.
- Systemd controls.
- Port scanning.
- LAN discovery.
- Internet monitoring.
- Tailscale API keys or admin APIs.
- Historical uptime database.
- Prometheus or Grafana.
- ntfy alerts.
- WSL Doctor integration.
- Hermes MCP.
- Browser configuration editor.
- Accounts, roles, or multi-tailnet support.
- Public access.

Design metadata fields so future discovery sources can be represented without changing core service records:

```yaml
source: manual
runtime: unknown
runtime_metadata: {}
```

Potential future values include `docker`, `systemd`, `tailscale-endpoint`, and `imported`.

## 18. Approval gates

Obtain approval before:

1. Installing system packages.
2. Changing Tailscale Serve.
3. Replacing a Serve route.
4. Creating or enabling systemd units.
5. Publishing or tagging releases.
6. Adding real private infrastructure to tracked files.
7. Expanding scope.

## 19. Definition of done

The MVP is complete only when:

- Tailscale detection works on the target host.
- Missing fields and disconnected states fail gracefully.
- Manual fallback works.
- At least three real services can be registered without committing private data.
- Launch URLs work from another tailnet device.
- Health states are classified correctly.
- The dashboard works on desktop and mobile.
- The backend binds only to localhost.
- Serve exposure is private and preserves unrelated routes.
- Setup dry-run performs no mutation.
- Automatic startup works when systemd is available, with a documented fallback otherwise.
- Tests, Ruff, MyPy, build validation, smoke tests, and CI pass.
- Examples and fixtures are sanitized.
- Uninstall behavior is tested.
- Release publication remains approval-gated.

## 20. Completion report

At completion, report:

- What was built and repository state.
- Installed version, local bind address, dashboard URL, and configuration path.
- Auto-detected and manually supplied values.
- Redacted service verification results.
- Tests and checks actually run.
- Every host file, package, service, and Tailscale setting changed.
- Confirmation that deferred features were not added.
- Honest limitations and unresolved issues.
