---
name: manage-projects
description: Manage BRAIN active and archived projects.
version: 1.0.0
trigger: Use when user wants to list, create, update, or archive a project.
---
# Manage Projects

This skill handles the lifecycle of projects in the `/opt/data/BRAIN/projects/` directory.

## Capabilities

### 1. List Active Projects
- Scan `/opt/data/BRAIN/projects/`, excluding the `archive/` directory.
- Cross-reference with `/opt/data/BRAIN/projects/AGENTS.md` to provide a list of active projects along with their brief descriptions.

### 2. Create a New Project
- **Prerequisite Gathering:** Before creating the project, ensure the user has provided ALL of the following information:
 1. Project Name
 2. Project Description
 3. Project Start Date
 4. Project Status (defaults to 'active')
 5. Project Type (e.g., blogpost, tutorial, school-activity, public-speaking, or other)
- If any information is missing, explicitly ask the user for the missing details and wait for their response. Do NOT create the project until all fields are collected.
- Format the folder name as `YYYYMM-project_name` (e.g., `202608-new_tutorial`).
- Create the directory: `/opt/data/BRAIN/projects/<folder_name>`.
- Initialize an `AGENTS.md` inside the new folder.
- Create a project-specific markdown file (e.g., `README.md`) inside the new project folder containing YAML frontmatter with the gathered details:
 ```yaml
 ---
 project_name: "[Name]"
 project_description: "[Description]"
 project_start_date: "[Date]"
 project_status: active
 project_type: "[Type]"
 ---
 ```
- **CRITICAL:** Update `/opt/data/BRAIN/projects/AGENTS.md` to register the new folder and its description in the `## Contents` section.

### 3. Archive a Project
- Move the target project folder from `/opt/data/BRAIN/projects/<folder_name>` to `/opt/data/BRAIN/projects/archive/<folder_name>`.
- Update the project-specific markdown file's frontmatter to change `project_status` to `archived`.
- **CRITICAL:** Update `/opt/data/BRAIN/projects/AGENTS.md` to reflect that this folder has been moved from the active list to the archive.

### 4. Update an Existing Project
- Locate the target project folder in `/opt/data/BRAIN/projects/`.
- Target the project's main markdown file (e.g., `README.md`).
- Based on the user's request, append the information to the appropriate section, creating the header if it does not already exist:
 - For new ideas/concepts: Append as a bullet point under the `## Ideas` section.
 - For execution steps/progress: Append as a bullet point under the `## Execution Log` section, prefixed with the current date (e.g., `- **[YYYY-MM-DD]**: [Step description]`).