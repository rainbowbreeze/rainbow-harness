# INSTALL_FOR_AGENTS.md — Setup & Upgrade Guide

> **Target:** Autonomous AI agents initializing or upgrading a local Markdown knowledge base.

## 0. Architectural Invariants
1. **Execution Plane (`$WORKSPACE_ROOT`)**: Where the agent runs (`${HOME}`). Contains `skills/` and configs. **Never** dump knowledge files here.
2. **Data Plane (`$BRAIN_PATH`)**: Where knowledge entities live. **MUST NOT EQUAL** `$WORKSPACE_ROOT`.

---

## 1. Version Pre-Flight (Mandatory)

### 1.1 Path Resolution
```bash
WORKSPACE_ROOT="${HOME}"
if [ -z "${BRAIN_PATH:-}" ]; then
  echo "Error: BRAIN_PATH environment variable is not set."
  echo "Please provide the BRAIN_PATH environment variable (or ask the operator) and try again."
  exit 1
fi

# Hard Invariant Guard Check:
if [ "$BRAIN_PATH" = "$WORKSPACE_ROOT" ]; then
  echo "Error: BRAIN_PATH cannot equal WORKSPACE_ROOT.
  exit 1
fi
```

### Step 1.2: Check Installed vs. Upstream Version (Update Guard)
Before downloading tarballs or modifying files, probe the installed version and compare it against upstream GitHub:

```bash
INSTALLED_VERSION="0.0.0"
if [ -f "$BRAIN_PATH/.version" ]; then
  INSTALLED_VERSION="$(bun -e 'try{console.log(JSON.parse(fs.readFileSync("'"$BRAIN_PATH"'/.version")).version||"0.0.0")}catch(e){console.log("0.0.0")}')"
elif [ -f "$WORKSPACE_ROOT/package.json" ]; then
  INSTALLED_VERSION="$(bun -e 'try{console.log(JSON.parse(fs.readFileSync("'"$WORKSPACE_ROOT"'/package.json")).version||"0.0.0")}catch(e){console.log("0.0.0")}')"
fi

# 2. Fetch upstream release version from GitHub without downloading full repository
UPSTREAM_VERSION="$(curl -fsSL https://raw.githubusercontent.com/rainbowbreeze/rainbow-harness/main/rainbow-llm-wiki/package.json 2>/dev/null | bun -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>console.log(JSON.parse(d).version||"unknown"))')"

VERSION_CMP="$(bun -e '
  const p = v => v.replace(/^v/,"").split(".").map(n=>parseInt(n,10)||0);
  const [m1,n1,t1] = p(process.argv[1]||"0"), [m2,n2,t2] = p(process.argv[2]||"0");
  if(m1!==m2) console.log(m1>m2?1:-1); else if(n1!==n2) console.log(n1>n2?1:-1); else if(t1!==t2) console.log(t1>t2?1:-1); else console.log(0);
' "$UPSTREAM_VERSION" "$INSTALLED_VERSION")"

echo "--- PRE-FLIGHT RESULTS ---"
echo "INSTALLED_VERSION=$INSTALLED_VERSION | UPSTREAM_VERSION=$UPSTREAM_VERSION | VERSION_CMP=$VERSION_CMP"
```

**Agent Decision Logic (based on `VERSION_CMP`):**
- **Fresh Install** (`INSTALLED_VERSION == "0.0.0"`): Proceed to Phase 2.
- **Upgrade** (`1`): Proceed to Phase 2.
- **Up-to-Date** (`0`): **HALT** unless operator explicitly included `--force` in prompt.
- **Ahead** (`-1`): **ABORT** (downgrade prevented).

### 1.3 Confirmation
Ask operator: *"Ready for [Install/Upgrade] to v$UPSTREAM_VERSION at $BRAIN_PATH?"* (Wait for approval).

---

