---
name: rainbowllmwiki-maintain
version: 1.0.0
description: |
  Knowledge base health, linting, dead link detection, and orphan audit protocol for BRAIN/.
triggers:
  - "maintain"
  - "lint"
  - "audit health"
  - "fix broken links"
  - "prune inbox"
mutating: true
---

# Knowledge Base Health & Maintenance Protocol

Regular maintenance procedures to ensure the `BRAIN/` knowledge base stays clean, consistent, and error-free.

---

## 1. Automated Health Audit Checklist

Run the validation suite:
```bash
bun run lint
bun run stats
```

The linter verifies:
1. **Frontmatter Integrity**: All files have valid YAML frontmatter with mandatory fields (`type`, `id`, `title`, `updated_at`).
2. **Broken Internal Links**: Detects broken relative markdown links (`[Target](../category/file.md)`).
3. **Duplicate Aliases**: Identifies colliding alias strings across multiple entities.
4. **Two-Layer Compliance**: Confirms the presence of `---` page layer divider.

---

## 2. Manual Maintenance Tasks

- **Empty Inbox**: Review `BRAIN/inbox/` files, walk `BRAIN/RESOLVER.md`, and refile them into permanent directories.
- **Prune Open Threads**: Check `Open Threads` sections across active pages; move resolved items to the `## Timeline` section.
- **Orphan Page Linking**: Identify pages with zero incoming backlinks and link them to their relevant parent projects, companies, or concepts.
