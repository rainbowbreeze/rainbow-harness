---
name: ingest
version: 1.0.0
description: |
  Ingest protocol for capturing notes, meeting transcripts, articles, and raw data
  into appropriate MECE directories inside BRAIN/ or temporary inbox staging.
triggers:
  - "ingest"
  - "capture"
  - "meeting transcript"
  - "save article"
  - "quick note"
mutating: true
writes_to:
  - BRAIN/meetings/
  - BRAIN/inbox/
  - BRAIN/sources/
  - BRAIN/writing/
  - BRAIN/ideas/
---

# Ingestion Protocol

Guidelines for capturing raw inputs and turning them into structured knowledge inside `BRAIN/`.

---

## 1. Routing Input Sources

When receiving new content:

1. **Meeting Transcripts**:
   - Save full transcript and synthesis into `BRAIN/meetings/YYYY-MM-DD-title.md`.
   - Extract action items and decisions.
   - Trigger `skills/enrich/SKILL.md` for all meeting attendees.
2. **Quick Notes & Fleeting Thoughts**:
   - Walk `BRAIN/RESOLVER.md`. If destination is unambiguous (e.g. idea `BRAIN/ideas/`, mental model `BRAIN/concepts/`), write directly to destination.
   - If ambiguous write to `BRAIN/inbox/slug.md`.
3. **Articles & Web Research**:
   - Extract core concepts into `BRAIN/concepts/` or ideas into `BRAIN/ideas/`.
   - Store raw reference snapshot in `BRAIN/sources/` if large/immutable.
4. **Per-Entity Raw Dumps**:
   - Store per-person or per-company API dumps in `BRAIN/people/.raw/` or `BRAIN/companies/.raw/`.

---

## 2. Ingest Checklist

- [ ] Check `BRAIN/RESOLVER.md` for proper target directory.
- [ ] Ensure valid YAML frontmatter is included.
- [ ] Establish Two-Layer structure: Compiled synthesis on top, raw transcript/source excerpt below `---`.
- [ ] Trigger reciprocal cross-links on referenced entities.
- [ ] Log entry in `BRAIN/log.md`.
