# Concepts (`concepts/`) — Directory Resolver

> **Primary Home for:** Mental models, reusable frameworks, design patterns, and teachable principles.

---

## 1. What Goes Here
- Universal principles, frameworks, cognitive models (e.g. MECE, First Principles, Raft Consensus).
- Slug convention: `concept-name.md`

## 2. What Does NOT Go Here
- Things you could build as code $\rightarrow$ [`ideas/`](../ideas/README.md)
- Long essays or narrative prose $\rightarrow$ [`writing/`](../writing/README.md)

---

## 3. Concept Page Template

```markdown
---
type: concept
id: concept-slug
title: Concept Name
aliases: ["Alternate Name"]
domain: Knowledge Architecture
tags: [mental-model, taxonomy]
updated_at: "YYYY-MM-DD"
---

# Concept Name

> Executive summary: Core definition and why this mental model is useful.

## Definition & Core Rules
- Exact mechanics and invariants that define this concept.

## Examples & Applications
- Concrete examples of where and how to apply this framework.

## Common Pitfalls
- Anti-patterns or misapplications to avoid.

## See Also
- [Related Concept](../concepts/related-concept.md)

---

## Timeline
- **YYYY-MM-DD** | [Origin / Reference] — Documented framework.
```
