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
- Lint and check link integrity: `bun run lint` (or `node scripts/lint.js`)
- Rebuild index and alias catalog: `bun run index` (or `node scripts/index.js`)
- Generate relationship graph: `bun run graph` (or `node scripts/graph.js`)
- View knowledge base health and statistics: `bun run stats` (or `node scripts/stats.js`)

## Skills Reference
- Master Dispatcher: [`skills/RESOLVER.md`](skills/RESOLVER.md)
- Ingestion: [`skills/ingest/SKILL.md`](skills/ingest/SKILL.md)
- Tiered Enrichment: [`skills/enrich/SKILL.md`](skills/enrich/SKILL.md)
- Query & Backlinks: [`skills/query/SKILL.md`](skills/query/SKILL.md)
- Deduplication & Merging: [`skills/dedup-merge/SKILL.md`](skills/dedup-merge/SKILL.md)
- Health & Maintenance: [`skills/maintain/SKILL.md`](skills/maintain/SKILL.md)
