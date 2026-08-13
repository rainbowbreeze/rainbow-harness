# Companies (`companies/`) — Directory Resolver

> **Primary Home for:** Companies, startups, VC funds, non-profits, and institutions.

---

## 1. What Goes Here
- Any corporate or institutional organization.
- Slug convention: `company-name.md` (lowercase, hyphens for spaces).

## 2. What Does NOT Go Here
- Human founders or executives $\rightarrow$ [`people/`](../people/README.md)
- Specific financial deals or rounds $\rightarrow$ [`deals/`](../deals/README.md)
- Internal software projects $\rightarrow$ [`projects/`](../projects/README.md)

---

## 3. Company Page Template

```markdown
---
type: company
id: company-slug
title: Company Name
aliases: ["Alternate Name", "domain.com"]
stage: Series A
industry: Developer Tools
website: "https://example.com"
status: active
tags: [tag1, tag2]
relations:
  - target: "people/founder-slug"
    type: "founder"
updated_at: "YYYY-MM-DD"
---

# Company Name

> Executive summary: What the company does, its core differentiator, and market position.

## State
- **What:** One-line description
- **Stage:** Seed / Series A / Growth / Public
- **Key People:** [Founder Name](../people/founder-slug.md)
- **Key Metrics:** Revenue, team size, valuation/funding

## What They're Building
- Core product features, architectural choices, and roadmaps.

## Open Threads
- Pending partnerships, inquiries, or follow-ups

## See Also
- [Founder Name](../people/founder-slug.md)

---

## Timeline
- **YYYY-MM-DD** | [Source Type: Source Name] — Event summary.
```
