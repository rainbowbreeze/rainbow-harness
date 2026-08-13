# Projects (`projects/`) — Directory Resolver

> **Primary Home for:** Active initiatives with repositories, specifications, or assigned owners.

---

## 1. What Goes Here
- Active software projects, open source packages, operational workflows with deliverables.
- Slug convention: `project-name.md`

## 2. What Does NOT Go Here
- Ideas with no active development $\rightarrow$ [`ideas/`](../ideas/README.md)
- Mental models or theory $\rightarrow$ [`concepts/`](../concepts/README.md)

---

## 3. Project Page Template

```markdown
---
type: project
id: project-slug
title: Project Title
aliases: ["short-name"]
status: in-progress # planning | in-progress | on-hold | completed | archived
owner: "people/owner-slug"
repo: "https://github.com/org/repo"
tags: [tag1, tag2]
updated_at: "YYYY-MM-DD"
---

# Project Title

> Executive summary: What is being built, key architecture, and target milestone.

## State
- **Status:** In Progress
- **Lead / Owner:** [Owner Name](../people/owner-slug.md)
- **Repository:** `https://github.com/org/repo`
- **Key Milestones:** Target dates and current sprint goals

## Architecture & Design
- Core technical choices and system design decisions.

## Open Threads
- Current blockers, decisions under review, or next immediate tasks.

## See Also
- [Related Company](../companies/company-slug.md)

---

## Timeline
- **YYYY-MM-DD** | [Commit/Release: vX.Y] — Milestone reached.
```
