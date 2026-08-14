# INSTALL_FOR_AGENTS.md — Installation, Setup & Upgrade Guide for AI Agents

> **Target Audience:** Autonomous AI agents (Hermes, OpenClaw, Claude Code, Cursor, Codex, Gemini CLI, Aider) tasked with initializing or upgrading a pure local Markdown knowledge base.
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
   - Contains: `RESOLVER.md`, `schema.md`, `index.md`, `log.md`, `graph.md`, `aliases.json`, `.scripts/`, and the MECE entity directories (`people/`, `companies/`, `events/`, etc.).
   - **HARD INVARIANT:** `$BRAIN_PATH` **MUST NEVER EQUAL** `$WORKSPACE_ROOT`. Knowledge files must NEVER be dumped directly into the root workspace folder.

---

## Phase 1: Initial Discovery & Pre-Flight Confirmation (DO NOT SKIP)

Whether performing an **initial installation** or a **framework upgrade**, first discover the paths and ask the human operator for explicit confirmation.

### Step 1.1: Determine Target Paths & Mode
Ask the operator:
> *"Are we performing a **First Installation** of the LLM-Wiki knowledge base, or an **Upgrade / Refresh** from upstream GitHub?"*
> *"Where should the brain data live? (Default is `./BRAIN` inside this project)."*

Execute this path resolution logic strictly:
```bash
WORKSPACE_ROOT="$(pwd)"

# Precedence 1: Check existing environment variable ($BRAIN_PATH)
if [ -n "${BRAIN_PATH:-}" ]; then
  echo "Using existing BRAIN_PATH environment variable: $BRAIN_PATH"
# Precedence 2: Check .brainpath file if present
elif [ -f "$WORKSPACE_ROOT/.brainpath" ]; then
  BRAIN_PATH="$(cat "$WORKSPACE_ROOT/.brainpath")"
# Precedence 3: Default In-Workspace Folder ($WORKSPACE_ROOT/BRAIN)
else
  BRAIN_PATH="$WORKSPACE_ROOT/BRAIN"
fi

# Hard Invariant Guard Check:
if [ "$BRAIN_PATH" = "$WORKSPACE_ROOT" ]; then
  echo "Error: BRAIN_PATH cannot equal WORKSPACE_ROOT. Defaulting to $WORKSPACE_ROOT/BRAIN"
  BRAIN_PATH="$WORKSPACE_ROOT/BRAIN"
fi
```

### Step 1.2: Present Pre-Flight Confirmation Prompt (MANDATORY)
Present this prompt verbatim to the user (substituting resolved variables):

> **Please confirm the lifecycle operation before proceeding:**
> - **Operation:** `[First Installation | Upstream Framework Upgrade]`
> - **Execution Plane (`WORKSPACE_ROOT`):** `$WORKSPACE_ROOT` *(where agent skills and root SOPs live)*
> - **Data Plane (`BRAIN_PATH`):** `$BRAIN_PATH` *(where all markdown knowledge notes and entities live)*
>
> Shall I proceed with downloading the upstream release and applying this operation?

**Stop and wait for user approval before moving to Phase 2.**

---

## Phase 2: Upstream Staging & Shared Core Overlay

This core sequence runs for BOTH First Installation and Framework Upgrade:

```bash
# 1. Download latest upstream main release tarball into temporary staging directory
STAGING_DIR="/tmp/rainbow-llm-wiki-staging-$$"
mkdir -p "$STAGING_DIR"
curl -fsSL https://github.com/rainbowbreeze/rainbow-harness/archive/refs/heads/main.tar.gz | \
  tar -xz --strip-components=2 -C "$STAGING_DIR" "rainbow-harness-main/rainbow-llm-wiki"

# 2. Scaffold Core Data Plane Directories (harmless if existing)
mkdir -p "$BRAIN_PATH"/{people/.raw,companies/.raw,projects,ideas,concepts,meetings,events,deals,writing,sources,inbox,archive,.scripts}

# 3. Scaffold & Update Workspace Execution Plane Skills
mkdir -p "$WORKSPACE_ROOT"/skills
cp -r "$STAGING_DIR/skills"/* "$WORKSPACE_ROOT/skills/"
cp "$STAGING_DIR/AGENTS.md" "$STAGING_DIR/INSTALL_FOR_AGENTS.md" "$STAGING_DIR/package.json" "$WORKSPACE_ROOT/"

# 4. Copy Zero-Dependency Automation Utilities into Data Plane (.scripts/)
cp -r "$STAGING_DIR/scripts"/* "$BRAIN_PATH/.scripts/"

# 5. Update Core Data Plane Taxonomy & Schema
cp "$STAGING_DIR/BRAIN/RESOLVER.md" "$BRAIN_PATH/RESOLVER.md"
cp "$STAGING_DIR/BRAIN/schema.md" "$BRAIN_PATH/schema.md"

# 6. Copy / Update Canonical Directory Resolvers (README.md only — NEVER entity files)
for dir in people companies projects ideas concepts meetings events deals writing sources inbox archive; do
  cp "$STAGING_DIR/BRAIN/$dir/README.md" "$BRAIN_PATH/$dir/README.md"
done
```

