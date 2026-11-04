---
name: sync-knowledge
description: Sync the vault's knowledge graph (`knowledge/`) with new or changed source notes in `courses/`, `videos/` and `articles/`. Detects changes from git since the last `knowledge: sync` commit (including uncommitted and untracked notes), creates or updates concept notes, keeps links between concepts and hubs, cites sources on every note, and commits the result. Use this whenever the user says they finished or updated notes on a course, video or article and wants them "integrated", "synthesized", "processed", "merged into the knowledge base", or asks to "sync", "update", "refresh" or "rebuild" the knowledge graph — even if they don't name the folders or mention git. Also use when source notes were deleted, renamed or moved and the knowledge graph needs to follow.
---

# Sync knowledge

The vault has two layers. **Source notes** (`courses/`, `videos/`, `articles/`) record what one course, video or article taught. **`knowledge/`** is the synthesis: one note per concept, organized by topic rather than by source, interlinked, each citing the sources that contributed to it.

This skill folds source changes into `knowledge/` so it stays an accurate, compact reference. The two ways it goes wrong are **bloat** (appending each source's take, so concepts get restated three times in three voices) and **drift** (knowledge that no longer matches its sources, or links that point nowhere). Most of the guidance below exists to prevent one of those.

Scripts live in this skill's `scripts/` folder. Run everything from the vault root.

## 1. Find what changed

```bash
bash .claude/skills/sync-knowledge/scripts/changed_sources.sh
```

The first line is `BASE <sha>`: the last `knowledge: sync` commit, or `none` on the first run (then every source note counts as added). The other lines list Markdown source notes as `A`/`M`/`D`/`R` (added, modified, deleted, renamed). This compares the base commit with the **working tree**, so committed, uncommitted and untracked changes are all included.

- If no files are listed, say so and stop.
- Files marked `(empty)` have no content yet. Skip them. They get committed with the sync, and once they're filled in they show up as modified.
- A `D` and an `A` with similar paths, or the same content under a new path, are probably an untracked move. Treat them as a rename.

## 2. Understand each change

- **Added**: read the whole note.
- **Modified**: `git diff <base> -- "<path>"` shows exactly what changed. Read the full current note as well, so you understand the context around the change.
- **Deleted**: `git show <base>:"<path>"` recovers what it said. `grep -rl "<path without .md>" knowledge/` finds the notes that cite it.
- **Renamed**: no content work, unless the diff also shows edits. Only the citations need updating (step 5).

For each source, list the concepts it teaches. A concept is something a person would look up or link to on its own: a vulnerability class, an attack technique, a protocol, a tool, a principle, a Linux mechanism. Write down the specifics the source gives: commands, flags, payloads, numbers, examples, caveats. These are the most valuable details and the easiest to lose.

## 3. Map concepts onto the existing graph

Before writing anything, find out what `knowledge/` already covers. A duplicate concept is the worst outcome here, because the two copies drift apart and split the backlinks.

```bash
ls knowledge/
grep -ril "<term>\|<synonym>\|<acronym>" knowledge/
grep -rn "^aliases:" knowledge/
```

Search by name, acronym and synonym. IDOR and BOLA are the same concept, and so are XSS and Cross-Site Scripting. Read every candidate note before deciding. Then sort each concept into one of three buckets:

- **Existing note**: fold the new material into it (step 4).
- **New note**: only if the concept has real substance (several facts, not one line) and other notes would plausibly link to it.
- **Bullet in an existing note**: anything too thin for its own note goes into the closest parent note. Promote it to its own note later, once more sources make it substantial.

## 4. Write the notes

### Note format

`knowledge/` is flat: one file per concept, named after the concept's canonical full name in Title Case (`Cross-Site Scripting.md`, `Broken Object Level Authorization.md`). Obsidian shows the filename as the title, so don't add an H1.

```markdown
---
aliases: [XSS]
---
**Cross-Site Scripting (XSS)** is the injection of attacker-controlled script into pages served to other users, so it runs with the victim's session in the site's origin.

## Types
- **Reflected**: payload comes from the request and is echoed back immediately.
- **Stored**: payload is persisted (comments, profiles) and served to every visitor.
- **DOM-based**: client-side JS writes untrusted data into the DOM; the server never sees it.

## Mitigation
- Context-aware output encoding; see [[Content Security Policy]] for defense in depth.
- `HttpOnly` cookies limit session theft but don't prevent the injection.

## Sources
- [[courses/pluralsight/web-app-pentesting/Notes|Web App Pentesting]] (course, Pluralsight)
- [[articles/portswigger-xss/Notes|PortSwigger: Cross-site scripting]] (article)
```

- **Frontmatter**: only `aliases`, and only when the concept has acronyms or alternate names. Leave out other properties unless the vault starts using them.
- **First line**: the definition, with the term in bold. No preamble.
- **Sections**: pick the ones that fit the concept. For a vulnerability or technique, that's typically how it works, impact, exploitation, detection and mitigation. For a tool, purpose and key usage (commands in code blocks). For a principle, statement, rationale and application. Skip any section that would have no real content, rather than padding it.
- **`## Sources`**: always the last section, one bullet per contributing source note. Each bullet is a full-path wikilink with readable display text, plus the source type. Every source folder contains a file called `Notes.md`, so a bare `[[Notes]]` would be ambiguous. Take the display text from the source note's title or frontmatter if it has one; otherwise turn the folder name into readable words.

### Keeping it crisp

The knowledge graph is a reference, not a reading log. It's meant to be skimmed in ten seconds when you need it.

- **State facts about the concept, not about the source.** Write "Tokens must be validated server-side for `exp`", not "The course explains that tokens should be validated". Attribution lives in `## Sources`.
- **Merge, don't append.** When a second source covers an existing concept, add only what's new and rewrite the surrounding text so the note reads as one coherent piece. Never add a "From <source>" or "Update" section. If the source adds nothing new, still add it to `## Sources`: it covers the concept, and the user wants to trace concepts back to every source that taught them.
- **One home per fact.** Each fact lives in the most specific note it belongs to, and broader notes link to it instead of restating it. An API Security hub says "enforce [[Rate Limiting]]". The details of rate-limiting algorithms live in the Rate Limiting note.
- **Bullets over paragraphs. No intros, recaps or "in summary".**
- **Keep specifics verbatim**: commands, payloads, header names, CVE IDs, numbers. Put code and commands in fenced blocks.
- **Disagreements**: if sources contradict each other, say so briefly and attribute each side ("Source A recommends X; [[...]] argues Y because Z"). This is the one place a source belongs in the body.
- **Stay grounded in the sources.** A short clarifying clause to connect ideas is fine. Substantial content that no source supports misrepresents what the `## Sources` list vouches for, so leave it out and mention the gap in the report instead.
- Offensive techniques go alongside their detection and mitigation where the sources cover them (see CLAUDE.md).

### Handling edits, deletions and renames

- **Modified source**: integrate additions as above. If the user removed or corrected something, update the knowledge it fed into, unless another cited source still supports the old version.
- **Deleted source**: remove its `## Sources` bullet everywhere. In notes that still have other sources, remove only content that clearly came from the deleted source alone (`git show` the old version and compare with the remaining sources). If a note has no sources left, delete it, and replace every `[[link]]` to it with plain text or a link to a better note. Git keeps the history, so deleting is recoverable.
- **Renamed or moved source**: rewrite the citation path in every note that cites it. Use `grep -rl` on the old path, without `.md`.

## 5. Maintain the links

Links are what make this a graph rather than a pile of notes.

- **Link inline, at the first mention** of another concept that has a note. Don't add a separate "Related" list for things the text already links. Use `## Related` only for genuinely related notes the prose doesn't mention.
- **Backfill links to new notes.** Once a note is created, grep `knowledge/` for plain-text mentions of its name and aliases, and link the first mention in each note. Otherwise older notes never point to the new one.
- **No dangling links.** Link only to notes that exist (or that you create in this run). A link to a missing note is a promise nobody keeps.
- **Renaming a knowledge note** (e.g. to its canonical name): update every link that points to it.
- **Hubs**: broad domains (`API Security`, `Linux Privilege Escalation`, `OWASP Top 10`) get a hub note. A hub opens with a 1–3 sentence definition and then lists its member concepts in grouped bullets, each with a one-line orientation (`- [[Rate Limiting]]: throttling clients to stop brute force and resource exhaustion`). Hubs are concept notes too: they can link to other hubs, and they carry `## Sources` for their own text. Every concept note should be reachable from at least one hub.
- **`knowledge/Index.md`** is the entry point: a short list of hubs, each with a one-line orientation. Create it on the first sync and add new hubs to it.

## 6. Validate

```bash
python3 .claude/skills/sync-knowledge/scripts/check_links.py . --subtree knowledge
```

Fix every broken link and run it again until it passes. Then check orphans: every concept note except `Index.md` should have inbound links (at least from a hub). Also check that every note in `knowledge/` ends with a `## Sources` section containing at least one link that resolves to a source note. `Index.md` is the exception.

## 7. Commit the sync point

Write a short commit body to a temporary file (in the scratchpad or `$TMPDIR`, not inside the vault), then run:

```bash
bash .claude/skills/sync-knowledge/scripts/commit_sync.sh /path/to/body.txt
```

The script stages and commits only `courses/`, `videos/`, `articles/` and `knowledge/`, with the subject `knowledge: sync`. The next run uses that subject to find its starting point, so don't commit sync results any other way. Anything else the user has modified, such as `.obsidian/`, is left alone. Don't push.

Body format:

```
Sources:
  A courses/pluralsight/api-security-best-practices/Notes.md
  M articles/jwt-pitfalls/Notes.md

Knowledge:
  + Rate Limiting
  ~ JSON Web Token
  - JWT None Algorithm Attack
```

(`+` created, `~` updated, `-` deleted.)

## 8. Report

Tell the user, briefly:

- Which source notes were processed. Name any that were skipped (empty) and why.
- Which concept notes were created, updated and deleted, and which hubs changed.
- Anything worth their attention: contradictions between sources, a thin concept kept as a bullet that could become its own note, gaps you noticed but didn't fill, and anything you added that the sources don't directly state.
- The commit hash.
