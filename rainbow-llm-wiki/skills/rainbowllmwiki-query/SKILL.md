---
name: rainbowllmwiki-query
version: 1.0.0
description: |
  Search, retrieval, and knowledge synthesis protocol across pure local Markdown files in BRAIN/.
triggers:
  - "query"
  - "search"
  - "what do we know about"
  - "who is"
  - "find connections"
mutating: false
---

# Pure-Markdown Query & Retrieval Protocol

How to answer complex user questions and trace entity relationships without an external database.

---

## 1. Search Strategies

1. **Exact & Alias Lookup**:
   - Check `BRAIN/aliases.json` or `BRAIN/index.md` first for canonical filenames.
   - Example: To find information on "Jenny G. Shao", locate the alias mapping to `people/jenny-shao.md`.
2. **Direct Keyword & Regex Search**:
   - Grep across frontmatter tags, roles, and titles across the relevant MECE directory in `BRAIN/`.
3. **Backlink Traversal (Relationship Exploration)**:
   - Run `bun run graph` or inspect `BRAIN/graph.md` and the `See Also` / `relations` frontmatter fields to trace connections (e.g. Person $\to$ Company $\to$ Deals).
4. **Deep Semantic Synthesis**:
   - Read the Compiled Truth (above the line) of all relevant pages.
   - Combine disparate threads into a coherent executive briefing.

---

## 2. Response Standards

When answering queries about people, companies, or projects:
- Cite specific files using relative Markdown links: `[Ada Lovelace](BRAIN/people/ada-lovelace.md)`.
- Distinguish between current state (compiled truth) and historical background (timeline evidence).
- Highlight any active `Open Threads`.
