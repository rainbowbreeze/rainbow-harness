# INSTALL_FOR_AGENTS.md — Installation & Setup Guide for AI Agents

> **Target Audience:** Autonomous AI agents (Hermes, OpenClaw, Claude Code, Cursor, Codex, Gemini CLI, Aider) tasked with initializing or managing a pure local Markdown knowledge base.
> **Design Philosophy:** 100% local, zero-database, zero-cloud-lock-in, Git-native Markdown wiki.

---

## Step 0: Initial Discovery & User Confirmation (DO NOT SKIP)

Before creating any directories or writing files, **ask the operator**:

1. **Brain Location**:
   > *"Where would you like to create your knowledge base? Default is `./BRAIN` inside this project, or `~/brain` for a standalone personal repository."*
2. **Domain Customization**:
   > *"The standard domains are: `people`, `companies`, `projects`, `ideas`, `concepts`, `meetings`, `deals`, `writing`, `sources`, `inbox`, `archive`. Would you like to add any specialized domains (e.g. `personal`, `household`, `civic`, `hiring`)?"*

Once the user confirms the target path (referred to below as `$BRAIN_PATH`), proceed with the steps below.

---

## Step 1: Scaffold Directory Structure

Create the root `$BRAIN_PATH` directory along with all MECE subdirectories and `.raw/` sidecars:

```bash
mkdir -p "$BRAIN_PATH"/{people/.raw,companies/.raw,projects,ideas,concepts,meetings,deals,writing,sources,inbox,archive}
mkdir -p skills/{enrich,ingest,query,maintain,dedup-merge}
mkdir -p scripts
```

Ensure `.gitkeep` files exist in empty directories (especially `.raw/` folders):
```bash
touch "$BRAIN_PATH"/people/.raw/.gitkeep
touch "$BRAIN_PATH"/companies/.raw/.gitkeep
```

---

## Step 2: Install Core Brain Governance Files

Copy or write the core governance files directly into `$BRAIN_PATH/`:

1. **`$BRAIN_PATH/RESOLVER.md`**: Master decision tree for filing entities and notes. Walk this tree before writing any new file.
2. **`$BRAIN_PATH/schema.md`**: Structural specifications, YAML frontmatter schemas for all entity types, Two-Layer rules (Compiled Truth above `---`, Timeline below `---`), and epistemic tags (`observed`, `self-described`, `inferred`).
3. **`$BRAIN_PATH/log.md`**: Append-only event log starting with:
   ```markdown
   # Knowledge Base Event Log
   
   ## YYYY-MM-DD
   - **SYSTEM_INIT** | Knowledge base initialized at $BRAIN_PATH.
   ```
4. **`$BRAIN_PATH/index.md`**: Entity catalog placeholder (auto-generated in Step 6).
5. **`$BRAIN_PATH/aliases.json`**: Alias lookup map `{}` (auto-generated in Step 6).

---

## Step 3: Install Directory Resolvers (`README.md`)

Every subdirectory in `$BRAIN_PATH/` must have a `README.md` defining:
1. **What goes here** (inclusion criteria and slug convention).
2. **What does NOT go here** (disambiguation from neighboring directories).
3. **Page template** with YAML frontmatter, compiled truth sections, and timeline log.

Ensure the following resolver files exist:
- `$BRAIN_PATH/people/README.md` (Slug: `first-last.md`)
- `$BRAIN_PATH/companies/README.md` (Slug: `company-name.md`)
- `$BRAIN_PATH/projects/README.md` (Slug: `project-name.md`)
- `$BRAIN_PATH/ideas/README.md` (Slug: `idea-name.md`)
- `$BRAIN_PATH/concepts/README.md` (Slug: `concept-name.md`)
- `$BRAIN_PATH/meetings/README.md` (Slug: `YYYY-MM-DD-title.md`)
- `$BRAIN_PATH/deals/README.md` (Slug: `company-round-year.md`)
- `$BRAIN_PATH/writing/README.md` (Slug: `topic-title.md`)
- `$BRAIN_PATH/sources/README.md` (Bulk raw imports & snapshots)
- `$BRAIN_PATH/inbox/README.md` (Temporary staging)
- `$BRAIN_PATH/archive/README.md` (Retired entities)

