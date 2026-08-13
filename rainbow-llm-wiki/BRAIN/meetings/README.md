# Meetings (`meetings/`) — Directory Resolver

> **Primary Home for:** Records, analyses, decisions, action items, and transcripts of specific meetings or calls.

---

## 1. What Goes Here
- Meeting notes, customer interview transcripts, 1:1 call notes, board syncs.
- Slug convention: `YYYY-MM-DD-topic-or-participants.md`

## 2. What Does NOT Go Here
- General bios of participants $\rightarrow$ [`people/`](../people/README.md) (enrich people pages using insights from the meeting).
- Broad company profiles $\rightarrow$ [`companies/`](../companies/README.md)

---

## 3. Meeting Page Template

```markdown
---
type: meeting
id: YYYY-MM-DD-meeting-title
title: Meeting Title
date: "YYYY-MM-DD"
participants:
  - "people/participant-1"
  - "people/participant-2"
tags: [tag1, tag2]
updated_at: "YYYY-MM-DD"
---

# Meeting Title

> Executive summary: High-level distillation of the meeting outcome and strategic significance.

## Attendees
- [Participant 1](../people/participant-1.md)
- [Participant 2](../people/participant-2.md)

## Key Decisions Made
1. Decision 1
2. Decision 2

## Action Items & Owners
- [ ] Task 1 — Owner: [Participant 1](../people/participant-1.md)
- [ ] Task 2 — Owner: [Participant 2](../people/participant-2.md)

## Strategic Takeaways
- Synthesis of what was communicated and what was unsaid.

---

## Full Transcript / Raw Notes
```
[Paste transcript or raw timestamped notes here]
```
```
