---
name: manage-projects
description: >-
  Use this skill when the user asks to list active projects, create a new project, archive an existing project, or append ideas, tasks, or updates to a project.
version: 1.2.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [project-management]
    category: rainbowskills
required_environment_variables:
  - name: BRAIN_PROJECTS_PATH
    prompt: Projects folder in the BRAIN knowledge repository 
    help: Define where the projects folder should be, generally /opt/data/BRAIN/projects
    required_for: full functionality
---

# Manage Projects

This skill handles the lifecycle of projects located at the path defined by the `$BRAIN_PROJECTS_PATH` environment variable.

## Language Convention
- All generated documentation, frontmatter, section headings, and notes inside project files must be written in **English**.
- **Exception (`## Logs` Section):** The `## Logs` audit section must record the exact sentence and prompt provided by the user in their **original language** without translation.

## Capability Bootstrapping
Before performing any operation, resolve the environment variable `$BRAIN_PROJECTS_PATH`. If `$BRAIN_PROJECTS_PATH` is not set or empty, explicitly ask the user for the path or to set `$BRAIN_PROJECTS_PATH` before continuing.

Once `$BRAIN_PROJECTS_PATH` is resolved, verify that the directory exists. If missing or uninitialized:
- Create `$BRAIN_PROJECTS_PATH/` and `$BRAIN_PROJECTS_PATH/archive/`.
- Initialize `$BRAIN_PROJECTS_PATH/projects.md` with the following skeleton if it does not exist:
  ```markdown
  # Projects Index

  | Project Slug | Status | Description | Project Folder |
  |---|---|---|---|
  ```

---

## Capabilities

### 1. List Active Projects
- Scan `$BRAIN_PROJECTS_PATH/`, excluding the `archive/` directory.
- Cross-reference folders with `$BRAIN_PROJECTS_PATH/projects.md` to provide a clear, formatted summary (e.g., Markdown table showing Project Slug, Status, Description, Project Folder, and Type).
- **Discrepancy Check:** Explicitly report any active project folders on disk that are missing from `projects.md`, or stale entries in `projects.md` that lack a corresponding folder.

### 2. Create a New Project
- **Prerequisite Gathering:** Before creating the project, ensure the user has provided ALL of the following information:
  1. Project Name
  2. Project Description
  3. Project Start Date (defaults to current date if omitted)
  4. Project Status (defaults to 'active')
  5. Project Type (e.g., blogpost, tutorial, school-activity, public-speaking, or other)
- If any essential information is missing, explicitly ask the user for the missing details and wait for their response. Do NOT create the project until all required fields are collected.
- **Slugification & Collision Check:**
  - Format the folder slug as `YYYYMM-project_slug` (lowercase, alphanumeric, spaces replaced with hyphens or underscores).
  - Verify that `$BRAIN_PROJECTS_PATH/<folder_name>` does not already exist. If it exists, alert the user.
- Create the directory: `$BRAIN_PROJECTS_PATH/<folder_name>`.
- Create the main markdown file (`README.md`) inside the new project folder with the following structure:
  ```markdown
  ---
  project_name: "[Name]"
  project_slug: "YYYYMM-project_slug"
  project_description: "[Description]"
  project_status: active
  project_type: "[Type]"
  project_start_date: "[YYYY-MM-DD]"
  project_target_date: "[YYYY-MM-DD]" # optional
  ---

  # [Name]

  [Description]

  ## Ideas

  ## Scope & Objectives

  ## Tasks & Next Steps

  ## Resources & References

  ## Logs
  - **[YYYY-MM-DD]**: [Exact sentence/prompt used by user to create the project in original language]
  ```
- **CRITICAL:** Update `$BRAIN_PROJECTS_PATH/projects.md` to register the new project in the table using a brief description (maximum one sentence):
  ```markdown
  | [YYYYMM-project_slug](./YYYYMM-project_slug/) | active | Brief project description (max 1 sentence) | ./YYYYMM-project_slug/ |
  ```

### 3. Archive a Project
- Move the target project folder from `$BRAIN_PROJECTS_PATH/<folder_name>` to `$BRAIN_PROJECTS_PATH/archive/<folder_name>`.
- Locate the project's `README.md`:
  - Update its YAML frontmatter to change `project_status` to `archived`.
  - Append an immutable entry to `## Logs`:
    `- **[YYYY-MM-DD]**: [Exact sentence/prompt used by user to archive the project in original language]`
- **CRITICAL:** Update `$BRAIN_PROJECTS_PATH/projects.md`:
  - Locate the row corresponding to the project in the table.
  - Update the `Status` column to `archived`.
  - Update the `Project Folder` column to `./archive/YYYYMM-project_slug/` while preserving the description:
    ```markdown
    | [YYYYMM-project_slug](./archive/YYYYMM-project_slug/) | archived | Brief project description (max 1 sentence) | ./archive/YYYYMM-project_slug/ |
    ```

### 4. Update an Existing Project
- **Project Selection:** If the user does not specify the exact folder path or slug when asking to append information, inspect `$BRAIN_PROJECTS_PATH/projects.md` and use the project slugs and brief descriptions to decide which project to target. If ambiguous or multiple projects fit the description, ask the user to clarify before proceeding.
- Locate the target project folder in `$BRAIN_PROJECTS_PATH/` (or `$BRAIN_PROJECTS_PATH/archive/` if archived).
- Target the project's main markdown file (`README.md`).
- Based on the user's request, append or update information in the appropriate section (written in English):
  - **Ideas:** Append bullet points under `## Ideas`.
  - **Scope & Objectives:** Update or append under `## Scope & Objectives`.
  - **Tasks:** Append or check off tasks under `## Tasks & Next Steps`.
  - **Resources:** Append links or references under `## Resources & References`.
- **Immutable Log Rule:** Whenever any project modification is made, append a new line to the `## Logs` section at the end of the file. This section is strictly append-only (never modify or delete existing log lines):
  ```markdown
  - **[YYYY-MM-DD]**: [Exact sentence/prompt provided by user in their original language without translation]
  ```
- **User Response Summary:** Once the project file is updated, provide a brief reply to the user summarizing the specific actions performed (e.g., new task added, idea logged or converted, milestone achieved, or status updated).