#!/usr/bin/env bash
set -euo pipefail
arg="${1-}"
if [[ -z "$arg" ]]; then echo "Usage: $0 <apv.json | raw-json>"; exit 2; fi
if [[ -f "$arg" ]]; then SRC="$arg"
elif [[ "$arg" =~ ^[[:space:]]*\{ || "$arg" =~ ^[[:space:]]*\[ ]]; then
  TMP="$(mktemp)"; printf '%s\n' "$arg" > "$TMP"; SRC="$TMP"
else
  echo "✗ Not found and not JSON: $arg" >&2; exit 66
fi
echo "$SRC"
