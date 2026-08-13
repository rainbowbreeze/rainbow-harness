# People (`people/`) — Directory Resolver

> **Primary Home for:** Individual human beings.

---

## 1. What Goes Here
- Any individual person (collaborator, colleague, investor, founder, advisor, friend).
- Slug convention: `first-last.md` (all lowercase, hyphens for spaces).
- Disambiguation: `john-smith-acme.md` if collisions occur.

## 2. What Does NOT Go Here
- Organizations or companies [`companies/`](../companies/README.md)
- Collections of people or teams link individual people to a company or project.

---

## 3. Person Page Template

```markdown
---
type: person
id: first-last
title: First Last
aliases: ["Nickname", "first@example.com", "@handle"]
role: Current Role
company: Current Company
status: active
tags: [tag1, tag2]
relations:
  - target: "companies/company-slug"
    type: "founder"
updated_at: "YYYY-MM-DD"
---

# First Last

> Executive summary: 1-2 sentence core distillation of who they are and why they matter.

## State
- **Role:** Title
- **Company:** [Company Name](../companies/company-slug.md)
- **Relationship:** Collaborator / Investor / Friend
- **Key Context:** 2-3 bullets of essential current context

## What They Believe
- [Belief statement] — observed: [Meeting/Interaction, YYYY-MM-DD], confidence: high
- [Belief statement] — self-described: [Interview/Post, YYYY-MM-DD], confidence: high

## What They're Building
- Summary of current projects and product focus.

## What Motivates Them
- Career arc, ambitions, and core drivers.

## Communication Style
- How they communicate, handle disagreement, and what energizes them.

## Contact & Network
- **Email:** email@example.com
- **Handles:** @handle
- **Close to:** [Related Person](../people/related-person.md)

## Open Threads
- Active follow-ups or pending questions

---

## Timeline
- **YYYY-MM-DD** | [Source Type: Source Name] — Event summary.
```
