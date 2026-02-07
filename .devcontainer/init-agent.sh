#!/usr/bin/env bash
set -euo pipefail

echo "=== Initializing Vindicta Agent Identity ==="

# Import GPG private key from environment
if [ -n "${GPG_PRIVATE_KEY:-}" ]; then
  echo "$GPG_PRIVATE_KEY" | base64 -d | gpg --batch --import
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)

  # Trust the key ultimately
  echo "${GPG_KEY_ID}:6:" | gpg --import-ownertrust

  echo "GPG key imported: $GPG_KEY_ID"
else
  echo "WARNING: No GPG_PRIVATE_KEY set. Generating a new key..."
  cat > /tmp/gpg-key-params <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: ${AGENT_NAME:-vindicta-bot}
Name-Email: ${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}
Expire-Date: 1y
%commit
EOF
  gpg --batch --gen-key /tmp/gpg-key-params
  rm /tmp/gpg-key-params
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)

  echo ""
  echo "=== NEW GPG KEY GENERATED ==="
  echo "Add this public key to the agent's GitHub account:"
  echo ""
  gpg --armor --export "$GPG_KEY_ID"
  echo ""
  echo "Export the private key for future containers:"
  echo "  gpg --armor --export-secret-keys $GPG_KEY_ID | base64 -w0"
  echo ""
fi

# Configure git identity
git config --global user.name "${AGENT_NAME:-vindicta-bot}"
git config --global user.email "${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}"
git config --global user.signingkey "$GPG_KEY_ID"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg

# Configure GitHub CLI auth
if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "$GITHUB_TOKEN" | gh auth login --with-token
  echo "GitHub CLI authenticated."
fi

echo "=== Agent Identity Ready ==="
echo "  Name:  $(git config user.name)"
echo "  Email: $(git config user.email)"
echo "  GPG:   $GPG_KEY_ID"
