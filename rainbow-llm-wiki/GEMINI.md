# GEMINI.md — Project Memory & Operational Guide

## Overview
This repository contains a 100% local, zero-database personal intelligence and knowledge management system inspired by [gbrain](https://github.com/garrytan/gbrain).

All knowledge base files and folders are isolated inside the `BRAIN/` directory to cleanly separate data/content from repository root scripts and agent skill definitions.

It implements an LLM-maintained, interlinked wiki structured around:
1. **MECE Categorical Directories**: Every piece of knowledge has exactly one home inside `BRAIN/`.
2. **Two-Layer Pages**: Compiled Truth (synthesis) above `---`, Timeline (immutable evidence) below `---`.
3. **Epistemic Discipline**: Explicit labeling of claim types (`observed`, `self-described`, `inferred`) and confidence tracking.
4. **Tool-Agnostic Agent Skills**: Standard Operating Procedures guiding autonomous knowledge capture, enrichment, and maintenance (`skills/`).
5. **Zero External DB Dependencies**: Powered entirely by Markdown files, YAML frontmatter, and lightweight Node/Bun validation scripts (`scripts/`).

---

## Core Invariants & Rules
- **Rule 1 (MECE Filing)**: Every entity or note belongs to exactly one primary directory inside `BRAIN/` determined by `BRAIN/RESOLVER.md`.
- **Rule 2 (Mandatory Resolver Consultation)**: Always read `BRAIN/RESOLVER.md` before creating or moving any file.
- **Rule 3 (Two-Layer Separation)**: Above `---` is mutable compiled truth; below `---` is immutable evidence log.
- **Rule 4 (Epistemic Discipline)**: Subjective context claims must specify source type, citation date, and confidence level.
- **Rule 5 (User Correction Primacy)**: User feedback immediately overrides previous inferences with highest priority.
- **Rule 6 (Slug Stability & Alias Search)**: Search `aliases` across all files prior to page creation to eliminate split-brain duplicates.
- **Rule 7 (Continuous Enrichment)**: Enrich entities upon encountering any signal rather than deferring to batch jobs.
- **Rule 8 (No Unprompted Git Commits)**: Never stage or commit changes unless explicitly instructed by the user.

---

## Directory Structure
```
.
├── GEMINI.md            — Project memory & operational guide (this file)
├── INSTALL_FOR_AGENTS.md— Detailed installation and setup instructions for AI agents
├── AGENTS.md            — Operational instructions for general AI agents
├── CLAUDE.md            — Operational guidelines for Claude Code
├── package.json         — Convenience script runners (bun/node)
├── skills/              — Agent skill SOPs
│   ├── RESOLVER.md      — Skill dispatcher
│   ├── enrich/          — 7-step tiered entity enrichment protocol
│   ├── ingest/          — Ingestion protocol for meetings, notes, articles
│   ├── query/           — Retrieval and backlink traversal protocol
│   ├── maintain/        — Knowledge base health, linting, and audit protocol
│   └── dedup-merge/     — Alias search and entity merge protocol
├── scripts/             — Zero-dependency validation and indexing utilities (targets BRAIN/)
│   ├── lint.js          — Validates frontmatter, broken links, and duplicate aliases
│   ├── index.js         — Rebuilds BRAIN/index.md and BRAIN/aliases.json
│   ├── graph.js         — Extracts relationship graph and backlink matrix
│   └── stats.js         — Reports knowledge base size, link density, and metrics
└── BRAIN/               — The Knowledge Base root folder
    ├── RESOLVER.md      — Master decision tree for routing notes and entities
    ├── schema.md        — Page formatting schemas, frontmatter specs, and epistemic rules
    ├── index.md         — Catalog of all entities grouped by category
    ├── log.md           — Append-only chronological record of ingests and updates
    ├── graph.md         — Auto-generated relationship graph (Mermaid)
    ├── aliases.json     — Fast-lookup map of all canonical slugs and aliases
    ├── people/          — One page per individual (slug: first-last.md)
    │   ├── README.md    — Directory resolver
    │   └── .raw/        — Raw per-person API/contact snapshots
    ├── companies/       — One page per organization (slug: company-name.md)
    │   ├── README.md    — Directory resolver
    │   └── .raw/        — Raw per-company API/filing snapshots
    ├── projects/        — Active projects with specs, repos, or deliverables
    │   └── README.md
    ├── ideas/           — Possibilities not yet in development
    │   └── README.md
    ├── concepts/        — Frameworks, mental models, and reusable knowledge patterns
    │   └── README.md
    ├── meetings/        — Analysis, decisions, and transcripts of meetings
    │   └── README.md
    ├── deals/           — Financial transactions, terms, investments, partnerships
    │   └── README.md
    ├── writing/         — Long-form essays, drafts, articles, philosophy
    │   └── README.md
    ├── sources/         — Bulk raw imports, reference snapshots, archives
    │   └── README.md
    ├── inbox/           — Staging area for unclassified notes
    │   └── README.md
    └── archive/         — Retired or superseded entities
        └── README.md
```

---

## Tooling & Maintenance Commands
- `bun run lint` (or `node scripts/lint.js`): Run full schema and link integrity validation in `BRAIN/`.
- `bun run index` (or `node scripts/index.js`): Rebuild `BRAIN/index.md` catalog and `BRAIN/aliases.json`.
- `bun run graph` (or `node scripts/graph.js`): Re-generate relationship graph and backlink counts.
- `bun run stats` (or `node scripts/stats.js`): Inspect knowledge base metrics and health.
