# INSTALL_FOR_AGENTS.md — Installation & Setup Guide for AI Agents

> **Target Audience:** Autonomous AI agents (Hermes, OpenClaw, Claude Code, Cursor, Codex, Gemini CLI, Aider) tasked with initializing or managing a pure local Markdown knowledge base.
> **Design Philosophy:** 100% local, zero-database, zero-cloud-lock-in, Git-native Markdown wiki.

---

## Architectural Invariant: Execution Plane vs. Data Plane

Before doing anything, understand this strict two-plane separation:

1. **`$WORKSPACE_ROOT` (Agent Execution Plane)**:
   - The root repository or workspace where the AI agent runs (`pwd`).
   - Contains: `skills/`, `scripts/`, `package.json`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
   - **CRITICAL RULE:** Skills MUST live in `$WORKSPACE_ROOT/skills/`. **NEVER create or copy `skills/` inside the brain data directory.**

2. **`$BRAIN_PATH` (Knowledge Base Data Plane)**:
   - Where knowledge notes, entity files, logs, and schemas live.
   - Contains: `RESOLVER.md`, `schema.md`, `index.md`, `log.md`, `graph.md`, `aliases.json`, and the MECE entity directories (`people/`, `companies/`, etc.).
   - **HARD INVARIANT:** `$BRAIN_PATH` **MUST NEVER EQUAL** `$WORKSPACE_ROOT`. Knowledge files must NEVER be dumped directly into the root workspace folder.

---

## Step 0: Initial Discovery & User Confirmation (DO NOT SKIP)

Before creating directories or files, **ask the human operator**:

1. **Brain Location**:
   > *"Where would you like to create your knowledge base? Default is `./BRAIN` inside this project, or `~/brain` for a standalone personal repository."*
2. **Domain Customization**:
   > *"The standard domains are: `people`, `companies`, `projects`, `ideas`, `concepts`, `meetings`, `deals`, `writing`, `sources`, `inbox`, `archive`. Would you like to add any specialized domains (e.g. `personal`, `household`, `civic`, `hiring`)?"*

### Path Assignment Logic (Execute strictly):
```bash
WORKSPACE_ROOT="$(pwd)"

# Mode A: In-Workspace Brain (Default & Recommended)
# When the user says "here", "in this project", or accepts the default:
BRAIN_PATH="$WORKSPACE_ROOT/BRAIN"

# Mode B: External Standalone Brain (e.g. ~/brain or /custom/path)
# When the user specifies an external location:
# BRAIN_PATH="$HOME/brain"
# echo "$BRAIN_PATH" > "$WORKSPACE_ROOT/.brainpath"

# Invariant Guard Check:
if [ "$BRAIN_PATH" = "$WORKSPACE_ROOT" ]; then
  echo "Error: BRAIN_PATH cannot equal WORKSPACE_ROOT. Defaulting to $WORKSPACE_ROOT/BRAIN"
  BRAIN_PATH="$WORKSPACE_ROOT/BRAIN"
fi
```

### Step 0.5: Final Pre-Flight Confirmation (DO NOT SKIP)

Before executing any `mkdir`, file creation, or file copy commands, **you MUST present the exact resolved paths to the user and wait for their confirmation**.

Present this prompt to the user verbatim (substituting the resolved variables):

> **Please confirm the installation paths before proceeding:**
> - **Execution Plane (`WORKSPACE_ROOT`):** `$WORKSPACE_ROOT` *(where skills, scripts, and agent SOPs live)*
> - **Data Plane (`BRAIN_PATH`):** `$BRAIN_PATH` *(where all markdown knowledge notes and entities live)*
> - **Custom Domains:** `[List custom domains if requested, or "None"]`
>
> Shall I proceed with scaffolding these directories and installing the knowledge base?

**Stop and wait for user approval before moving to Step 1.**

---

## Step 1: Scaffold Directory Structure

Create the `$BRAIN_PATH` directory structure and the `$WORKSPACE_ROOT` tooling directories:

```bash
# 1. Create Brain Data Plane
mkdir -p "$BRAIN_PATH"/{people/.raw,companies/.raw,projects,ideas,concepts,meetings,deals,writing,sources,inbox,archive}

# 2. Create Workspace Execution Plane (in $WORKSPACE_ROOT, NOT in $BRAIN_PATH)
mkdir -p "$WORKSPACE_ROOT"/skills/{rainbowllmwiki-enrich,rainbowllmwiki-ingest,rainbowllmwiki-query,rainbowllmwiki-maintain,rainbowllmwiki-dedup-merge}
mkdir -p "$WORKSPACE_ROOT"/scripts

# 3. Add placeholder .gitkeep files for .raw directories
touch "$BRAIN_PATH"/people/.raw/.gitkeep
touch "$BRAIN_PATH"/companies/.raw/.gitkeep
```

---

## Step 2: Install Core Brain Governance Files

Copy or write the core governance files directly into `$BRAIN_PATH/`:

1. **`$BRAIN_PATH/RESOLVER.md`**: Master decision tree for filing entities and notes. Walk this tree before writing any new file.
2. **`$BRAIN_PATH/schema.md`**: Structural specifications, Universal Base Frontmatter schema, Two-Layer rules (Compiled Truth above `---`, Timeline below `---`), and epistemic tags (`observed`, `self-described`, `inferred`).
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

> [!IMPORTANT]
> **DO NOT generate directory README resolvers from scratch.**
> Always copy the canonical `README.md` resolver files from this repository or use the canonical 3-section template below.

If installing from a local clone of this repository:
```bash
# Copy all canonical directory resolvers into $BRAIN_PATH
for dir in people companies projects ideas concepts meetings deals writing sources inbox archive; do
  cp "BRAIN/$dir/README.md" "$BRAIN_PATH/$dir/README.md"
done
```

