---
name: rainbowllmwiki-maintain
version: 1.2.0
description: Knowledge base health, linting, dead link detection, and audit protocol for ${BRAIN_PATH}/
author: Rainbowbreeze
metadata:
  hermes:
    category: rainbowskills
    tags: [wiki, llm-wiki, maintain, lint, audit]
required_environment_variables:
  - name: BRAIN_PATH
    prompt: Where can I store the wiki files?
    help: Path to store the wiki files
    required_for: full functionality
---

# Knowledge Base Health & Maintenance Protocol

Regular maintenance procedures to ensure the `${BRAIN_PATH}/` knowledge base stays clean, consistent, and error-free.

---

## 1. Automated Health Audit Checklist

Run the validation and indexing suite:
```bash
bun ${BRAIN_PATH}/.scripts/lint.mjs
bun ${BRAIN_PATH}/.scripts/index.mjs
bun ${BRAIN_PATH}/.scripts/graph.mjs
bun ${BRAIN_PATH}/.scripts/stats.mjs
```

The linter and indexer verify:
1. **Frontmatter Integrity**: All files have valid YAML frontmatter with mandatory fields (`type`, `id`, `title`, `updated_at`).
2. **Broken Internal Links**: Detects broken relative markdown links (`[Target](../category/file.md)`).
3. **Duplicate Aliases**: Identifies colliding alias strings across multiple entities.
4. **Two-Layer Compliance**: Confirms the presence of `---` page layer divider.

---

## 2. Manual Maintenance Tasks

- **Empty Inbox**: Review `${BRAIN_PATH}/inbox/` files, walk `${BRAIN_PATH}/RESOLVER.md`, and refile them into permanent directories.
- **Prune Open Threads**: Check `Open Threads` sections across active pages; move resolved items to the `## Timeline` section.
- **Orphan Page Linking**: Identify pages with zero incoming backlinks and link them to their relevant parent projects, companies, or concepts.
