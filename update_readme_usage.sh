#!/usr/bin/env bash
# Usage: ./update_readme_usage.sh [USAGE_BLOCK] [README]
BLK="${1:-README_USAGE_BLOCK.md}"
READ="${2:-README.md}"
TMP="$READ.tmp"

# Replace existing block delimited by markers, or append if not present.
if grep -q '<!-- diff-risk:usage:start -->' "$READ"; then
  awk -v F="$BLK" '
    BEGIN { while ((getline l < F) > 0) blk = blk l ORS; close(F) }
    /<!-- diff-risk:usage:start -->/ { print blk; inside=1; next }
    /<!-- diff-risk:usage:end -->/   { inside=0; next }
    !inside { print }
  ' "$READ" > "$TMP" && mv "$TMP" "$READ"
else
  printf '\n' >> "$READ"
  cat "$BLK" >> "$READ"
fi

echo "README usage block updated ✅"
