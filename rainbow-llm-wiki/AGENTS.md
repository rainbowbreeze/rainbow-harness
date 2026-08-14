# AGENTS.md — Agent Operating Protocol

> **Core Purpose:** This file governs how all autonomous AI agents (Cursor, Codex, Gemini CLI, Claude Code, Aider, OpenClaw, Hermes) read, write, enrich, and maintain this pure Markdown knowledge base located in `BRAIN/`.

---

## 1. Golden Rules (Inviolable)

1. **All Knowledge Base Content Lives in `BRAIN/`**:
   Never create raw entity files in the root folder. All entities, resolvers, schemas, logs, and indexes reside inside [`BRAIN/`](BRAIN/).
2. **Always Read [`BRAIN/RESOLVER.md`](BRAIN/RESOLVER.md) First**:
   Before creating or moving any file, walk the decision tree in `BRAIN/RESOLVER.md`. Never guess directory placement.
3. **Search Before Write (Deduplication Gate)**:
   Before creating a person or company page, scan `aliases` across all existing files or check `BRAIN/index.md`/`BRAIN/aliases.json`. If a match exists, execute the **Update / Enrich** workflow instead of creating a new file.
4. **Strict Two-Layer Separation**:
   Maintain the horizontal rule `---` dividing compiled truth (above) and the append-only timeline (below).
5. **Epistemic Labeling**:
   Always tag contextual claims with `observed`, `self-described`, or `inferred`, accompanied by source and confidence level as defined in [`BRAIN/schema.md`](BRAIN/schema.md).
6. **Primacy of User Corrections**:
   If the user corrects a fact or assessment, update the compiled truth immediately, add a timeline entry, and set confidence to `high`.
7. **No Unrequested Git Commits**:
   Do not execute `git commit` or `git push` unless explicitly asked by the operator.

---

## 2. Standard Operating Procedures (SOPs)

For detailed step-by-step instructions on specific tasks, read the corresponding skill in `skills/`:

| Task / Trigger | Protocol Reference |
|---|---|
| Ingest meeting, email, article, or quick note | [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md) |
| Enrich a person or company with new context | [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md) |
| Search, retrieve, or query relationships | [`skills/rainbowllmwiki-query/SKILL.md`](skills/rainbowllmwiki-query/SKILL.md) |
| Merge duplicate entities and fix backlinks | [`skills/rainbowllmwiki-dedup-merge/SKILL.md`](skills/rainbowllmwiki-dedup-merge/SKILL.md) |
| Routine brain health, linting, and audit | [`skills/rainbowllmwiki-maintain/SKILL.md`](skills/rainbowllmwiki-maintain/SKILL.md) |

---

## 3. Pre-Flight Checklist for Agent Modifications

Before finalizing any changes to the knowledge base:
- [ ] Run `bun run lint` (or `node BRAIN/.scripts/lint.js`) to ensure frontmatter validity and verify no broken internal links exist.
- [ ] If new entities were added, run `bun run index` (or `node BRAIN/.scripts/index.js`) to refresh `BRAIN/index.md` and `BRAIN/aliases.json`.
- [ ] Append a brief summary of what was ingested or updated to [`BRAIN/log.md`](BRAIN/log.md).
