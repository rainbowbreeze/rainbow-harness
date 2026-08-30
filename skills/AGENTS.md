# Agent Skills Directory Rules

The following rules apply to all AI agents operating within the `skills/` directory and its subdirectories. 

## 1. Skill Validation Rule
When checking or validating a skill, ensure its YAML frontmatter and folder structure strictly adheres to the accepted cross-platform formats:
- **agentskills.io Standard**: You must lazy-load and validate the frontmatter and folder structure against the standard defined at `https://agentskills.io`.
- **Hermes Agent Format**: Ensure the frontmatter satisfies the specific format accepted by Hermes Agents, as defined in their official documentation at `https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#skillmd-format`.

These controls must be done **only when explicitly requested by the user to "audit" or "validate" a skill**

## 2. Mandatory Frontmatter Metadata
In addition to the standard format requirements, every skill created or validated in this directory MUST contain the following fields in its `SKILL.md` YAML frontmatter. These are strictly enforced and should not be altered during creation:
- **`name`**: Name of the skill, a slug in camel-case with the same name of the directory which contains the SKILL.md file.
- **`description`**: A brief description of the capability, and when to use it (a clear trigger condition (e.g. "Use this skill when the user asks to add, query, or remove a social event").
- **`author`**: Must be set to `Rainbowbreeze`.
- **`license`**: Must be set to `MIT`.
- **`version`**: The initial version of a skill must be explicitly set to `1.0.0`.

## 3. New Skill Creation Process
When a user asks to create a new skill, you must follow this process:
1. **Query the User**: First, explicitly ask the user what the skill should do. 
2. **Propose the Metadata**: Based on their reply, propose a skill name (formatted as a valid skill slug, e.g., `my-new-skill`) and a carefully crafted `description`. The description must clearly state what the skill does and exactly when it should be triggered. Do not create the files until the user approves the proposed name and description.
3. **Propose the Implementation**: After the name and description are approved, propose a directory structure (e.g., `scripts/`, `assets/`) and a step-by-step implementation plan. Wait for a second round of approval before writing any files.

## 4. Environment Variables
When referencing or utilizing environment variables within scripts, markdown instructions, or configurations, every environmental variable MUST be enclosed in curly braces (graph parentheses), for example: `${BRAIN_ROOT}`.

Furthermore, every environmental variable present in the `SKILL.md` and any associated files in the skill's folder MUST be declared in the frontmatter using the Hermes frontmatter format.

Example of how to declare variables:
```yaml
metadata:
  hermes:
    config:
      - key: BRAIN_HEALTHRECORDS_PATH
        description: "Path to store the health records files"
        default: "/opt/data/BRAIN/fascicolo-sanitario"
        prompt: "Where can I store the medical health records of your family?"
```

## 5. How to Add New Rules in the Future
To add new rules that apply globally to all skills in this folder, simply edit this `AGENTS.md` file and append the new rule in the most appropriate section.
