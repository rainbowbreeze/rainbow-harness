---
name: rainbowllmwiki-enrich
version: 1.2.0
description: Tiered intelligence enrichment for people and companies in ${BRAIN_PATH}/
author: Rainbowbreeze
metadata:
  hermes:
    category: rainbowskills
    tags: [wiki, llm-wiki, enrichment, intelligence]
required_environment_variables:
  - name: BRAIN_PATH
    prompt: Where can I store the wiki files?
    help: Path to store the wiki files
    required_for: full functionality
---

# Tiered Entity Enrichment Protocol

Enrich person and company pages in `${BRAIN_PATH}/` to create comprehensive intelligence dossiers rather than shallow directory scrapes.

---

## 1. Enrichment Tiers

Calibrate research depth to the entity's importance:

| Tier | Category | Effort | Target Depth |
|---|---|---|---|
| **Tier 1 (Key)** | Close collaborators, key founders, partners | Deep | Full profile: Beliefs, What They're Building, Motivations, Communication Style, Contact Info (all emails/phones/locations), Relationships |
| **Tier 2 (Notable)** | Industry figures, portfolio leaders, frequent contacts | Moderate | Core state, beliefs, current ships, verified emails, phone numbers, handles, location |
| **Tier 3 (Minor)** | Brief mentions, occasional contacts | Light | Role, company, basic connection, verified email(s)/phone(s), one-line summary |

---

## 2. The 7-Step Enrichment Procedure

### Step 1: Extract Entities, Slugs & Contact Details
- Identify person or company name.
- Extract all personal and contact metadata:
  - **Emails**: Work, personal, academic, or alternate addresses.
  - **Phone numbers**: Mobile, direct office, WhatsApp/Signal numbers (with country code).
  - **Location & Timezone**: City, region, country.
  - **Online presence**: Personal website, GitHub, LinkedIn, Twitter/X, Discord/Telegram handles.
- Generate canonical slug (e.g. `john-doe.md` or `acme-corp.md`).

### Step 2: Check Brain State & Deduplicate
- Search `aliases` across `${BRAIN_PATH}/people/*.md` or `${BRAIN_PATH}/companies/*.md` (or check `${BRAIN_PATH}/aliases.json`) using name, all email addresses, and phone numbers.
- If an alias or slug matches **UPDATE existing file** (merge newly discovered emails, phone numbers, and aliases).
- If no match **CREATE new file** in `${BRAIN_PATH}/people/` or `${BRAIN_PATH}/companies/` using the standard template.

### Step 3: Extract Signal & Epistemic Attribution
- Classify claims into:
  - `observed` (from direct meetings, emails, or messages)
  - `self-described` (from interviews, bios, public writing)
  - `inferred` (synthesized patterns)
- Assign confidence rating (`high`, `medium`, `low`).

### Step 4: Update Compiled Truth (Above the line)
- Update/rewrite the Executive Summary blockquote.
- Update YAML frontmatter:
  - Add/merge all known email addresses into `emails: ["..."]`.
  - Add/merge all phone numbers into `phones: ["..."]`.
  - Set `location:` and `website:` if available.
  - Ensure all emails, phone numbers, nicknames, and handles are listed in `aliases: ["..."]`.
- Update `## State` with current role, company, and key context.
- Update/create `## Contact & Personal Info` section with:
  - **Emails**: Full list of email addresses with context labels (e.g., Work, Personal).
  - **Phone Numbers**: Full list of phone numbers with context labels (e.g., Mobile, Office).
  - **Location**: City, country, and timezone.
  - **Socials / Handles**: Clickable links to profiles and handles.
- Populate beliefs, what they are building, motivations, and communication style.

### Step 5: Append to Timeline (Below the line)
- Append a new reverse-chronological entry under `## Timeline`:
  `- **YYYY-MM-DD** | [Source Type: Source Name] — Summary of event/observation.`

### Step 6: Maintain Bidirectional Links
- When adding a link to another entity (e.g. linking `jane-doe.md` to `acme-corp.md`), also add the reciprocal backlink in the related entity's page.

### Step 7: Update Index & Log
- Run `bun run index` (or `node ${BRAIN_PATH}/.scripts/index.js`) to reflect changes in `${BRAIN_PATH}/index.md` and `${BRAIN_PATH}/aliases.json`.
- Append a 1-line summary of the enrichment to `${BRAIN_PATH}/log.md`.
