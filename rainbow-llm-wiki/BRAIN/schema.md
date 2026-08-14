# schema.md — Knowledge Base Schema & Conventions

> **Version:** 1.1.0 (Pure Local Markdown Edition)  
> This specification defines the structural conventions, frontmatter schemas, two-layer page architecture, and epistemic discipline for all knowledge files in the brain.

---

## 1. The Two-Layer Page Architecture

Every page in this knowledge base is split into two distinct structural layers by a horizontal rule (`---`):

```markdown
---
[YAML Frontmatter]
---

# Page Title

> Executive summary: 1-2 sentence core distillation.

## State
[Structured key-value fields and current status]

## [Domain-Specific Sections]
[Compiled Truth & Synthesis]

## Open Threads
- Active items, follow-ups, pending questions

## See Also
- [Related Entity](../category/slug.md)

---

## Timeline
- **YYYY-MM-DD** | [Source Type: Source Name] — Dated, immutable evidence log.
```

### Above the Line: Compiled Truth (Synthesis)
- **Mutable & Pre-computed**: Updated and rewritten whenever new information arrives.
- **Executive Summary**: The first blockquote must provide immediate context so anyone reading the top 5 lines understands the current state of play.
- **State & Beliefs**: Contains high-signal structured assessments and current operational status.
- **Open Threads**: Active items currently requiring action. When resolved, they are removed from here and logged in the Timeline below.

### Below the Line: Timeline (Evidence Log)
- **Immutable & Append-Only**: Never delete or rewrite past timeline entries.
- **Reverse Chronological**: Newest entries at the top of the Timeline section.
- **Format**: `- **YYYY-MM-DD** | [Source Type: Source Description] — Clear description of what happened or what was observed.`

---

## 2. Universal Base Frontmatter Schema (MANDATORY)

Every entity file in this knowledge base—whether a built-in standard domain or a newly created custom domain—**MUST** inherit and include these core fields:

```yaml
---
type: "<domain_singular>"   # e.g., person, company, project, concept, idea, meeting, deal, writing, personal, household, hiring
id: "<canonical-slug>"      # matches filename without .md (lowercase, kebab-case)
title: "<Human Readable Title>"
aliases: ["<Variant 1>", "<Variant 2>"] # array of alternate names, handles, emails, or abbreviations
status: active              # active | draft | in-progress | on-hold | closed | archived
tags: ["tag1", "tag2"]      # categorization tags
relations:                  # typed bidirectional links to other entities
  - target: "<directory>/<target-slug>"
    type: "<relationship-type>" # e.g., founder, collaborator, investor, parent-project, depends-on
updated_at: "YYYY-MM-DD"    # ISO date of last modification
---
```

### Domain-Specific Fields (Extensions)
Domain-specific fields are additive extensions on top of the Universal Base Schema:
- **Person**: `role`, `company`
- **Company**: `stage`, `industry`, `website`
- **Project**: `owner`, `repo`
- **Meeting**: `date`, `participants`
- **Event**: `start_date`, `end_date`, `location`, `url`
- **Deal**: `company`, `stage`, `amount`, `lead_investor`
- **Concept**: `domain`
- **Idea**: `target_domain`
- **Custom Domains** (e.g. `hiring`, `personal`, `household`): define domain-specific keys in addition to the base schema.

---

## 3. Epistemic Discipline Rules

Contextual assertions and personality assessments are high-value but prone to hallucination or drift. Adhere strictly to these rules:

1. **Explicit Source Citation**: Every subjective claim must cite where it was learned.
2. **Three Source Types**:
   - `observed`: Directly witnessed by you or the user (e.g., in a meeting, email, or direct dialogue).
   - `self-described`: Stated by the subject themselves (e.g., in an interview, bio, podcast, or tweet).
   - `inferred`: Deductions or patterns analyzed across multiple data points.
3. **Confidence Scoring**:
   - `high`: 5+ direct interactions or corroborated by multiple primary sources.
   - `medium`: 2–4 interactions or single reliable primary source.
   - `low`: 1 brief mention, second-hand report, or speculative inference.
4. **Primacy of User Corrections**: Direct user corrections override any inference immediately without requiring corroboration.

Example format:
```markdown
## What They Believe
- Believes distributed teams outperform centralized offices — observed: [Team Sync, 2026-03-12], confidence: high
- Skeptical of closed LLM API lock-in — self-described: [Blog Post, 2026-01-15], confidence: high
- Likely seeking Series B lead investor in Q3 — inferred: [Hiring freeze + runway signals], confidence: medium
```

---

## 4. Canonical Slugs & Aliases

1. **Canonical Slugs**:
   - People: `first-last.md` (e.g., `ada-lovelace.md`, `alan-turing.md`)
   - Companies: `company-name.md` (e.g., `acme-corp.md`, `openai.md`)
   - Collision resolution: If two entities share a name, disambiguate with domain or company: `john-smith-acme.md`, `john-smith-venture.md`.
