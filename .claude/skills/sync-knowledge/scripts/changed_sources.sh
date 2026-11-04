#!/usr/bin/env bash
# List source notes changed since the last `knowledge: sync` commit,
# including uncommitted and untracked changes.
#
# Usage: changed_sources.sh [VAULT_ROOT]
#
# Output (tab-separated):
#   BASE	<sha>|none
#   A	<path>			added (new file, tracked or untracked)
#   M	<path>			modified
#   D	<path>			deleted
#   R	<old path>	<new path>	renamed / moved
# A trailing "	(empty)" marks files with no content yet.
# Only Markdown files under courses/, videos/, articles/ are reported.

set -euo pipefail

cd "${1:-.}"
cd "$(git rev-parse --show-toplevel)"

SOURCES=(courses videos articles)
SYNC_SUBJECT='knowledge: sync'

base=$(git log -1 --format=%H --grep="^${SYNC_SUBJECT}\$" 2>/dev/null || true)
printf 'BASE\t%s\n' "${base:-none}"

annotate() {
  # $1 = path; prints "(empty)" marker if file exists and is blank
  if [ -f "$1" ] && ! grep -q '[^[:space:]]' "$1" 2>/dev/null; then
    printf '\t(empty)'
  fi
}

is_md() { [[ "$1" == *.md ]]; }

{
  if [ -n "$base" ]; then
    # Base commit vs working tree: covers committed + uncommitted tracked changes.
    git diff -M --name-status "$base" -- "${SOURCES[@]}" | while IFS=$'\t' read -r status a b; do
      case "$status" in
        R*) is_md "$b" || is_md "$a" || continue
            printf 'R\t%s\t%s%s\n' "$a" "$b" "$(annotate "$b")" ;;
        A|M|D) is_md "$a" || continue
            printf '%s\t%s%s\n' "$status" "$a" "$(annotate "$a")" ;;
        *)  is_md "$a" || continue
            printf 'M\t%s%s\n' "$a" "$(annotate "$a")" ;;
      esac
    done
  else
    # First sync: every existing source note is new.
    git ls-files --cached -- "${SOURCES[@]}" | while IFS= read -r f; do
      [ -f "$f" ] && is_md "$f" && printf 'A\t%s%s\n' "$f" "$(annotate "$f")"
    done
  fi

  # Untracked files are invisible to git diff; report them as added.
  git ls-files --others --exclude-standard -- "${SOURCES[@]}" | while IFS= read -r f; do
    is_md "$f" && printf 'A\t%s%s\n' "$f" "$(annotate "$f")"
  done
} | sort -u -t$'\t' -k2,2
