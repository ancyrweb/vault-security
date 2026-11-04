#!/usr/bin/env python3
"""Validate links in a markdown knowledge graph.

Checks wikilinks ([[Note]], [[Note|alias]], [[Note\\|alias]] in tables,
[[Note#anchor]], ![[embed.png]]) and relative markdown links ([text](path.md)).

Reports broken links, ambiguous basenames, orphan notes, and counts.
Exits 1 if any link is broken, so it can gate "done".

Usage:
    check_links.py VAULT_ROOT [--subtree PATH] [--exclude DIR ...] [--quiet]

    VAULT_ROOT   Root of the vault/repo. The note index is built from here,
                 because basename resolution is vault-wide.
    --subtree    Only check links *found in* this path (relative to root).
                 Targets may live anywhere in the vault.
    --exclude    Extra directory names to skip (repeatable).
"""

import argparse
import os
import re
import sys
from collections import defaultdict

DEFAULT_EXCLUDES = {".git", ".trash", ".obsidian", ".serena", "node_modules",
                    ".venv", "__pycache__", ".next", "dist", "build"}

# [[target]] / [[target|alias]] / ![[target]] — captures the raw inner text.
WIKILINK = re.compile(r"!?\[\[([^\]]+)\]\]")
# [text](target) — skips external URLs and pure anchors at resolve time.
MDLINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def is_excluded(path, root, excludes):
    rel = os.path.relpath(path, root)
    return any(part in excludes for part in rel.split(os.sep))


def walk_files(root, excludes):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for name in filenames:
            yield os.path.join(dirpath, name)


def build_index(root, excludes):
    """Map basename -> [relative paths]. Notes are keyed without the .md
    extension (how wikilinks name them); other files keep theirs (embeds)."""
    by_name = defaultdict(list)
    notes = []
    for full in walk_files(root, excludes):
        rel = os.path.relpath(full, root)
        base = os.path.basename(rel)
        if base.lower().endswith(".md"):
            stem = base[:-3]
            by_name[stem].append(rel)
            notes.append(rel)
        else:
            by_name[base].append(rel)
    return by_name, notes


def clean_wikilink_target(raw):
    """Strip alias and anchor from a wikilink's inner text.

    Order matters: the escaped pipe (\\|) is how a wikilink alias is written
    inside a markdown table, and it must be handled before the plain pipe or
    the trailing backslash leaks into the target and looks broken.
    """
    target = raw.replace("\\|", "|").split("|", 1)[0]
    target = target.split("#", 1)[0]
    return target.strip()


def resolve(target, by_name, root, source_rel):
    """True if a wikilink target resolves. Accepts bare basenames (Obsidian's
    default), basenames with .md, and path-qualified forms."""
    if not target:
        return False
    candidates = [target]
    if target.lower().endswith(".md"):
        candidates.append(target[:-3])
    for cand in candidates:
        if cand in by_name:
            return True
        # Path-qualified: [[folder/Note]] — match against known note paths.
        norm = cand.replace("\\", "/").lstrip("./")
        for paths in by_name.values():
            for p in paths:
                pn = p.replace(os.sep, "/")
                if pn == norm or pn == norm + ".md" or pn.endswith("/" + norm) \
                   or pn.endswith("/" + norm + ".md"):
                    return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--subtree", default=None)
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    by_name, notes = build_index(root, excludes)

    scope = os.path.abspath(os.path.join(root, args.subtree)) if args.subtree else root
    if not os.path.exists(scope):
        print(f"error: subtree not found: {scope}", file=sys.stderr)
        return 2

    broken = []
    escaped_pipe_links = []
    total_links = 0
    targets_seen = set()
    linked_targets = defaultdict(set)   # target stem -> set of source files

    for full in walk_files(scope, excludes):
        if not full.lower().endswith(".md"):
            continue
        source_rel = os.path.relpath(full, root)
        try:
            text = open(full, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError) as exc:
            print(f"warn: could not read {source_rel}: {exc}", file=sys.stderr)
            continue

        for raw in WIKILINK.findall(text):
            if "\\|" in raw:
                escaped_pipe_links.append((source_rel, raw))
            target = clean_wikilink_target(raw)
            if not target:           # [[#anchor]] — same-file, nothing to resolve
                continue
            total_links += 1
            targets_seen.add(target)
            linked_targets[target].add(source_rel)
            if not resolve(target, by_name, root, source_rel):
                broken.append((source_rel, raw, target))

        for raw in MDLINK.findall(text):
            t = raw.split()[0] if raw.split() else raw
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", t) or t.startswith("#"):
                continue          # external scheme or pure anchor
            if not t.lower().endswith(".md"):
                continue          # only validate markdown targets here
            total_links += 1
            dest = os.path.normpath(os.path.join(os.path.dirname(full),
                                                 t.split("#", 1)[0]))
            if not os.path.exists(dest):
                broken.append((source_rel, raw, t))
            else:
                # Record inbound edges for relative links too, otherwise every
                # page in a plain-markdown repo looks like an orphan.
                stem = os.path.basename(dest)
                if stem.lower().endswith(".md"):
                    stem = stem[:-3]
                targets_seen.add(stem)
                linked_targets[stem].add(source_rel)

    # Ambiguity only matters for names actually linked to: two notes sharing a
    # basename make every basename link to it resolve unpredictably.
    ambiguous = {name: paths for name, paths in by_name.items()
                 if len(paths) > 1 and name in targets_seen}

    # Orphans: notes inside the subtree that nothing links to.
    subtree_notes = [n for n in notes
                     if os.path.abspath(os.path.join(root, n)).startswith(scope + os.sep)
                     or os.path.abspath(os.path.join(root, n)) == scope]
    orphans = []
    for rel in subtree_notes:
        stem = os.path.basename(rel)[:-3]
        linkers = linked_targets.get(stem, set())
        if not (linkers - {rel}):
            orphans.append(rel)

    if not args.quiet:
        print(f"notes indexed (vault):   {len(notes)}")
        print(f"notes in scope:          {len(subtree_notes)}")
        print(f"links checked:           {total_links}")
        print(f"unique targets:          {len(targets_seen)}")
        if escaped_pipe_links:
            print(f"escaped-pipe aliases:    {len(escaped_pipe_links)} (correct table syntax)")
        print()

    if broken:
        print(f"BROKEN LINKS ({len(broken)}):")
        for src, raw, target in broken:
            print(f"  {src}\n    [[{raw}]] -> unresolved: {target!r}")
        print()
    elif not args.quiet:
        print("BROKEN LINKS: none")

    if ambiguous:
        print(f"AMBIGUOUS TARGETS ({len(ambiguous)}) "
              f"- basename links resolve unpredictably:")
        for name, paths in sorted(ambiguous.items()):
            print(f"  {name!r}:")
            for p in paths:
                print(f"    {p}")
        print()
    elif not args.quiet:
        print("AMBIGUOUS TARGETS: none")

    if orphans and not args.quiet:
        print(f"ORPHANS ({len(orphans)}) - in scope, nothing links to them:")
        for rel in orphans:
            print(f"  {rel}")
        print("  (a hub linked only from outside the subtree is expected here)")
        print()
    elif not args.quiet:
        print("ORPHANS: none")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
