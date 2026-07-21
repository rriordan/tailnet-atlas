# Configuration

## Default path

```text
~/.config/tailnet-atlas/config.yaml
```

Configuration is local and may contain private infrastructure metadata. Do not commit a real configuration file to a public repository.

## Example

See `examples/config.example.yaml` for a sanitized complete example.

## Top-level sections

### `schema_version`

Required integer used for future migrations.

### `dashboard`

Controls display and local runtime behavior.

| Field | Purpose | Default |
|---|---|---|
| `title` | Dashboard title | `Tailnet Atlas` |
| `bind_host` | Local bind address | `127.0.0.1` |
| `port` | Local web port | `8787` |
| `base_path` | Dashboard path | `/` |
| `refresh_seconds` | UI state refresh | `30` |
| `health_interval_seconds` | Health-check interval | `30` |
| `health_timeout_seconds` | Per-target timeout | `4` |
| `theme` | `light`, `dark`, or `system` | `system` |

`bind_host` must remain localhost for normal operation. Non-local binding should not be exposed as a routine option in the MVP.

### `tailnet`

Stores the confirmed local tailnet identity.

| Field | Purpose |
|---|---|
| `dns_suffix` | MagicDNS tailnet suffix |
| `local_device` | ID of the dashboard host |
| `detection_source` | `automatic`, `manual`, or `mixed` |

### `devices`

Stores normalized device metadata and user preferences.

Required or common fields:

- `id`
- `display_name`
- `machine_name`
- `dns_name`
- `tailscale_ips`
- `os`
- `visible`
- `pinned`

Discovery refresh may update detected metadata, but it must preserve display names, visibility, pins, and service associations.

### `services`

Each service has:

- Unique `id`
- `name`
- Optional `description`
- `category`
- Referenced `device`
- `scheme`: `http` or `https`
- `port`: 1–65535
- `path` beginning with `/`
- Optional `url_override`
- `favorite`
- Tags
- Source and runtime metadata
- Health configuration

## Health configuration

```yaml
health:
  enabled: true
  method: GET
  path: /health
  follow_redirects: true
  tls_verify: true
```

The MVP should support `GET` and may support `HEAD` if behavior is well tested. Response bodies must not be retained or displayed.

## URL construction

Without an override:

```text
<scheme>://<device DNS name or Tailscale IP>:<port><path>
```

The address-selection order is:

1. Full device DNS name.
2. Machine name plus tailnet DNS suffix.
3. Tailscale IP.

## Validation

Validation must reject:

- Duplicate IDs.
- Unknown device references.
- Invalid ports.
- Paths without `/`.
- Unsupported schemes.
- Arbitrary public health targets.
- Overrides outside registered tailnet devices or localhost.
- Secret-like fields that are not part of the documented schema.

## Writes and backups

CLI changes must:

1. Load and validate the current file.
2. Construct a complete candidate model.
3. Write a temporary file.
4. Validate the serialized candidate.
5. Preserve the previous valid file.
6. Replace atomically.

The CLI should show the configuration path and provide a redacted `config show` view suitable for diagnostics.

## Private configuration hygiene

Do not include in tracked files:

- Real tailnet suffixes.
- Tailscale IPs.
- Internal service URLs.
- Credentials or cookies.
- Personal device names when they reveal identity or location.

Use the example file as a template and keep the actual file under the user's configuration directory.
