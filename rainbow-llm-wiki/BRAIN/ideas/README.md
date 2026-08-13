# Ideas (`ideas/`) — Directory Resolver

> **Primary Home for:** Raw possibilities and product concepts that could be built, but have no active development.

---

## 1. What Goes Here
- Product features, startup hypotheses, technical experiments not yet started.
- Slug convention: `idea-name.md`

## 2. What Does NOT Go Here
- Active builds $\rightarrow$ [`projects/`](../projects/README.md) (Graduation: move file to `projects/` when work starts).
- General mental frameworks $\rightarrow$ [`concepts/`](../concepts/README.md)

---

## 3. Idea Page Template

```markdown
---
type: idea
id: idea-slug
title: Idea Title
status: raw # raw | evaluating | validated | discarded | graduated
target_domain: Developer Tools
tags: [tag1, tag2]
updated_at: "YYYY-MM-DD"
---

# Idea Title

> Executive summary: Core concept, user problem solved, and hypothesis.

## Concept & Mechanics
- Detailed breakdown of how the product or feature would work.

## Validation Signals
- Market demand signals, competing tools, or user interest.

## Open Questions
- Key unknowns or risks to test before building.

---

## Timeline
- **YYYY-MM-DD** | [Inception] — Idea captured.
```
