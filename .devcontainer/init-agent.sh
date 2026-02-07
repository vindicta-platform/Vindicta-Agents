#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="/output"
mkdir -p "$OUTPUT_DIR"

echo "=== Initializing Vindicta Agent Identity ==="
echo ""

# --- PAT Access Check ---

GPG_READ=false
GPG_WRITE=false

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "[PAT] Checking GitHub token permissions..."

  # Test GPG read access
  GPG_READ_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/user/gpg_keys")

  if [ "$GPG_READ_RESPONSE" = "200" ]; then
    GPG_READ=true
    echo "  ✅ GPG keys: READ access"
  else
    echo "  ❌ GPG keys: no read access (HTTP $GPG_READ_RESPONSE)"
  fi

  # Test GPG write access by sending a dry-run POST with an invalid key
  # A 422 (validation error) means we have write access but the key was invalid
  # A 404/403 means we don't have write access
  GPG_WRITE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "https://api.github.com/user/gpg_keys" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d '{"armored_public_key": "test"}')

  if [ "$GPG_WRITE_RESPONSE" = "422" ]; then
    GPG_WRITE=true
    echo "  ✅ GPG keys: WRITE access"
  elif [ "$GPG_WRITE_RESPONSE" = "201" ]; then
    GPG_WRITE=true
    echo "  ✅ GPG keys: WRITE access"
  else
    echo "  ❌ GPG keys: no write access (HTTP $GPG_WRITE_RESPONSE)"
  fi

  # Check basic user info
  USER_LOGIN=$(curl -s \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/user" | jq -r '.login // "unknown"')
  echo "  👤 Authenticated as: $USER_LOGIN"
  echo ""
else
  echo "[PAT] No GITHUB_TOKEN provided. GitHub features disabled."
  echo ""
fi

# --- GPG Key Setup ---

if [ -n "${GPG_PRIVATE_KEY:-}" ]; then
  # === IMPORT EXISTING KEY ===
  echo "[GPG] Importing provided GPG key..."
  echo "$GPG_PRIVATE_KEY" | base64 -d | gpg --batch --import 2>/dev/null
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)

  # Trust the key ultimately
  echo "${GPG_KEY_ID}:6:" | gpg --import-ownertrust 2>/dev/null
  echo "  Key imported: $GPG_KEY_ID"

  # Validate the key exists on GitHub (read-only check)
  if [ "$GPG_READ" = true ]; then
    echo "[GPG] Validating key is registered on GitHub..."
    FOUND=$(curl -s \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/user/gpg_keys" | \
      grep -c "${GPG_KEY_ID}" 2>/dev/null || true)

    if [ "${FOUND:-0}" -gt 0 ]; then
      echo "  ✅ Key is registered on GitHub"
    else
      echo "  ⚠️  Key NOT found on GitHub"
      if [ "$GPG_WRITE" = true ]; then
        echo "  Uploading key to GitHub..."
        ARMORED_KEY=$(gpg --armor --export "$GPG_KEY_ID")
        UPLOAD_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
          -X POST "https://api.github.com/user/gpg_keys" \
          -H "Authorization: Bearer $GITHUB_TOKEN" \
          -H "Accept: application/vnd.github+json" \
          -d "$(jq -n --arg key "$ARMORED_KEY" '{armored_public_key: $key}')")
        if [ "$UPLOAD_CODE" = "201" ] || [ "$UPLOAD_CODE" = "422" ]; then
          echo "  ✅ Key uploaded to GitHub"
        else
          echo "  ❌ Upload failed (HTTP $UPLOAD_CODE)"
          echo "  Add manually: https://github.com/settings/keys"
        fi
      else
        echo "  ℹ️  PAT lacks write access. Add the key manually:"
        echo "     1. Copy: $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
        echo "     2. Paste at: https://github.com/settings/keys"
        echo ""
        echo "  To enable auto-upload on next run, add 'admin:gpg_key' scope (classic PAT)"
        echo "  or 'gpg_keys: write' permission (fine-grained PAT)."
      fi
    fi
  fi

else
  # === GENERATE NEW KEY ===
  echo "[GPG] No GPG_PRIVATE_KEY provided. Generating a new key..."
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
  gpg --batch --gen-key /tmp/gpg-key-params 2>/dev/null
  rm /tmp/gpg-key-params
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)
  echo "  New key generated: $GPG_KEY_ID"

  # Try to auto-upload
  if [ "$GPG_WRITE" = true ]; then
    echo "[GPG] Uploading key to GitHub..."
    ARMORED_KEY=$(gpg --armor --export "$GPG_KEY_ID")
    UPLOAD_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -X POST "https://api.github.com/user/gpg_keys" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -d "$(jq -n --arg key "$ARMORED_KEY" '{armored_public_key: $key}')")

    if [ "$UPLOAD_CODE" = "201" ]; then
      echo "  ✅ Key uploaded to GitHub automatically"
    elif [ "$UPLOAD_CODE" = "422" ]; then
      echo "  ✅ Key already exists on GitHub"
    else
      echo "  ❌ Upload failed (HTTP $UPLOAD_CODE). Add manually."
    fi
  else
    echo ""
    echo "  ========================================"
    echo "  MANUAL STEP REQUIRED"
    echo "  ========================================"
    echo "  The key could not be uploaded automatically."
    if [ -n "${GITHUB_TOKEN:-}" ]; then
      echo "  Your PAT does not have GPG write permission."
      echo ""
      echo "  To fix for next run, update your PAT with:"
      echo "    - Classic PAT:       add 'admin:gpg_key' scope"
      echo "    - Fine-Grained PAT:  add 'gpg_keys: write' permission"
    else
      echo "  No GITHUB_TOKEN was provided."
    fi
    echo ""
    echo "  For now, add the key manually:"
    echo "    1. Copy:  $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
    echo "    2. Go to: https://github.com/settings/keys"
    echo "    3. Click 'New GPG key' and paste the contents"
    echo "  ========================================"
  fi
fi

# --- Export keys to host volume ---

echo ""
echo "[Export] Writing keys to $OUTPUT_DIR/"
PUBKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
gpg --armor --export "$GPG_KEY_ID" > "$PUBKEY_FILE"
echo "  Public key:  $PUBKEY_FILE"

PRIVKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-private-b64.txt"
gpg --armor --export-secret-keys "$GPG_KEY_ID" | base64 -w0 > "$PRIVKEY_FILE"
echo "  Private key: $PRIVKEY_FILE"

# --- Configure git identity ---

git config --global user.name "${AGENT_NAME:-vindicta-bot}"
git config --global user.email "${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}"
git config --global user.signingkey "$GPG_KEY_ID"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg

# --- Configure GitHub CLI auth ---

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null
  echo "[GH CLI] Authenticated."
fi

echo ""
echo "=== Agent Identity Ready ==="
echo "  Name:    $(git config user.name)"
echo "  Email:   $(git config user.email)"
echo "  GPG:     $GPG_KEY_ID"
echo "  PubKey:  $PUBKEY_FILE"
echo "  PrivKey: $PRIVKEY_FILE"
if [ "$GPG_READ" = true ]; then
  echo "  GitHub:  GPG read ✅"
fi
if [ "$GPG_WRITE" = true ]; then
  echo "  GitHub:  GPG write ✅"
fi
