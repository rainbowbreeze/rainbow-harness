---
name: enrich
version: 1.0.0
description: |
  Tiered intelligence enrichment protocol for people and companies. Creates and updates
  entity pages with compiled truth, timeline evidence, epistemic citations, and bidirectional links in BRAIN/.
triggers:
  - "enrich"
  - "create person"
  - "update company"
  - "who is this person"
  - "research company"
mutating: true
writes_to:
  - BRAIN/people/
  - BRAIN/companies/
---

# Tiered Entity Enrichment Protocol

Enrich person and company pages in `BRAIN/` to create comprehensive intelligence dossiers rather than shallow directory scrapes.

---

## 1. Enrichment Tiers

Calibrate research depth to the entity's importance:

| Tier | Category | Effort | Target Depth |
|---|---|---|---|
| **Tier 1 (Key)** | Close collaborators, key founders, partners | Deep | Full profile: Beliefs, What They're Building, Motivations, Communication Style, Trajectory, Relationships |
| **Tier 2 (Notable)** | Industry figures, portfolio leaders, frequent contacts | Moderate | Core state, beliefs, current ships, verified contact handles |
| **Tier 3 (Minor)** | Brief mentions, occasional contacts | Light | Role, company, basic connection, one-line summary |

---

## 2. The 7-Step Enrichment Procedure

### Step 1: Extract Entities & Slugs
- Identify person or company name.
- Generate canonical slug (e.g. `john-doe.md` or `acme-corp.md`).

### Step 2: Check Brain State & Deduplicate
- Search `aliases` across `BRAIN/people/*.md` or `BRAIN/companies/*.md` (or check `BRAIN/aliases.json`).
- If an alias or slug matches **UPDATE existing file**.
- If no match **CREATE new file** in `BRAIN/people/` or `BRAIN/companies/` using standard template.

### Step 3: Extract Signal & Epistemic Attribution
- Classify claims into:
  - `observed` (from direct meetings or messages)
  - `self-described` (from interviews, bios, public writing)
  - `inferred` (synthesized patterns)
- Assign confidence rating (`high`, `medium`, `low`).

### Step 4: Update Compiled Truth (Above the line)
- Update/rewrite the Executive Summary blockquote.
- Update `## State` with current role, company, and key context.
- Populate beliefs, what they are building, motivations, and communication style.

### Step 5: Append to Timeline (Below the line)
- Append a new reverse-chronological entry under `## Timeline`:
  `- **YYYY-MM-DD** | [Source Type: Source Name] — Summary of event/observation.`

### Step 6: Maintain Bidirectional Links
- When adding a link to another entity (e.g. linking `jane-doe.md` to `acme-corp.md`), also add the reciprocal backlink in the related entity's page.

### Step 7: Update Index & Log
- Run `bun run index` to reflect changes in `BRAIN/index.md` and `BRAIN/aliases.json`.
- Append a 1-line summary of the enrichment to `BRAIN/log.md`.
