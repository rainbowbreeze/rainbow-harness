# CLAUDE.md — Operating Guidelines for Claude Code

## System Overview
This repository contains a 100% local, zero-database knowledge base organized along MECE principles and maintained via two-layer Markdown files located in `BRAIN/`.

## Invariant Rules
1. All knowledge base notes and entities live in `BRAIN/`.
2. Consult [`BRAIN/RESOLVER.md`](BRAIN/RESOLVER.md) before creating or moving any entity.
3. Maintain two-layer page structure: Compiled Truth above `---`, Timeline below `---`.
4. Check `aliases` across files before creating new people or company entities.
5. Adhere to epistemic standards (`observed`, `self-described`, `inferred`) with source citations in [`BRAIN/schema.md`](BRAIN/schema.md).
6. Never run `git commit` or stage changes unless explicitly instructed by the user.

## Common Agent Commands
- Lint and check link integrity: `bun run lint` (or `node BRAIN/.scripts/lint.js`)
- Rebuild index and alias catalog: `bun run index` (or `node BRAIN/.scripts/index.js`)
- Generate relationship graph: `bun run graph` (or `node BRAIN/.scripts/graph.js`)
- View knowledge base health and statistics: `bun run stats` (or `node BRAIN/.scripts/stats.js`)

## Skills Reference
- Master Dispatcher: [`skills/RESOLVER.md`](skills/RESOLVER.md)
- Ingestion: [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md)
- Tiered Enrichment: [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md)
- Query & Backlinks: [`skills/rainbowllmwiki-query/SKILL.md`](skills/rainbowllmwiki-query/SKILL.md)
- Deduplication & Merging: [`skills/rainbowllmwiki-dedup-merge/SKILL.md`](skills/rainbowllmwiki-dedup-merge/SKILL.md)
- Health & Maintenance: [`skills/rainbowllmwiki-maintain/SKILL.md`](skills/rainbowllmwiki-maintain/SKILL.md)
