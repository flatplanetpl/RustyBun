#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# This is trusted project configuration, not an upstream script.
# shellcheck disable=SC1091
source "$ROOT/upstream/bun-baseline.env"
DEST="${1:-$ROOT/work/bun}"
MODE="${2:-source}"
case "$MODE" in
  source) EXPECTED="$BUN_SOURCE_SHA" ;;
  reference) EXPECTED="$BUN_RUN_SHA" ;;
  *) echo "Usage: bash $0 [destination] [source|reference]" >&2; exit 2 ;;
esac

if [[ -e "$DEST" ]]; then
  if [[ ! -d "$DEST/.git" ]]; then
    echo "ERROR: destination exists but is not a standalone Git checkout" >&2; exit 1
  fi
  if [[ "$(git -C "$DEST" remote get-url origin)" != "$BUN_UPSTREAM_REPO" ]]; then
    echo "ERROR: unexpected origin; leaving checkout unchanged" >&2; exit 1
  fi
  if [[ -n "$(git -C "$DEST" status --porcelain)" ]]; then
    echo "ERROR: dirty checkout; leaving changes untouched" >&2; exit 1
  fi
else
  mkdir -p "$(dirname "$DEST")"
  git init "$DEST"
  git -C "$DEST" remote add origin "$BUN_UPSTREAM_REPO"
fi

# Fetch only the pinned object, not current main or the full rewrite history.
if ! git -C "$DEST" cat-file -e "$EXPECTED^{commit}" 2>/dev/null; then
  git -C "$DEST" fetch --no-tags --depth=1 origin "$EXPECTED"
fi
git -C "$DEST" checkout --detach "$EXPECTED"
ACTUAL="$(git -C "$DEST" rev-parse HEAD)"
[[ "$ACTUAL" == "$EXPECTED" ]] || { echo 'ERROR: SHA mismatch' >&2; exit 1; }
if [[ "$MODE" == reference ]]; then
  PARENT="$(git -C "$DEST" cat-file -p HEAD | sed -n 's/^parent //p' | head -n 1)"
  [[ "$PARENT" == "$BUN_SOURCE_SHA" ]] || { echo 'ERROR: reference parent mismatch' >&2; exit 1; }
fi
printf 'Pinned checkout ready: %s\nMode: %s\nSHA: %s\n' "$DEST" "$MODE" "$ACTUAL"
echo 'This checkout is not a blind sandbox. Use build-context-pack.py for agent input.'
