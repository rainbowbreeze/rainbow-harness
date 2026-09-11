---
name: rainbowllmwiki-query
description: Search, retrieval, and synthesis protocol across pure Markdown files in ${BRAIN_PATH}/
version: 1.2.0
author: Rainbowbreeze
metadata:
  hermes:
    category: rainbowskills
    tags: [wiki, llm-wiki, query, search, retrieval]
required_environment_variables:
  - name: BRAIN_PATH
    prompt: Where can I store the wiki files?
    help: Path to store the wiki files
    required_for: full functionality
---

# Pure-Markdown Query & Retrieval Protocol

How to answer complex user questions and trace entity relationships without an external database.

---

## 1. Search Strategies

1. **Exact & Alias Lookup**:
   - Check `${BRAIN_PATH}/aliases.json` or `${BRAIN_PATH}/index.md` first for canonical filenames.
   - Example: To find information on "Jenny G. Shao", locate the alias mapping to `people/jenny-shao.md`.
2. **Direct Keyword & Regex Search**:
   - Grep across frontmatter tags, roles, and titles across the relevant MECE directory in `${BRAIN_PATH}/`.
3. **Backlink Traversal (Relationship Exploration)**:
   - Run `bun run graph` or inspect `${BRAIN_PATH}/graph.md` and the `See Also` / `relations` frontmatter fields to trace connections (e.g. Person $\to$ Company $\to$ Deals).
4. **Deep Semantic Synthesis**:
   - Read the Compiled Truth (above the line) of all relevant pages.
   - Combine disparate threads into a coherent executive briefing.

---

## 2. Response Standards

When answering queries about people, companies, or projects:
- Cite specific files using relative Markdown links: `[Ada Lovelace](${BRAIN_PATH}/people/ada-lovelace.md)`.
- Distinguish between current state (compiled truth) and historical background (timeline evidence).
- Highlight any active `Open Threads`.
