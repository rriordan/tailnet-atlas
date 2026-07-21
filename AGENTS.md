# AGENTS.md

## Purpose

This repository contains the specification and implementation scaffold for **Tailnet Atlas**, a private dashboard for launching and checking services across a Tailscale tailnet.

## Read order

Before changing code, read:

1. `HERMES_TASK.md`
2. `docs/implementation-spec.md`
3. `docs/architecture.md`
4. `docs/security-model.md`
5. `docs/roadmap.md`

## Scope discipline

The `0.1.0` MVP is tailnet-first. Do not add Docker discovery, Docker control, port scanning, systemd control buttons, public exposure, Tailscale Funnel, historical monitoring, or an unrestricted URL-fetch API.

Docker-hosted services may be entered manually as ordinary URLs. The application must not inspect Docker in the MVP.

## Working rules

- Start with a Phase 0 environment assessment and implementation plan.
- Auto-detect Tailscale metadata first; prompt only for missing or ambiguous values.
- Treat the explicit YAML registry as the authoritative source for services.
- Keep all Tailscale CLI access behind a compatibility adapter.
- Bind the web server to `127.0.0.1` by default.
- Require explicit approval before mutating Tailscale Serve configuration.
- Never invoke or enable Tailscale Funnel.
- Never commit real tailnet suffixes, Tailscale IPs, service URLs, secrets, or private topology.
- Keep setup mutations visible, reversible, and covered by dry-run behavior.
- Do not claim tests or checks passed unless they were executed.
- Prefer small, testable modules over a large framework.
- Preserve user configuration and unrelated Tailscale Serve routes.

## Approval gates

Stop and request approval before:

1. Installing system packages.
2. Modifying Tailscale Serve.
3. Replacing an existing Serve route.
4. Creating or enabling a systemd unit.
5. Publishing the repository or a release.
6. Adding real service inventory to a tracked file.
7. Expanding beyond the MVP.

Routine source edits, local tests, fixtures, and non-mutating dry-runs do not require repeated approval after the implementation plan is approved.

## Quality bar

The implementation is not complete until:

- Ruff passes.
- MyPy passes at strict or near-strict settings.
- Pytest passes.
- CI passes.
- Configuration validation and atomic writes are tested.
- Tailscale JSON parsing handles missing and changed fields gracefully.
- Health checks cannot target arbitrary internet domains.
- Setup dry-run makes no changes.
- Uninstall preserves configuration by default and does not erase unrelated Serve routes.

## Commit hygiene

- Use focused commits.
- Do not mix private host configuration with reusable application code.
- Use sanitized fixtures and fictional examples.
- Update documentation when behavior or scope changes.
