# Vindicta-Agents

Agent infrastructure, automation, and identity management for the [Vindicta Platform](https://github.com/vindicta-platform).

## Overview

This repo contains:

- **`.devcontainer/`** — Dev container for isolated agent operations with GPG commit signing
- **`agents/`** — Agent definitions and configurations
- **`automation/`** — Scripts for org-wide automation (branch protections, etc.)
- **`tests/`** — Test suites for agent infrastructure

## Agent Dev Container

### Quick Start

1. **Clone and checkout the branch:**
   ```bash
   git clone https://github.com/vindicta-platform/Vindicta-Agents.git
   cd Vindicta-Agents
   ```

2. **Copy the environment template:**
   ```bash
   cp .devcontainer/.env.example .devcontainer/.env
   ```

3. **Fill in your secrets** in `.devcontainer/.env`:
   - `AGENT_GITHUB_TOKEN` — Fine-Grained PAT from the `vindicta-bot` account
   - `GPG_PRIVATE_KEY` — Base64-encoded GPG private key (leave blank for auto-generation)

4. **Build and run:**

   **VS Code:** Open in Dev Containers extension (auto-builds and runs `init-agent.sh`).

   **Docker CLI (PowerShell on Windows):**
   ```powershell
   docker build --no-cache -t vindicta-agent .devcontainer/
   docker run --rm -e AGENT_NAME=vindicta-bot -e "AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com" -it vindicta-agent init-agent.sh
   ```

   **Docker CLI (bash/macOS/Linux):**
   ```bash
   docker build --no-cache -t vindicta-agent .devcontainer/
   docker run --rm \
     -e AGENT_NAME=vindicta-bot \
     -e AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com \
     -it vindicta-agent init-agent.sh
   ```

5. **On first run** (no GPG key), the init script will:
   - Generate a 4096-bit RSA GPG key for `vindicta-bot`
   - Print the public key — **add this to the bot's GitHub account**
   - Print the base64 export command — **save this to `.env` for future containers**

> **Note:** The Dockerfile includes `dos2unix` to handle Windows CRLF line endings automatically. No manual conversion needed.

### What the Container Does

- Configures `git` identity as `vindicta-bot` (`260104759+vindicta-bot@users.noreply.github.com`)
- Enables automatic GPG signing on all commits and tags
- Authenticates `gh` CLI with the bot's PAT
- All commits from this container will show as **Verified** on GitHub

### GPG Key Lifecycle

| Action | Command |
|---|---|
| Export public key | `gpg --armor --export KEY_ID` |
| Export private key (base64) | `gpg --armor --export-secret-keys KEY_ID \| base64 -w0` |
| List keys | `gpg --list-secret-keys --keyid-format=long` |
| Key expiry | 1 year (re-generate and rotate) |

## Branch Protections

All `vindicta-platform` **public** repos have branch protections on `main`:

- **1 approving review** required before merge
- **Stale reviews dismissed** on new pushes
- **Admin bypass enabled** — org admins can merge without review
- **Force pushes and branch deletion blocked**

> **Note:** Private repos (`Vindicta-Agents`, `.agent`, `.specify`) require GitHub Team plan for branch protections.

To re-apply protections across all repos:
```bash
bash automation/apply-branch-protections.sh
```

## Agent Workflow

```
1. Agent works inside dev container
2. Creates feature branch (e.g., feat/agent-task-123)
3. Makes GPG-signed commits
4. Pushes branch and creates PR via gh CLI
5. brandon-fox reviews and approves
6. PR is merged
```

## Scope & Roadmap

### Current Scope (v1 — Machine User)

- Dedicated `vindicta-bot` GitHub account with GPG signing
- Dev container for isolated agent operations
- PAT-based authentication
- Branch protections requiring human approval

### Explicitly Out of Scope

- **GitHub Apps integration** — Not part of this setup. The current machine-user approach is a short-term solution.

### Future: GitHub Apps Migration (v2)

The `vindicta-bot` machine-user account will eventually migrate to become the **owner of a GitHub App**. This enables:

- **Multiple independent bots** — Each with unique identity, permissions, and audit trails, all managed under a single GitHub App installation
- **Installation-based auth** — JWT + installation tokens instead of PATs (more secure, auto-rotating)
- **Granular permissions** — Per-repository and per-API-scope access control
- **Webhook-driven automation** — Native event subscriptions without polling
- **Rate limit isolation** — Each app gets its own rate limits separate from user accounts

This migration is tracked separately and will be planned when the platform reaches the scale where multiple specialized agents are needed.

## Security

> **⚠️ Never commit secrets.** The `.env` file is gitignored. See [issue #4](https://github.com/vindicta-platform/Vindicta-Agents/issues/4) for secret scanning enforcement.

## Related Issues

- [#4](https://github.com/vindicta-platform/Vindicta-Agents/issues/4) — Secret scanning
- [#5](https://github.com/vindicta-platform/Vindicta-Agents/issues/5) — Purchase vindicta.dev
- [#6](https://github.com/vindicta-platform/Vindicta-Agents/issues/6) — Automated GPG verification testing
- [#7](https://github.com/vindicta-platform/Vindicta-Agents/issues/7) — Branch protection validation spike
- [#8](https://github.com/vindicta-platform/Vindicta-Agents/issues/8) — MADR & Architecture documentation

## License

See [LICENSE](LICENSE).
