# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An Obsidian vault (not a code project) holding personal cybersecurity knowledge: pentesting, Linux, security principles, OWASP, and related topics. There are no build, lint, or test commands. The "output" is Markdown notes that render correctly in Obsidian and fit into the vault's link graph.

## Vault structure

The vault has two layers: **source notes** (what was learned from one specific source) and a **knowledge graph** that synthesizes all of them.

- `courses/` holds notes from courses taken, laid out as `courses/<platform>/<course-slug>/Notes.md` (e.g. `courses/pluralsight/api-security-best-practices/Notes.md`).
- `videos/` holds notes from videos watched.
- `articles/` holds notes from blog posts and web pages.
- `knowledge/` holds the synthesized knowledge graph: atomic, interlinked concept notes plus hub notes, built from everything in the source folders. It is organized by topic, not by source.

Source notes stay faithful to their source. `knowledge/` notes merge what several sources say about one concept. When a source note is added or updated, the usual follow-up is to fold its content into `knowledge/`: extend existing concept notes instead of duplicating them, create new ones where needed, and link each knowledge note back to the source notes it draws on (`[[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]]`). Every source folder has a file named `Notes.md`, so links to them need the full path to be unambiguous.

## Working in the vault

- **Notes are plain Markdown** with Obsidian extensions. Link with wikilinks (`[[Note Name]]`, `[[Note Name#Heading]]`, `[[Note Name|alias]]`), not relative Markdown links, so backlinks and the graph view work. A wikilink to a note that doesn't exist yet is fine: it marks a note to write later.
- **Frontmatter properties** are enabled (core `properties` plugin). Use YAML frontmatter for metadata such as `tags`, `aliases`, and source URLs, so notes can be queried with core **Bases** (`.base` files).
- **In `knowledge/`, prefer small, linked notes** over one large document: one concept, tool, technique, or vulnerability class per note, plus hub/MOC notes that link them together. To break up a long source note or research dump into `knowledge/`, use the `knowledge-graph` skill.
- **Tables**: the Advanced Tables plugin (`table-editor-obsidian`) is installed, so standard GFM pipe tables are the expected format.
- Core `templates` and `daily-notes` are enabled but not configured. Check `.obsidian/templates.json` / `daily-notes.json` before assuming where they live.
- Canvas (`.canvas`) is enabled. The core footnotes plugin is disabled, so footnote syntax won't get editor support.

## Things to avoid

- Don't edit `.obsidian/` (settings, workspace, theme "Obsidian Nord", plugins) unless asked. `workspace.json` changes constantly while Obsidian is open, so ignore it. Obsidian Sync is enabled, so config edits propagate to other devices.
- When renaming or moving a note, update every `[[wikilink]]` that points to it. Obsidian only does this automatically for renames made inside the app.
- Offensive content (exploits, payloads, attack techniques) is reference material for learning and authorized testing. Keep it in that framing, for example by noting prerequisites, detection, and mitigation alongside the technique.
