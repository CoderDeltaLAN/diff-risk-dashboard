#!/usr/bin/env bash
arg="${1-}"
if [ -z "$arg" ]; then echo "Usage: $0 <apv.json | raw-json>" >&2; exit 2; fi
if [ -f "$arg" ]; then echo "$arg"; exit 0; fi
case "$arg" in
  \{*|\[* ) tmp="$(mktemp)"; printf '%s\n' "$arg" > "$tmp"; echo "$tmp"; exit 0;;
esac
echo "✗ Not found and not JSON: $arg" >&2; exit 66
