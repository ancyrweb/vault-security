#!/usr/bin/env bash
# Commit the processed source notes and the knowledge graph as a sync point.
#
# Usage: commit_sync.sh BODY_FILE [VAULT_ROOT]
#
# Only courses/, videos/, articles/ and knowledge/ are committed; anything
# else the user has staged or modified (e.g. .obsidian/) is left untouched.
# The subject is always "knowledge: sync" — changed_sources.sh relies on it.

set -euo pipefail

body_file="$1"
cd "${2:-.}"
cd "$(git rev-parse --show-toplevel)"

paths=()
for d in courses videos articles knowledge; do
  # Include dirs that exist, or that were tracked and are now fully deleted.
  if [ -e "$d" ] || [ -n "$(git ls-files -- "$d" | head -1)" ]; then
    paths+=("$d")
  fi
done

if [ ${#paths[@]} -eq 0 ]; then
  echo "nothing to commit: no source or knowledge folders" >&2
  exit 0
fi

git add -A -- "${paths[@]}"

if git diff --cached --quiet -- "${paths[@]}"; then
  echo "nothing to commit: source and knowledge folders unchanged"
  exit 0
fi

msg=$(mktemp)
trap 'rm -f "$msg"' EXIT
{ printf 'knowledge: sync\n\n'; cat "$body_file"; } > "$msg"
git commit -q -F "$msg" -- "${paths[@]}"
git log -1 --stat --format='%h %s'
