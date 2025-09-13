#!/usr/bin/env bash
set -euo pipefail
BLK="${1:-README_USAGE_BLOCK.md}"
READ="${2:-README.md}"

if grep -q '<!-- diff-risk:usage:start -->' "$READ"; then
  awk -v F="$BLK" '
    BEGIN { while ((getline l < F) > 0) blk = blk l ORS; close(F) }
    /<!-- diff-risk:usage:start -->/ { print blk; in=1; next }
    /<!-- diff-risk:usage:end -->/   { in=0; next }
    !in { print }
  ' "$READ" > "$READ.tmp" && mv "$READ.tmp" "$READ"
else
  printf '\n' >> "$READ"
  cat "$BLK" >> "$READ"
fi
echo "README usage block updated ✅"