## 2. Upstream Staging
```bash
# 1. Scaffold Core Data Plane Directories (harmless if existing)
STAGING_DIR="/tmp/rainbow-llm-wiki-staging-$$"
mkdir -p "$STAGING_DIR" "$BRAIN_PATH"/{people/.raw,companies/.raw,schools,projects,ideas,concepts,meetings,events,deals,writing,sources,inbox,archive,.scripts}

# 2. Download latest upstream release tarball into temporary staging directory
curl -fsSL https://github.com/rainbowbreeze/rainbow-harness/archive/refs/heads/main.tar.gz | tar -xz --strip-components=2 -C "$STAGING_DIR" "rainbow-harness-main/rainbow-llm-wiki"

# 3. Scaffold and Update Workspace Execution Plane Skills
mkdir -p "$WORKSPACE_ROOT/skills"
cp -r "$STAGING_DIR/skills"/* "$WORKSPACE_ROOT/skills/"
cp "$STAGING_DIR/AGENTS.md" "$STAGING_DIR/INSTALL_FOR_AGENTS.md" "$STAGING_DIR/package.json" "$WORKSPACE_ROOT/"

# 4. Copy Zero-Dependency Automation Utilities into Data Plane (.scripts/)
cp -r "$STAGING_DIR/scripts"/* "$BRAIN_PATH/.scripts/"
# 5. Update Core Data Plane Taxonomy and Schema
cp "$STAGING_DIR/BRAIN/RESOLVER.md" "$STAGING_DIR/BRAIN/schema.md" "$BRAIN_PATH/"

# 6. Copy / Update Canonical Directory Resolvers (README.md only — NEVER entity files)
for dir in people companies schools projects ideas concepts meetings events deals writing sources inbox archive; do
  cp "$STAGING_DIR/BRAIN/$dir/README.md" "$BRAIN_PATH/$dir/README.md"
done

# 7. Write Data Plane Version Metadata File ($BRAIN_PATH/.version)
cat << EOF > "$BRAIN_PATH/.version"
{"version": "$UPSTREAM_VERSION", "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")", "upstream": "rainbowbreeze/rainbow-harness", "ref": "main"}
EOF
```

---

## 3. Bootstrapping

**If Fresh Install:**
```bash
# 1. Add placeholder .gitkeep files for .raw directories
touch "$BRAIN_PATH"/{people,companies}/.raw/.gitkeep

# 2. Initialize empty alias lookup map
echo "{}" > "$BRAIN_PATH/aliases.json"


# 3. Initialize or update append-only event log
[ ! -f "$BRAIN_PATH/log.md" ] && echo -e "# Knowledge Base Event Log\n" > "$BRAIN_PATH/log.md"
echo "- **SYSTEM_INIT** | Initialized v$UPSTREAM_VERSION at $BRAIN_PATH." >> "$BRAIN_PATH/log.md"
```

**If Upgrade:** 
Append `SYSTEM_UPGRADE` event to `log.md`. **Do not** overwrite user entities.

---

## 4. Verification
```bash
rm -rf "$STAGING_DIR"
cd "$WORKSPACE_ROOT"
bun run version
bun run lint
bun run index
bun run graph
bun run stats
```
Verify `lint.js` reports 0 errors and all indexes are populated.

---

## 4.1 Automated Maintenance Scheduler
> **Idempotency:** Check your native scheduled task list. Add this only if it doesn't exist.
> 
> Use your framework's native scheduling tool (e.g., `/schedule`) to execute the `rainbowllmwiki-maintain` skill every night at 2:00 AM (`0 2 * * *`). Do not use bash crontabs.

---

## 5. Ongoing Operations
| Trigger | Action |
|---|---|
| Routine check / Cleanup | Run `rainbowllmwiki-maintain` (lint, empty inbox, graph) |
| New info (email, notes) | Run `rainbowllmwiki-ingest` $\to$ `rainbowllmwiki-enrich` |
| User fact correction | Update Compiled Truth immediately $\to$ add Timeline entry $\to$ set `confidence: high` |
