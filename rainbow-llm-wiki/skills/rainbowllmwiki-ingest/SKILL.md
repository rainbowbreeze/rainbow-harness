---
name: rainbowllmwiki-ingest
version: 1.0.0
description: Ingestion protocol for capturing notes, meetings, articles, and raw data into BRAIN/
metadata:
  hermes:
    category: rainbowskills
    tags: [wiki, llm-wiki, ingest, capture]
---

# Ingestion Protocol

Guidelines for capturing raw inputs and turning them into structured knowledge inside `BRAIN/`.

---

## 1. Routing Input Sources

When receiving new content:

1. **Meeting Transcripts & Calendar Invites**:
   - Save full transcript and synthesis into `BRAIN/meetings/YYYY-MM-DD-title.md`.
   - Extract action items and decisions.
   - Extract attendee metadata (all email addresses, phone numbers, affiliations, roles).
   - Trigger `skills/rainbowllmwiki-enrich/SKILL.md` for all meeting attendees to enrich their profiles and contact info.
2. **Emails, Messages & Contact Notes**:
   - Extract sender and recipient email addresses, phone numbers, titles, and company affiliations.
   - Trigger `skills/rainbowllmwiki-enrich/SKILL.md` for all involved people.
3. **Quick Notes & Fleeting Thoughts**:
   - Walk `BRAIN/RESOLVER.md`. If destination is unambiguous (e.g. idea `BRAIN/ideas/`, mental model `BRAIN/concepts/`), write directly to destination.
   - If ambiguous write to `BRAIN/inbox/slug.md`.
4. **Articles & Web Research**:
   - Extract core concepts into `BRAIN/concepts/` or ideas into `BRAIN/ideas/`.
   - Store raw reference snapshot in `BRAIN/sources/` if large/immutable.
5. **Per-Entity Raw Dumps (vCards, API dumps, CSVs)**:
   - Store per-person or per-company raw files in `BRAIN/people/.raw/` or `BRAIN/companies/.raw/`.
   - Trigger `skills/rainbowllmwiki-enrich/SKILL.md` to parse all emails, phones, and social links into structured dossiers.
6. **Conferences, Summits & Events**:
   - Save event overview, agenda highlights, connections made, and takeaways into `BRAIN/events/YYYY-MM-DD-event-name.md`.
   - Trigger `skills/rainbowllmwiki-enrich/SKILL.md` for speakers, organizers, and contacts met (capturing business cards, emails, phone numbers).

---

## 2. Ingest Checklist

- [ ] Check `BRAIN/RESOLVER.md` for proper target directory.
- [ ] Ensure valid YAML frontmatter is included.
- [ ] Establish Two-Layer structure: Compiled synthesis on top, raw transcript/source excerpt below `---`.
- [ ] Extract all personal/contact details (multiple emails, phone numbers, handles) for person entities.
- [ ] Trigger reciprocal cross-links on referenced entities.
- [ ] Log entry in `BRAIN/log.md`.

