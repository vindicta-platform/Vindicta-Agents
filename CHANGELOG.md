# Changelog

All notable changes to the Vindicta-Agents project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-07

### Added

- **Dev Container** — Base (`Dockerfile`) and slim (`Dockerfile.slim`) images for agent operations
- **GPG Signing** — Automatic key generation, import, and GitHub upload via `init-agent.sh`
- **PAT Validation** — Upfront access checks with read/write detection for GPG keys
- **Token Flexibility** — Accepts `GITHUB_TOKEN` or `AGENT_GITHUB_TOKEN` (errors if both set)
- **Volume Detection** — Skips file export when no `/output` volume mounted and PAT has write access
- **Build Pipeline** — `build.sh` / `build.cmd` for local Docker builds (base, slim, or both)
- **Branch Protections** — `automation/apply-branch-protections.sh` for org-wide protection rules
- **Test Suite** — Three verification scripts:
  - `tests/test-docker-build.sh` — image build, binaries, GPG config
  - `tests/test-gpg-signing.sh` — key gen, export, re-import, signed commits
  - `tests/test-branch-protections.sh` — org-wide protection validation
- **Setup Guides** — IDE-specific dev container docs for VS Code, PyCharm, Windsurf, Antigravity, Docker CLI
- **README** — Full documentation with quick start, GPG lifecycle, roadmap, and security notes

### Infrastructure

- Branch protections applied to 22/25 `vindicta-platform` repos (3 private repos blocked by GitHub Free)
- `vindicta-bot` machine user account created and added to org
- GitHub Apps noted as future v2 migration path (explicitly out of scope)

[0.1.0]: https://github.com/vindicta-platform/Vindicta-Agents/releases/tag/v0.1.0