2. **Aliases Array in Frontmatter**:
   - Every variant name, email address, Twitter/X handle, nickname, or misspelling must be listed in `aliases`.
   - Before creating any new entity, the agent must check all existing `aliases` to prevent duplicate creation.

---

## 5. Entity YAML Frontmatter Schemas

### Person (`people/first-last.md`)
```yaml
---
type: person
id: ada-lovelace
title: Ada Lovelace
aliases: ["Augusta Ada King", "Countess of Lovelace", "ada@example.com", "@adalovelace"]
status: active # active | dormant | former
tags: [computing, algorithm-design, pioneer]
relations:
  - target: "companies/analytical-engine-project"
    type: "collaborator"
  - target: "people/charles-babbage"
    type: "close-collaborator"
role: Mathematician & Computing Pioneer
company: Analytical Engine Project
updated_at: "2026-08-13"
---
```

### Company (`companies/company-name.md`)
```yaml
---
type: company
id: acme-corp
title: Acme Corporation
aliases: ["Acme Inc", "Acme Labs", "acme.com"]
status: active # active | acquired | dead | evaluating
tags: [devtools, infrastructure]
relations:
  - target: "people/jane-doe"
    type: "founder"
stage: Series A # Seed | Series A | Series B | Growth | Public | Non-profit
industry: Developer Tools
website: "https://acme.example.com"
updated_at: "2026-08-13"
---
```

### Project (`projects/project-name.md`)
```yaml
---
type: project
id: knowledge-engine
title: Knowledge Engine
aliases: ["kb-engine"]
status: in-progress # planning | in-progress | on-hold | completed | archived
tags: [knowledge-base, markdown, ai]
relations: []
owner: "people/first-last"
repo: "https://github.com/org/repo"
updated_at: "2026-08-13"
---
```

### Concept (`concepts/concept-name.md`)
```yaml
---
type: concept
id: mece-principle
title: MECE Principle
aliases: ["Mutually Exclusive Collectively Exhaustive", "MECE"]
status: active
tags: [mental-model, taxonomy, structuring]
relations: []
domain: Knowledge Architecture
updated_at: "2026-08-13"
---
```

### Idea (`ideas/idea-name.md`)
```yaml
---
type: idea
id: automated-backlink-linter
title: Automated Backlink Linter
aliases: []
status: raw # raw | evaluating | validated | discarded | graduated
tags: [linter, graph, markdown]
relations: []
target_domain: Developer Tools
updated_at: "2026-08-13"
---
```

### Meeting (`meetings/YYYY-MM-DD-title.md`)
```yaml
---
type: meeting
id: 2026-08-13-architecture-review
title: Knowledge Base Architecture Review
aliases: []
status: completed
tags: [architecture, review]
relations:
  - target: "projects/knowledge-engine"
    type: "review-target"
date: "2026-08-13"
participants:
  - "people/first-last"
updated_at: "2026-08-13"
---
```

### Event (`events/YYYY-MM-DD-event-name.md`)
```yaml
---
type: event
id: 2026-10-12-ai-developer-summit
title: AI Developer Summit 2026
aliases: ["AI Dev Summit", "#AIDev2026"]
status: upcoming # upcoming | attending | speaking | completed | cancelled
tags: [conference, ai, devtools]
relations:
  - target: "companies/organizer-slug"
    type: "organizer"
  - target: "people/speaker-slug"
    type: "speaker"
start_date: "2026-10-12"
end_date: "2026-10-14"
location: "San Francisco, CA" # or "Virtual"
url: "https://example.com/event"
updated_at: "2026-08-14"
---
```

### Deal (`deals/company-round-year.md`)
```yaml
---
type: deal
id: acme-series-a-2026
title: Acme Corp Series A
aliases: []
status: closed # evaluating | term-sheet | closed | passed
tags: [venture-capital, series-a]
relations:
  - target: "companies/acme-corp"
    type: "target-company"
company: "companies/acme-corp"
stage: Series A
amount: "$15M"
lead_investor: "people/investor-name"
updated_at: "2026-08-13"
---
```

### Writing (`writing/title-or-topic.md`)
```yaml
---
type: writing
id: zero-database-knowledge-systems
title: Zero-Database Knowledge Systems for AI Agents
aliases: []
status: draft # idea | outline | draft | published
tags: [essays, architecture, ai-memory]
relations: []
updated_at: "2026-08-13"
---
```

---

## 6. Creating New Custom Domains

When creating a new custom entity directory (e.g., `BRAIN/hiring/` or `BRAIN/personal/`):
1. Create directory `BRAIN/<domain>/`.
2. Create `BRAIN/<domain>/README.md` defining:
   - Section 1: **What Goes Here**
   - Section 2: **What Does NOT Go Here**
   - Section 3: **Page Template** using the Universal Base Frontmatter Schema.
3. Add the new domain to `MECE_DIRS` in `scripts/lint.js`, `scripts/index.js`, `scripts/graph.js`, `scripts/stats.js`.
