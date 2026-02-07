# Docker CLI Setup (Headless / CI)

For environments without an IDE — CI pipelines, headless servers, or manual scripting.

## Build

```bash
cd Vindicta-Agents
docker build --no-cache -t vindicta-agent .devcontainer/
```

## Run (Interactive)

**First run (generate key):**
```bash
docker run --rm \
  -v "$(pwd)/.keys:/output" \
  -v "$(pwd):/workspace" \
  -e AGENT_NAME=vindicta-bot \
  -e AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com \
  -e AGENT_GITHUB_TOKEN=ghp_YOUR_TOKEN \
  -w /workspace \
  -it vindicta-agent bash -c "init-agent.sh && bash"
```

**Subsequent runs (import key):**
```bash
docker run --rm \
  -v "$(pwd)/.keys:/output" \
  -v "$(pwd):/workspace" \
  -e AGENT_NAME=vindicta-bot \
  -e AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com \
  -e AGENT_GITHUB_TOKEN=ghp_YOUR_TOKEN \
  -e GPG_PRIVATE_KEY=$(cat .keys/vindicta-bot-gpg-private-b64.txt) \
  -w /workspace \
  -it vindicta-agent bash -c "init-agent.sh && bash"
```

## Run (One-Shot Command)

```bash
docker run --rm \
  -v "$(pwd):/workspace" \
  -e AGENT_NAME=vindicta-bot \
  -e AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com \
  -e GPG_PRIVATE_KEY=$(cat .keys/vindicta-bot-gpg-private-b64.txt) \
  -w /workspace \
  vindicta-agent bash -c 'init-agent.sh > /dev/null 2>&1 && git log --oneline -5'
```

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `AGENT_NAME` | Yes | Git commit author name |
| `AGENT_EMAIL` | Yes | Git commit author email |
| `AGENT_GITHUB_TOKEN` | Recommended | PAT for `gh` CLI and GPG key upload |
| `GPG_PRIVATE_KEY` | Optional | Base64 GPG private key (skips generation if set) |
