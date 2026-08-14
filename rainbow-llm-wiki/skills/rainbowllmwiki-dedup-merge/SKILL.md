---
name: rainbowllmwiki-dedup-merge
version: 1.0.0
description: Protocol for resolving split-brain duplicate entities and merging timelines in BRAIN/
metadata:
  hermes:
    category: rainbowskills
    tags: [wiki, llm-wiki, deduplication, merge]
---

# Entity Deduplication & Merge Protocol

When two separate files exist for the same entity in `BRAIN/` (e.g. `j-smith.md` and `john-smith.md`), execute this exact protocol.

---

## 1. Step-by-Step Merge Procedure

1. **Select Survivor**: Choose the more complete file with the canonical slug as the survivor.
2. **Merge Aliases**: Add the duplicate's filename and aliases into the survivor's `aliases:` array in frontmatter.
3. **Consolidate Compiled Truth**: Merge unique context, beliefs, and state fields into the survivor.
4. **Merge Timelines**: Copy all timeline entries from the duplicate into the survivor, ordering by date descending.
5. **Update Inbound Links**: Search `BRAIN/` for links pointing to the duplicate file and rewrite them to point to the survivor.
6. **Move Duplicate to Archive (or Delete)**: Move the duplicate to `BRAIN/archive/` or delete it if completely absorbed.
7. **Rebuild Index & Log**:
   ```bash
   bun run index
   bun run lint
   ```
   Append a merge record to `BRAIN/log.md`:
   `- **MERGE** | Merged duplicate.md into survivor.md`