Every resolver `README.md` must adhere to this exact 3-section structure:
1. **Section 1: What Goes Here** — Concrete inclusion criteria and slug convention.
2. **Section 2: What Does NOT Go Here** — Clear disambiguation from neighboring directories.
3. **Section 3: Entity Page Template** — Complete Markdown template adhering to the Universal Base Frontmatter Schema.

---

## Step 3.5: Creating Custom User Domains (Universal Frontmatter Standard)

If the user requested custom domains (e.g., `personal`, `household`, `civic`, `hiring`), the agent MUST:

1. Create the directory: `mkdir -p "$BRAIN_PATH/<custom_domain>"`
2. Create `$BRAIN_PATH/<custom_domain>/README.md` with the 3 canonical sections.
3. **MANDATORY**: Ensure the entity page template implements the **Universal Base Frontmatter Schema**:

```yaml
---
type: "<domain_singular>"   # e.g., personal, hiring, household, book
id: "<canonical-slug>"      # matches filename without .md (kebab-case)
title: "<Human Readable Title>"
aliases: ["<Variant 1>", "<Variant 2>"] # array of alternate names, handles, emails
status: active              # active | draft | in-progress | on-hold | closed | archived
tags: ["tag1", "tag2"]      # categorization tags
relations:                  # typed bidirectional links to other entities
  - target: "<directory>/<target-slug>"
    type: "<relationship-type>"
updated_at: "YYYY-MM-DD"    # ISO date of last modification
# [Optional domain-specific fields added below this line]
---
```

---

## Step 4: Install Agent Skills Layer (`$WORKSPACE_ROOT/skills/`)

> [!WARNING]
> Skills MUST be placed in `$WORKSPACE_ROOT/skills/` (the workspace root), NEVER inside `$BRAIN_PATH/skills/`.

Copy or write the skill files into `$WORKSPACE_ROOT/skills/`:
- `$WORKSPACE_ROOT/skills/RESOLVER.md`: Master skill dispatcher mapping prompts/triggers to skills.
- `$WORKSPACE_ROOT/skills/rainbowllmwiki-enrich/SKILL.md`: 7-step tiered enrichment protocol for people and companies.
- `$WORKSPACE_ROOT/skills/rainbowllmwiki-ingest/SKILL.md`: Multi-source ingestion protocol for meetings, transcripts, and notes.
- `$WORKSPACE_ROOT/skills/rainbowllmwiki-query/SKILL.md`: Pure Markdown search, alias resolution, and backlink traversal.
- `$WORKSPACE_ROOT/skills/rainbowllmwiki-maintain/SKILL.md`: Health audit, linting, dead link fixing, and inbox pruning protocol.
- `$WORKSPACE_ROOT/skills/rainbowllmwiki-dedup-merge/SKILL.md`: Entity deduplication, timeline merging, and cross-reference updating.

---

## Step 5: Configure Agent Protocol Files

Ensure agent instruction files are installed in `$WORKSPACE_ROOT/`:

1. **`$WORKSPACE_ROOT/AGENTS.md`**: Operational rules for Cursor, Hermes, OpenClaw, Codex, Gemini CLI.
2. **`$WORKSPACE_ROOT/CLAUDE.md`**: Operational guidelines for Claude Code.
3. **`$WORKSPACE_ROOT/GEMINI.md`**: Project memory and documentation sync file.

### Key Golden Rules to Enforce:
- **Always read `$BRAIN_PATH/RESOLVER.md` before creating any file.**
- **Check `aliases` in existing files or `$BRAIN_PATH/aliases.json` before creating a person/company to prevent split-brain duplicates.**
- **Maintain Two-Layer separation (`---`) between Compiled Truth (above) and Timeline (below).**
- **Tag subjective assertions with epistemic labels (`observed`, `self-described`, `inferred`) and confidence scores.**
- **Do NOT execute `git commit` or `git push` unless explicitly requested by the user.**

---

## Step 6: Install Zero-Dependency Validation & Indexing Scripts

Install the standard Node/Bun automation scripts in `$WORKSPACE_ROOT/scripts/`:

- **`$WORKSPACE_ROOT/scripts/lint.js`**: Validates Universal Base YAML frontmatter, checks for broken relative markdown links, and flags duplicate aliases in `$BRAIN_PATH`.
- **`$WORKSPACE_ROOT/scripts/index.js`**: Rebuilds `$BRAIN_PATH/index.md` and `$BRAIN_PATH/aliases.json` across all files.
- **`$WORKSPACE_ROOT/scripts/graph.js`**: Generates relationship cross-link matrices and Mermaid diagrams in `$BRAIN_PATH/graph.md`.
- **`$WORKSPACE_ROOT/scripts/stats.js`**: Computes entity counts, link density, and backlog metrics in `$BRAIN_PATH`.
- **`$WORKSPACE_ROOT/package.json`**: Provides npm/bun scripts (`bun run lint`, `bun run index`, `bun run graph`, `bun run stats`).

---

## Step 7: Verify the Installation

Run the complete verification pipeline from `$WORKSPACE_ROOT`:

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
| New meeting transcript or notes | Run [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md) extract entities run [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md) |
| Researching a person or company | Check `$BRAIN_PATH/aliases.json` read `$BRAIN_PATH/people/slug.md` enrich delta |
| Answering knowledge questions | Search `$BRAIN_PATH/` inspect `## State` & `See Also` links synthesize answer |
| User corrects a fact | Update Compiled Truth immediately add Timeline entry mark `confidence: high` |
| Routine maintenance / cleanup | Run `node scripts/lint.js` prune `$BRAIN_PATH/inbox/` resolve stale open threads |