---

## Phase 3: Mode-Specific Bootstrapping

Execute **EITHER** `3A` (First Install) **OR** `3B` (Upgrade):

### Option 3A: First Install Bootstrapping
If initializing a fresh brain:

```bash
# 1. Add placeholder .gitkeep files for .raw directories
touch "$BRAIN_PATH"/people/.raw/.gitkeep
touch "$BRAIN_PATH"/companies/.raw/.gitkeep

# 2. Initialize append-only event log
cat << 'EOF' > "$BRAIN_PATH/log.md"
# Knowledge Base Event Log

## YYYY-MM-DD
- **SYSTEM_INIT** | Knowledge base initialized at $BRAIN_PATH.
EOF

# 3. Initialize empty alias lookup map
echo "{}" > "$BRAIN_PATH/aliases.json"

# 4. Copy Optional Project-Local Memory (only if desired by user)
cp "$STAGING_DIR/CLAUDE.md" "$STAGING_DIR/GEMINI.md" "$WORKSPACE_ROOT/"
```

#### Step 3A.1: Custom User Domains (Universal Frontmatter Standard)
If the user requested custom domains (e.g., `personal`, `household`, `civic`, `hiring`):
1. `mkdir -p "$BRAIN_PATH/<custom_domain>"`
2. Create `$BRAIN_PATH/<custom_domain>/README.md` with the 3 canonical sections (What Goes Here, What Does NOT Go Here, Entity Page Template).
3. Ensure the entity page template implements the mandatory Universal Base Frontmatter Schema (`type`, `id`, `title`, `aliases`, `status`, `tags`, `relations`, `updated_at`).

---

### Option 3B: Framework Upgrade Actions
If upgrading an existing brain:

1. **Strict Data Protection Invariant**: Confirm that no user entity pages (`.md` files in `people/`, `companies/`, `events/`, `.raw/` sidecars, or `log.md`) were overwritten or altered.
2. **Preserve Project-Local Memory**: Do NOT overwrite any local `GEMINI.md` or `CLAUDE.md`.
3. **Record Upgrade Event**:
   Append an upgrade entry to `$BRAIN_PATH/log.md`:
   ```markdown
   - **SYSTEM_UPGRADE** | Refreshed framework scripts, skills, and schema from upstream GitHub (YYYY-MM-DD).
   ```

---

## Phase 4: Verification Pipeline & Cleanup

Run the complete validation and indexing suite from `$WORKSPACE_ROOT`:

```bash
# 1. Clean up temporary staging directory
rm -rf "$STAGING_DIR"

# 2. Run Schema & Link Integrity Linter
node "$BRAIN_PATH/.scripts/lint.js"

# 3. Recompile Index & Alias Lookup Table
node "$BRAIN_PATH/.scripts/index.js"

# 4. Rebuild Relationship Graph
node "$BRAIN_PATH/.scripts/graph.js"

# 5. Compute System Stats & Health Metrics
node "$BRAIN_PATH/.scripts/stats.js"
```

Verify that:
- `lint.js` reports **0 errors**.
- `$BRAIN_PATH/index.md`, `$BRAIN_PATH/graph.md`, and `$BRAIN_PATH/aliases.json` are populated.

---

## Phase 5: Ongoing Agent Operational Routine

When operating on this brain in future sessions:

| Inbound Trigger | Action Required |
|---|---|
| New meeting transcript or notes | Run [`skills/rainbowllmwiki-ingest/SKILL.md`](skills/rainbowllmwiki-ingest/SKILL.md) --> extract entities --> run [`skills/rainbowllmwiki-enrich/SKILL.md`](skills/rainbowllmwiki-enrich/SKILL.md) |
| Researching a person or company | Check `$BRAIN_PATH/aliases.json` --> read `$BRAIN_PATH/people/slug.md` --> enrich delta |
| Answering knowledge questions | Search `$BRAIN_PATH/` --> inspect `## State` & `See Also` links --> synthesize answer |
| User corrects a fact | Update Compiled Truth immediately --> add Timeline entry --> mark `confidence: high` |
| Routine maintenance / cleanup | Run `node "$BRAIN_PATH/.scripts/lint.js"` --> prune `$BRAIN_PATH/inbox/` --> resolve stale open threads |