---

## Step 4: Install Agent Skills Layer (`skills/`)

Skills teach autonomous agents how to perform knowledge management tasks consistently.

1. **`skills/RESOLVER.md`**: Master skill dispatcher mapping prompts/triggers to skills.
2. **`skills/enrich/SKILL.md`**: 7-step tiered enrichment protocol for people and companies.
3. **`skills/ingest/SKILL.md`**: Multi-source ingestion protocol for meetings, transcripts, and notes.
4. **`skills/query/SKILL.md`**: Pure Markdown search, alias resolution, and backlink traversal.
5. **`skills/maintain/SKILL.md`**: Health audit, linting, dead link fixing, and inbox pruning protocol.
6. **`skills/dedup-merge/SKILL.md`**: Entity deduplication, timeline merging, and cross-reference updating.

---

## Step 5: Configure Agent Protocol Files

Ensure agent instruction files are installed in the workspace root:

1. **`AGENTS.md`**: Operational rules for Cursor, Hermes, OpenClaw, Codex, Gemini CLI.
2. **`CLAUDE.md`**: Operational guidelines for Claude Code.
3. **`GEMINI.md`**: Project memory and documentation sync file.

### Key Golden Rules to Enforce:
- **Always read `$BRAIN_PATH/RESOLVER.md` before creating any file.**
- **Check `aliases` in existing files before creating a person/company to prevent split-brain duplicates.**
- **Maintain Two-Layer separation (`---`) between Compiled Truth and Timeline.**
- **Tag subjective assertions with epistemic labels (`observed`, `self-described`, `inferred`) and confidence scores.**
- **Do NOT execute `git commit` or `git push` unless explicitly requested by the user.**

---

## Step 6: Install Zero-Dependency Validation & Indexing Scripts

Install the standard Node/Bun automation scripts in `scripts/`:

- **`scripts/lint.js`**: Validates YAML frontmatter, checks for broken relative markdown links, and flags duplicate aliases.
- **`scripts/index.js`**: Rebuilds `$BRAIN_PATH/index.md` and `$BRAIN_PATH/aliases.json` across all files.
- **`scripts/graph.js`**: Generates relationship cross-link matrices and Mermaid diagrams in `$BRAIN_PATH/graph.md`.
- **`scripts/stats.js`**: Computes entity counts, link density, and backlog metrics.
- **`package.json`**: Provides npm/bun scripts (`bun run lint`, `bun run index`, `bun run graph`, `bun run stats`).

---

## Step 7: Verify the Installation

Run the complete verification pipeline:

```bash
# 1. Run Schema & Link Integrity Linter
node scripts/lint.js

# 2. Compile Index & Alias Lookup Table
node scripts/index.js

# 3. Build Relationship Graph
node scripts/graph.js

# 4. Check Health Metrics
node scripts/stats.js
```

Verify that:
- `scripts/lint.js` reports **0 errors**.
- `$BRAIN_PATH/index.md` and `$BRAIN_PATH/aliases.json` are populated.
- `$BRAIN_PATH/graph.md` is generated.
- Initial log entry is recorded in `$BRAIN_PATH/log.md`.

---

## Agent Operational Routine (Going Forward)

When operating on this brain in future sessions:

| Inbound Trigger | Action Required |
|---|---|
| New meeting transcript or notes | Run [`skills/ingest/SKILL.md`](skills/ingest/SKILL.md) extract entities run [`skills/enrich/SKILL.md`](skills/enrich/SKILL.md) |
| Researching a person or company | Check `$BRAIN_PATH/aliases.json` read `$BRAIN_PATH/people/slug.md` enrich delta |
| Answering knowledge questions | Search `$BRAIN_PATH/` inspect `## State` & `See Also` links synthesize answer |
| User corrects a fact | Update Compiled Truth immediately add Timeline entry mark `confidence: high` |
| Routine maintenance / cleanup | Run `node scripts/lint.js` prune `$BRAIN_PATH/inbox/` resolve stale open threads |
