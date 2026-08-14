# Skills Resolver — Dispatcher for Agent Operations

> **Purpose:** Maps user queries, background events, and triggers to specific Standard Operating Procedures (`SKILL.md`).
> Read the indicated skill file before executing an operation.

---

## Skill Dispatch Table

| Intent / Trigger Phrases | Target Skill | Primary Purpose |
|---|---|---|
| "enrich", "who is", "update company", "new person", "research contact", "dossier" | [`skills/rainbowllmwiki-enrich/SKILL.md`](rainbowllmwiki-enrich/SKILL.md) | 7-step tiered intelligence enrichment for people & companies |
| "ingest", "capture note", "save meeting transcript", "store article", "quick capture", "inbox" | [`skills/rainbowllmwiki-ingest/SKILL.md`](rainbowllmwiki-ingest/SKILL.md) | Capturing and structuring raw inputs into MECE categories |
| "what do we know about", "search", "who is connected to", "find connections", "backlinks" | [`skills/rainbowllmwiki-query/SKILL.md`](rainbowllmwiki-query/SKILL.md) | Multi-file searching, backlink traversal, and synthesis |
| "merge pages", "duplicate person", "combine entities", "same person", "dedup" | [`skills/rainbowllmwiki-dedup-merge/SKILL.md`](rainbowllmwiki-dedup-merge/SKILL.md) | Merging split-brain entity pages and repairing references |
| "lint", "check brain", "broken links", "audit health", "validate frontmatter", "brain stats" | [`skills/rainbowllmwiki-maintain/SKILL.md`](rainbowllmwiki-maintain/SKILL.md) | Knowledge base integrity validation and health maintenance |

---

## Chaining Skills

Skills are designed to chain cleanly:
- **Ingestion Enrichment**: When ingesting a meeting transcript with [`skills/rainbowllmwiki-ingest/SKILL.md`](rainbowllmwiki-ingest/SKILL.md), extract mentioned participants and trigger [`skills/rainbowllmwiki-enrich/SKILL.md`](rainbowllmwiki-enrich/SKILL.md) for any new or thin profiles.
- **Deduplication Maintenance**: After merging duplicate pages with [`skills/rainbowllmwiki-dedup-merge/SKILL.md`](rainbowllmwiki-dedup-merge/SKILL.md), run [`skills/rainbowllmwiki-maintain/SKILL.md`](rainbowllmwiki-maintain/SKILL.md) to verify all backlinks and indexes are clean.
