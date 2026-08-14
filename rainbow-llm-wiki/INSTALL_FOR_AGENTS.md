# INSTALL_FOR_AGENTS.md — Installation & Setup Guide for AI Agents

> **Target Audience:** Autonomous AI agents (Hermes, OpenClaw, Claude Code, Cursor, Codex, Gemini CLI, Aider) tasked with initializing or managing a pure local Markdown knowledge base.
> **Design Philosophy:** 100% local, zero-database, zero-cloud-lock-in, Git-native Markdown wiki.

---

## Architectural Invariant: Execution Plane vs. Data Plane

Before doing anything, understand this strict two-plane separation:

1. **`$WORKSPACE_ROOT` (Agent Execution Plane)**:
   - The root repository or workspace where the AI agent runs (`pwd`).
   - Contains: `skills/`, `package.json`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (`.scripts/` live inside `$BRAIN_PATH`).
   - **CRITICAL RULE:** Skills MUST live in `$WORKSPACE_ROOT/skills/`. **NEVER create or copy `skills/` inside the brain data directory.**

2. **`$BRAIN_PATH` (Knowledge Base Data Plane)**:
   - Where knowledge notes, entity files, logs, and schemas live.
   - Contains: `RESOLVER.md`, `schema.md`, `index.md`, `log.md`, `graph.md`, `aliases.json`, `.scripts/`, and the MECE entity directories (`people/`, `companies/`, etc.).
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

# Precedence 1: Check existing environment variable ($BRAIN_PATH)
if [ -n "${BRAIN_PATH:-}" ]; then
  echo "Using existing BRAIN_PATH environment variable: $BRAIN_PATH"
# Precedence 1: Check .brainpath file if present
elif [ -f "$WORKSPACE_ROOT/.brainpath" ]; then
  BRAIN_PATH="$(cat "$WORKSPACE_ROOT/.brainpath")"
# Precedence 2: Mode A — In-Workspace Brain (Default & Recommended)
else
  BRAIN_PATH="$WORKSPACE_ROOT/BRAIN"
fi

# Mode B: External Standalone Brain (e.g. ~/brain or /custom/path requested explicitly)
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

## Step 1: Scaffold Directory Structure & Download Upstream Release Tarball

Create the `$BRAIN_PATH` directory structure and unpack the canonical GitHub framework release into a temporary staging folder (`/tmp/rainbow-llm-wiki-staging-$$`):

```bash
# 1. Create Brain Data Plane
mkdir -p "$BRAIN_PATH"/{people/.raw,companies/.raw,projects,ideas,concepts,meetings,events,deals,writing,sources,inbox,archive}

# 2. Download latest upstream release tarball into staging directory
STAGING_DIR="/tmp/rainbow-llm-wiki-staging-$$"
mkdir -p "$STAGING_DIR"
curl -fsSL https://github.com/rainbowbreeze/rainbow-harness/archive/refs/heads/main.tar.gz | \
  tar -xz --strip-components=2 -C "$STAGING_DIR" "rainbow-harness-main/rainbow-llm-wiki"

# 3. Create Workspace Execution Plane & Data Plane Script Folder
mkdir -p "$WORKSPACE_ROOT"/skills
mkdir -p "$BRAIN_PATH"/.scripts

# 4. Copy Core Automation Scripts & Execution Plane Docs from Staging
cp -r "$STAGING_DIR/scripts"/* "$BRAIN_PATH/.scripts/"
cp -r "$STAGING_DIR/skills"/* "$WORKSPACE_ROOT/skills/"
cp "$STAGING_DIR/AGENTS.md" "$STAGING_DIR/package.json" "$WORKSPACE_ROOT/"

# 5. Add placeholder .gitkeep files for .raw directories
touch "$BRAIN_PATH"/people/.raw/.gitkeep
touch "$BRAIN_PATH"/companies/.raw/.gitkeep
```

---

## Step 2: Install Core Brain Governance Files

Copy the canonical core governance files from staging directly into `$BRAIN_PATH/`:

1. **`$BRAIN_PATH/RESOLVER.md`**: Master decision tree copied from `$STAGING_DIR/BRAIN/RESOLVER.md`. Walk this tree before writing any new file.
2. **`$BRAIN_PATH/schema.md`**: Structural specifications copied from `$STAGING_DIR/BRAIN/schema.md`.
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
> Always copy the canonical `README.md` resolver files from the staging directory.

