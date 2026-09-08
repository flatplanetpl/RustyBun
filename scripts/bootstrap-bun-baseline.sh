#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT/upstream/bun-baseline.env"

DEST="${1:-$ROOT/work/bun}"

if [[ -e "$DEST/.git" ]]; then
  echo "Repository already exists: $DEST"
  git -C "$DEST" fetch --all --tags
else
  mkdir -p "$(dirname "$DEST")"
  git clone --filter=blob:none "$BUN_UPSTREAM_REPO" "$DEST"
fi

git -C "$DEST" checkout --detach "$BUN_RUN_SHA"

ACTUAL="$(git -C "$DEST" rev-parse HEAD)"
if [[ "$ACTUAL" != "$BUN_RUN_SHA" ]]; then
  echo "ERROR: expected $BUN_RUN_SHA but checked out $ACTUAL" >&2
  exit 1
fi

SOURCE_PARENT="$(git -C "$DEST" rev-parse HEAD^)"
if [[ "$SOURCE_PARENT" != "$BUN_SOURCE_SHA" ]]; then
  echo "ERROR: Phase-A parent mismatch: expected $BUN_SOURCE_SHA, got $SOURCE_PARENT" >&2
  exit 1
fi

echo "RustyBun baseline ready"
echo "  worktree: $DEST"
echo "  run SHA:  $ACTUAL"
echo "  source:   $SOURCE_PARENT"
