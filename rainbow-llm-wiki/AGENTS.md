# AGENTS.md — Master Agent Operating Protocol

> **Core Purpose:** This file governs how all autonomous AI agents (Cursor, Codex, Gemini CLI, Claude Code, Aider, OpenClaw, Hermes) read, write, enrich, and maintain this 100% local, zero-database Markdown knowledge base.

---

## 1. System Overview & Directory Structure
This repository implements an LLM-maintained, interlinked wiki organized along MECE (Mutually Exclusive, Collectively Exhaustive) principles. All knowledge base files are isolated inside the `BRAIN/` directory to cleanly separate data/content from repository root scripts and agent skill definitions.

```text
.
├── AGENTS.md            — Operational instructions for all AI agents (this file)
├── INSTALL_FOR_AGENTS.md— Detailed installation and setup instructions
├── package.json         — Convenience script runners (bun)
├── skills/              — Agent skill SOPs
│   ├── RESOLVER.md              — Master Dispatcher / Skill router
│   ├── rainbowllmwiki-enrich/   — 7-step tiered entity enrichment protocol
│   ├── rainbowllmwiki-ingest/   — Ingestion protocol for meetings, notes, articles
│   ├── rainbowllmwiki-query/    — Retrieval and backlink traversal protocol
│   ├── rainbowllmwiki-maintain/ — Knowledge base health, linting, and audit protocol
│   └── rainbowllmwiki-dedup-merge/ — Alias search and entity merge protocol
└── BRAIN/               — The Knowledge Base root folder
    ├── .scripts/        — Zero-dependency validation and indexing utilities
    ├── RESOLVER.md      — Master decision tree for routing notes and entities
    ├── schema.md        — Page formatting schemas, frontmatter specs, epistemic rules
    ├── index.md         — Catalog of all entities grouped by category
    ├── log.md           — Append-only chronological record of ingests and updates
    ├── graph.md         — Auto-generated relationship graph (Mermaid)
    ├── aliases.json     — Fast-lookup map of all canonical slugs and aliases
    └── [Domain Dirs]    — people/, companies/, projects/, meetings/, etc.
```

---

## 2. Core Invariants & Golden Rules (Inviolable)
1. **Execution Plane vs. Data Plane**: Agent tools/skills live in `$WORKSPACE_ROOT/skills/`. All knowledge files live in `BRAIN/`. Never create raw entity files in the root folder, and never put skills inside the brain.
2. **Mandatory Resolver Consultation**: Always read `BRAIN/RESOLVER.md` before creating or moving any file. Never guess directory placement.
3. **Strict Two-Layer Separation**: Maintain the horizontal rule `---` dividing mutable compiled truth (above) and the append-only timeline (below).
4. **Search Before Write (Deduplication Guard)**: Before creating a person or company page, scan `aliases` across all files or check `BRAIN/aliases.json` to eliminate split-brain duplicates. Execute the Update/Enrich workflow if a match exists.
5. **Universal Base Schema**: All entity files must include `type`, `id`, `title`, `aliases`, `status`, `tags`, `relations`, and `updated_at`.
6. **Epistemic Discipline**: Always tag contextual/subjective claims with `observed`, `self-described`, or `inferred`, accompanied by source and confidence level as defined in `BRAIN/schema.md`.
7. **Primacy of User Corrections**: If the user corrects a fact or assessment, update the compiled truth immediately, add a timeline entry, and set confidence to `high`.
8. **Continuous Enrichment**: Enrich entities upon encountering any signal rather than deferring to batch jobs.
9. **No Unprompted Git Commits**: Do not execute `git commit` or stage changes unless explicitly instructed by the user.

---

## 3. Universal Base Frontmatter Contract
Every entity file in `BRAIN/` inherits:
```yaml
---
type: "<domain_singular>"   # e.g., person, company, school, project, concept, idea, meeting, event
id: "<canonical-slug>"      # matches filename without .md (kebab-case)
title: "<Human Readable Title>"
aliases: ["<Variant 1>", "<Variant 2>"]
status: active              # active | draft | in-progress | on-hold | closed | archived
tags: ["tag1", "tag2"]
relations:
  - target: "<directory>/<target-slug>"
    type: "<relationship-type>"
updated_at: "YYYY-MM-DD"
---
```

---

## 4. Standard Operating Procedures (SOPs)
For detailed step-by-step instructions on specific tasks, read the corresponding skill in `skills/`:

| Task / Trigger | Protocol Reference |
|---|---|
| Ingest meeting, email, article, or quick note | [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md) |
| Enrich a person or company with new context | [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md) |
| Search, retrieve, or query relationships | [`skills/rainbowllmwiki-query/SKILL.md`](skills/rainbowllmwiki-query/SKILL.md) |
| Merge duplicate entities and fix backlinks | [`skills/rainbowllmwiki-dedup-merge/SKILL.md`](skills/rainbowllmwiki-dedup-merge/SKILL.md) |
| Routine brain health, linting, and audit | [`skills/rainbowllmwiki-maintain/SKILL.md`](skills/rainbowllmwiki-maintain/SKILL.md) |

---

## 5. Pre-Flight Checklist & Tooling Commands
Before finalizing any changes to the knowledge base, run the appropriate validation scripts from `$WORKSPACE_ROOT`:
- **Version Check**: `bun run version` (verify update status against upstream).
- **Validation**: `bun run lint` (ensure frontmatter validity, `.version` integrity, and verify no broken internal links exist).
- **Indexing**: `bun run index` (refresh `BRAIN/index.md` and `BRAIN/aliases.json` if new entities were added).
- **Relationship Graph**: `bun run graph` (re-generate relationship graph and backlink matrix).
- **Health/Stats**: `bun run stats` (inspect knowledge base size and link density metrics).
- **Logging**: Always append a brief summary of what was ingested or updated to [`BRAIN/log.md`](BRAIN/log.md).