```bash
# Copy all canonical directory resolvers from staging into $BRAIN_PATH
for dir in people companies projects ideas concepts meetings events deals writing sources inbox archive; do
  cp "$STAGING_DIR/BRAIN/$dir/README.md" "$BRAIN_PATH/$dir/README.md"
done

# Remove temporary staging directory
rm -rf "$STAGING_DIR"
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

1. **`$WORKSPACE_ROOT/AGENTS.md`**: Universal agent operational protocol and rules for all autonomous AI assistants.
2. **Project-Local Memory (Optional)**: If operating inside a persistent project workspace, create or preserve `GEMINI.md` / `CLAUDE.md` to store project-specific context and memory.

### Key Golden Rules to Enforce:
- **Always read `$BRAIN_PATH/RESOLVER.md` before creating any file.**
- **Check `aliases` in existing files or `$BRAIN_PATH/aliases.json` before creating a person/company to prevent split-brain duplicates.**
- **Maintain Two-Layer separation (`---`) between Compiled Truth (above) and Timeline (below).**
- **Tag subjective assertions with epistemic labels (`observed`, `self-described`, `inferred`) and confidence scores.**
- **Do NOT execute `git commit` or `git push` unless explicitly requested by the user.**

---

## Step 6: Install Zero-Dependency Validation & Indexing Scripts

Automation scripts live inside `$BRAIN_PATH/.scripts/`:

- **`$BRAIN_PATH/.scripts/lint.js`**: Validates Universal Base YAML frontmatter, checks for broken relative markdown links, and flags duplicate aliases in `$BRAIN_PATH`.
- **`$BRAIN_PATH/.scripts/index.js`**: Rebuilds `$BRAIN_PATH/index.md` and `$BRAIN_PATH/aliases.json` across all files.
- **`$BRAIN_PATH/.scripts/graph.js`**: Generates relationship cross-link matrices and Mermaid diagrams in `$BRAIN_PATH/graph.md`.
- **`$BRAIN_PATH/.scripts/stats.js`**: Computes entity counts, link density, and backlog metrics in `$BRAIN_PATH`.
- **`$WORKSPACE_ROOT/package.json`**: Provides npm/bun scripts (`bun run lint`, `bun run index`, `bun run graph`, `bun run stats`).

---

## Step 7: Verify the Installation

Run the complete verification pipeline:

```bash
# 1. Run Schema & Link Integrity Linter
node "$BRAIN_PATH/.scripts/lint.js"

# 2. Compile Index & Alias Lookup Table
node "$BRAIN_PATH/.scripts/index.js"

# 3. Build Relationship Graph
node "$BRAIN_PATH/.scripts/graph.js"

# 4. Check Health Metrics
node "$BRAIN_PATH/.scripts/stats.js"
```

Verify that:
- `lint.js` reports **0 errors**.
- `$BRAIN_PATH/index.md` and `$BRAIN_PATH/aliases.json` are populated.
- `$BRAIN_PATH/graph.md` is generated.
- Initial log entry is recorded in `$BRAIN_PATH/log.md`.

---

## Step 8: Upgrading & Refreshing Framework from Upstream GitHub

When requested to **"update llm-wiki"** or **"refresh framework from GitHub"**, the agent MUST refresh all execution plane scripts, skills, and base templates **without ever modifying or deleting user data files** (`people/`, `companies/`, `events/`, `.raw/`, `log.md`).

Execute this selective tarball overlay script:

```bash
# 1. Download latest upstream release tarball into staging directory
STAGING_DIR="/tmp/rainbow-llm-wiki-upgrade-$$"
mkdir -p "$STAGING_DIR"
curl -fsSL https://github.com/rainbowbreeze/rainbow-harness/archive/refs/heads/main.tar.gz | \
  tar -xz --strip-components=2 -C "$STAGING_DIR" "rainbow-harness-main/rainbow-llm-wiki"

# 2. Update Core Execution Plane Tools & SOPs
mkdir -p "$BRAIN_PATH"/.scripts && cp -r "$STAGING_DIR/scripts"/* "$BRAIN_PATH/.scripts/"
cp -r "$STAGING_DIR/skills"/* "$WORKSPACE_ROOT/skills/"
cp "$STAGING_DIR/AGENTS.md" "$STAGING_DIR/INSTALL_FOR_AGENTS.md" "$STAGING_DIR/package.json" "$WORKSPACE_ROOT/"

# 3. Update Core Data Plane Taxonomy & Schema
cp "$STAGING_DIR/BRAIN/RESOLVER.md" "$BRAIN_PATH/RESOLVER.md"
cp "$STAGING_DIR/BRAIN/schema.md" "$BRAIN_PATH/schema.md"

# 4. Update Canonical Directory Resolvers (README.md only — NEVER entity files)
for dir in people companies projects ideas concepts meetings events deals writing sources inbox archive; do
  mkdir -p "$BRAIN_PATH/$dir"
  cp "$STAGING_DIR/BRAIN/$dir/README.md" "$BRAIN_PATH/$dir/README.md"
done

# 5. Clean up temporary staging directory
rm -rf "$STAGING_DIR"

# 6. Re-run System Audit & Re-index to verify zero schema regressions
node "$BRAIN_PATH/.scripts/lint.js"
node "$BRAIN_PATH/.scripts/index.js"
node "$BRAIN_PATH/.scripts/graph.js"
node "$BRAIN_PATH/.scripts/stats.js"
```

After updating, record the upgrade event in `$BRAIN_PATH/log.md`:
```markdown
- **SYSTEM_UPGRADE** | Refreshed framework scripts, skills, and schema from upstream GitHub (YYYY-MM-DD).
```

---

## Agent Operational Routine (Going Forward)

When operating on this brain in future sessions:

| Inbound Trigger | Action Required |
|---|---|
| New meeting transcript or notes | Run [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md) extract entities run [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md) |
| Researching a person or company | Check `$BRAIN_PATH/aliases.json` read `$BRAIN_PATH/people/slug.md` enrich delta |
| Answering knowledge questions | Search `$BRAIN_PATH/` inspect `## State` & `See Also` links synthesize answer |
| User corrects a fact | Update Compiled Truth immediately add Timeline entry mark `confidence: high` |
| Routine maintenance / cleanup | Run `node "$BRAIN_PATH/.scripts/lint.js"` prune `$BRAIN_PATH/inbox/` resolve stale open threads |
