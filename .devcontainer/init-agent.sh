#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="/output"
mkdir -p "$OUTPUT_DIR"

echo "=== Initializing Vindicta Agent Identity ==="

# --- GPG Key Setup ---

if [ -n "${GPG_PRIVATE_KEY:-}" ]; then
  # === IMPORT EXISTING KEY ===
  echo "Importing provided GPG key..."
  echo "$GPG_PRIVATE_KEY" | base64 -d | gpg --batch --import
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)

  # Trust the key ultimately
  echo "${GPG_KEY_ID}:6:" | gpg --import-ownertrust
  echo "GPG key imported: $GPG_KEY_ID"

  # Validate the key exists on GitHub (read-only check)
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    echo "Validating GPG key on GitHub..."
    EXISTING_KEYS=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/user/gpg_keys")

    if [ "$EXISTING_KEYS" = "200" ]; then
      # Check if our key fingerprint is registered
      KEY_FINGERPRINT=$(gpg --fingerprint "$GPG_KEY_ID" 2>/dev/null | grep -oP '[A-F0-9]{40}' | head -1)
      FOUND=$(curl -s \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/user/gpg_keys" | \
        grep -c "${GPG_KEY_ID}" 2>/dev/null || true)

      if [ "${FOUND:-0}" -gt 0 ]; then
        echo "  ✅ GPG key is registered on GitHub"
      else
        echo "  ⚠️  GPG key NOT found on GitHub — you may need to add it manually"
        echo "     Export: cat $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
      fi
    else
      echo "  ⚠️  Could not validate GPG keys on GitHub (HTTP $EXISTING_KEYS)"
    fi
  fi

else
  # === GENERATE NEW KEY ===
  echo "No GPG_PRIVATE_KEY provided. Generating a new key..."
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
  echo "New GPG key generated: $GPG_KEY_ID"

  # Try to auto-upload the key to GitHub
  UPLOADED=false
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    echo "Attempting to upload GPG key to GitHub..."
    ARMORED_KEY=$(gpg --armor --export "$GPG_KEY_ID")
    UPLOAD_RESPONSE=$(curl -s -w "\n%{http_code}" \
      -X POST https://api.github.com/user/gpg_keys \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -d "$(jq -n --arg key "$ARMORED_KEY" '{armored_public_key: $key}')")

    HTTP_CODE=$(echo "$UPLOAD_RESPONSE" | tail -1)
    RESPONSE_BODY=$(echo "$UPLOAD_RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" = "201" ]; then
      echo "  ✅ GPG key uploaded to GitHub automatically"
      UPLOADED=true
    elif [ "$HTTP_CODE" = "422" ]; then
      echo "  ✅ GPG key already exists on GitHub"
      UPLOADED=true
    elif [ "$HTTP_CODE" = "404" ] || [ "$HTTP_CODE" = "403" ]; then
      echo "  ⚠️  PAT does not have gpg_keys write permission (HTTP $HTTP_CODE)"
      echo "     Falling back to file export."
    else
      echo "  ⚠️  Upload failed (HTTP $HTTP_CODE)"
      echo "     Falling back to file export."
    fi
  fi

  if [ "$UPLOADED" = false ]; then
    echo ""
    echo "=== MANUAL STEP REQUIRED ==="
    echo "Add this public key to the bot's GitHub account: https://github.com/settings/keys"
    echo "The key has been exported to: $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
  fi
fi

# --- Export keys to host volume ---

PUBKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
gpg --armor --export "$GPG_KEY_ID" > "$PUBKEY_FILE"
echo "Public key exported to: $PUBKEY_FILE"

PRIVKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-private-b64.txt"
gpg --armor --export-secret-keys "$GPG_KEY_ID" | base64 -w0 > "$PRIVKEY_FILE"
echo "Private key (base64) exported to: $PRIVKEY_FILE"

# --- Configure git identity ---

git config --global user.name "${AGENT_NAME:-vindicta-bot}"
git config --global user.email "${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}"
git config --global user.signingkey "$GPG_KEY_ID"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg

# --- Configure GitHub CLI auth ---

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "$GITHUB_TOKEN" | gh auth login --with-token
  echo "GitHub CLI authenticated."
fi

echo ""
echo "=== Agent Identity Ready ==="
echo "  Name:      $(git config user.name)"
echo "  Email:     $(git config user.email)"
echo "  GPG:       $GPG_KEY_ID"
echo "  PubKey:  $PUBKEY_FILE"
echo "  PrivKey: $PRIVKEY_FILE"
echo "  PubKey:  $PUBKEY_FILE"
echo "  PrivKey: $PRIVKEY_FILE"
echo ""
echo "Add the public key to the bot's GitHub account:"
echo "  https://github.com/settings/keys"
