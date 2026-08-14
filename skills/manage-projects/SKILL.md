---
name: manage-projects
description: >-
  Use this skill when the user asks to list active projects, create a new project, archive an existing project, or append ideas or execution log entries to a project in BRAIN.
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [project-management]
    category: rainbowskills
---

# Manage Projects

This skill handles the lifecycle of projects in the fixed directory `/opt/data/BRAIN/projects/`.

## Capability Bootstrapping
Before performing any operation, verify that `/opt/data/BRAIN/projects/` exists. If missing or uninitialized:
- Create `/opt/data/BRAIN/projects/` and `/opt/data/BRAIN/projects/archive/`.
- Initialize `/opt/data/BRAIN/projects/AGENTS.md` with the following skeleton if it does not exist:
  ```markdown
  # BRAIN Projects Index

  ## Contents
  ```

---

## Capabilities

### 1. List Active Projects
- Scan `/opt/data/BRAIN/projects/`, excluding the `archive/` directory.
- Cross-reference folders with `/opt/data/BRAIN/projects/AGENTS.md` to provide a clear, formatted summary (e.g., Markdown table showing Project Name, Folder, Status, Type, and Description).
- **Discrepancy Check:** Explicitly report any active project folders on disk that are missing from `AGENTS.md`, or stale entries in `AGENTS.md` that lack a corresponding folder.

### 2. Create a New Project
- **Prerequisite Gathering:** Before creating the project, ensure the user has provided ALL of the following information:
  1. Project Name
  2. Project Description
  3. Project Start Date
  4. Project Status (defaults to 'active')
  5. Project Type (e.g., blogpost, tutorial, school-activity, public-speaking, or other)
- If any information is missing, explicitly ask the user for the missing details and wait for their response. Do NOT create the project until all fields are collected.
- **Slugification & Collision Check:**
  - Format the folder slug as `YYYYMM-project_slug` (lowercase, alphanumeric, spaces replaced with hyphens or underscores).
  - Verify that `/opt/data/BRAIN/projects/<folder_name>` does not already exist. If it exists, alert the user.
- Create the directory: `/opt/data/BRAIN/projects/<folder_name>`.
- Create the main markdown file (`README.md`) inside the new project folder containing YAML frontmatter and default log sections:
  ```markdown
  ---
  project_name: "[Name]"
  project_description: "[Description]"
  project_start_date: "[Date]"
  project_status: active
  project_type: "[Type]"
  ---

  # [Name]

  [Description]

  ## Ideas

  ## Execution Log
  ```
- **CRITICAL:** Update `/opt/data/BRAIN/projects/AGENTS.md` to register the new folder under the `## Contents` section using the format:
  ```markdown
  - [Project Name](./YYYYMM-project_slug/): Project Description
  ```

### 3. Archive a Project
- Move the target project folder from `/opt/data/BRAIN/projects/<folder_name>` to `/opt/data/BRAIN/projects/archive/<folder_name>`.
- Locate the project's `README.md` and update its YAML frontmatter to change `project_status` to `archived`.
- **CRITICAL:** Update `/opt/data/BRAIN/projects/AGENTS.md`:
  - Remove the project entry from the `## Contents` section.
  - Append the project entry under the `## Archived Projects` section (create the heading if it does not exist) using the format:
    ```markdown
    - [Project Name](./archive/YYYYMM-project_slug/): Project Description
    ```

### 4. Update an Existing Project
- Locate the target project folder in `/opt/data/BRAIN/projects/`.
- Target the project's main markdown file (`README.md`).
- Based on the user's request, append the information to the appropriate section, creating the header (`## Ideas` or `## Execution Log`) if it does not already exist:
  - For new ideas/concepts: Append as a bullet point under the `## Ideas` section.
  - For execution steps/progress: Append as a bullet point under the `## Execution Log` section, prefixed with the current date (e.g., `- **[YYYY-MM-DD]**: [Step description]`).