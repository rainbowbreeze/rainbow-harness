---
name: collect-links
description: >-
  Use this skill when the user provides one or more web links/URLs to store, save, bookmark, or summarize, or asks to save a link to the BRAIN links repository.
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [links, bookmarks, knowledge-capture, summary, deduplication, projects]
    category: rainbowskills
required_environment_variables:
  - name: BRAIN_LINKS_PATH
    prompt: Links folder in the BRAIN knowledge repository
    help: Define where the links folder should be located, e.g., /opt/data/BRAIN/links or ${WORKSPACE_ROOT}/rainbow-llm-wiki/BRAIN/links
    required_for: full functionality
---

# Collect Links (`collect-links`)

This skill handles saving, inspecting, summarizing, deduplicating, project-associating, and indexing user-provided URLs in the directory specified by `${BRAIN_LINKS_PATH}`.

## Capability Bootstrapping

1. **Resolve `${BRAIN_LINKS_PATH}`**:
   - Check if the environment variable `${BRAIN_LINKS_PATH}` is set and non-empty.
   - If missing or uninitialized, explicitly ask the user for the path or ask them to set `${BRAIN_LINKS_PATH}` before continuing. Do NOT proceed until the path is resolved.

2. **Directory & Index Initialization**:
   - Verify that `${BRAIN_LINKS_PATH}/` exists. If not, create `${BRAIN_LINKS_PATH}/` and `${BRAIN_LINKS_PATH}/summaries/`.
   - Ensure `${BRAIN_LINKS_PATH}/links.md` exists. If it does not exist, initialize it with the following skeleton:
     ```markdown
     # BRAIN Saved Links & Summaries

     An append-only repository of stored web links, bookmarks, and their detailed summaries.

     ## Links
     ```

---

## Capabilities & Workflow Steps

When the user provides one or more web links or URLs to store:

### 1. Deduplication Check & Web Content Extraction
- **Deduplication Check**:
  - Before fetching or storing a new link, inspect `${BRAIN_LINKS_PATH}/links.md` and existing files in `${BRAIN_LINKS_PATH}/summaries/` to verify that the URL is **not duplicated**.
  - If the URL is already stored, notify the user immediately with the link to the existing summary page and ask whether they want to update/enrich the existing summary or cancel.
- **Extract & Fetch Web Content**:
  - If not duplicated, extract the URL(s) from the user's request.
  - Use your web reading / content fetching tool (`read_url_content` or equivalent HTTP/browser tool) to fetch the HTML content, text, title, and metadata of the target URL.
  - **Fallback Handling**: If fetching the URL fails (e.g., paywall, 403 Forbidden, bot protection, or JavaScript-heavy site without tool support), inspect the URL structure and ask the user for a brief page title or key context so the link can still be stored cleanly.

### 2. Interactive Project Association (`manage-projects` Query)
- **Ask for Project Association**: Explicitly ask the user if the link should be added/associated to a specific project in their BRAIN repository.
- **Query Active Projects**:
  - If the user confirms they want to associate the link to a project, **and they do not explicitly provide the project name**, invoke/query the existing active projects using the `manage-projects` skill (`List Active Projects` capability) and present the formatted list of active projects to the user.
  - Wait for the user to specify one or more projects from the list (or provide project names).
- **Collect Specified Projects**: Store the list of associated projects to be included in the YAML frontmatter (`projects: [...]`) and master index entry.

### 3. Generate Link Summary (`${BRAIN_LINKS_PATH}/summaries/YYYYMMDD-link-slug.md`)
- **CRITICAL - English Language Mandate**: Regardless of the source language of the fetched web link/URL (e.g., Italian, Spanish, German, Japanese, etc.), **the summary, page title, and generated slug MUST be written in English**. Translate all takeaways, notes, and metadata to English.
- **Generate Date & Slug**:
  - Format the current local date as `YYYYMMDD` (8 digits without hyphens, e.g., `20260815`).
  - Generate a clean, lowercase alphanumeric slug `link-slug` in English derived from the translated page title or subject, replacing spaces and special characters with hyphens `-` (e.g., `deepmind-agentic-coding`).
  - Target summary path: `${BRAIN_LINKS_PATH}/summaries/YYYYMMDD-<link-slug>.md`.
  - If a file with this exact filename already exists, alert the user or append a suffix (`-1`, `-2`) to prevent accidental overwrite unless asked to re-summarize.
- **Write Structured Summary (in English)**:
  - Create the summary file at `${BRAIN_LINKS_PATH}/summaries/YYYYMMDD-<link-slug>.md` using the YAML frontmatter (including `projects` if specified) and section structure below:
    ```markdown
    ---
    type: "link"
    id: "YYYYMMDD-<link-slug>"
    title: "<Human Readable Page Title>"
    source_url: "<URL>"
    tags: ["<tag1>", "<tag2>"]
    projects: ["<project1>", "<project2>"]
    ---

    # <Human Readable Page Title>

    - **Source URL**: [<URL>](<URL>)
    - **Saved On**: YYYY-MM-DD
    - **Associated Projects**: <Project 1>, <Project 2>

    ## Overview / Executive Summary
    <Concise 2-3 sentence overview of the article, resource, or tool>

    ## Key Takeaways
    - **<Takeaway 1>**: <Details>
    - **<Takeaway 2>**: <Details>
    - **<Takeaway 3>**: <Details>

    ## Detailed Notes & Highlights
    <Structured breakdown of the core ideas, methods, or arguments presented in the link>

    ## Actionable Quotes / Reference Snippets
    > "<Relevant quote or code snippet extracted from page>"
    ```

### 4. Append Entry to Master Index (`${BRAIN_LINKS_PATH}/links.md`)
- Locate `${BRAIN_LINKS_PATH}/links.md`.
- Append a bullet item for the stored link directly under the `## Links` section (or at the end of the existing bullet list under `## Links`), including project associations if present:
  ```markdown
  - **[YYYY-MM-DD]** [Title of Page](./summaries/YYYYMMDD-<link-slug>.md) — Source: [<URL>](<URL>) | Tags: `#tag1`, `#tag2` | Projects: `Project 1`, `Project 2`
  ```

### 5. Confirm & Report
- Provide the user with a rich confirmation report showing:
  - **Page Title & URL**
  - **Created Summary File**: `${BRAIN_LINKS_PATH}/summaries/YYYYMMDD-<link-slug>.md`
  - **Tags & Associated Projects**
  - **Executive Takeaway**: A concise summary of the link's primary message or utility.
  - **Structured Breakdown**: The core ideas, methods, arguments, or technical highlights presented in the link (mirroring the `## Detailed Notes & Highlights` section).
