# Agent Skills Directory Rules

The following rules apply to all AI agents operating within the `skills/` directory and its subdirectories. 

## 1. Skill Validation Rule
When checking or validating a skill, ensure its YAML frontmatter and folder structure strictly adheres to the accepted cross-platform formats:
- **agentskills.io Standard**: You must lazy-load and validate the frontmatter and folder structure against the standard defined at `https://agentskills.io`.
- **Hermes Agent Format**: Ensure the frontmatter satisfies the specific format accepted by Hermes Agents, as defined in their official documentation at `https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#skillmd-format`.

These controls must be done **only when explicitly requested by the user to "audit" or "validate" a skill**

## 2. Mandatory Frontmatter Metadata
In addition to the standard format requirements, every skill created or validated in this directory MUST contain the following fields in its `SKILL.md` YAML frontmatter. These are strictly enforced and should not be altered during creation:
- **`name`**: Name of the skill, a slug in kebab-case with the same name of the directory which contains the SKILL.md file.
- **`description`**: A brief description of the capability, and when to use it (a clear trigger condition (e.g. "Use this skill when the user asks to add, query, or remove a social event").
- **`author`**: Must be set to `Rainbowbreeze`.
- **`license`**: Must be set to `MIT`.
- **`version`**: The initial version of a skill must be explicitly set to `1.0.0`. Subsequent updates must follow semantic versioning:
  - **Patch Version (e.g., 1.1.0 -> 1.1.1)**: Increment the last number for minor textual updates or typo fixes in the skill instructions.
  - **Minor Version (e.g., 1.1.0 -> 1.2.0)**: Increment the middle number when there is a change in the logic, workflow, or behavior of the skill.
  - **Major Version (e.g., 1.2.0 -> 2.0.0)**: ONLY the user can decide to increment the major version (e.g., during a major refactor or complete logic overhaul). The agent must not increment the major version on its own.

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

## 5. Scripting & Code Quality Rules
When writing or maintaining Python or shell scripts within the `scripts/` folder of any skill:
- **Dependency Management First:** All Python scripts must be executable using `uv run --with <package>` to ensure they run in isolated environments without requiring global dependency installation. Do not assume packages are globally available.
- **Absolute Path Resolution:** Scripts must never use hardcoded absolute paths or rely on relative `../` paths for data storage. They must always read the storage location dynamically from the Environment Variables defined in the `SKILL.md` frontmatter (e.g., `os.environ.get("BRAIN_ROOT_PATH")`).
- **Graceful Error Handling:** Scripts should never fail silently. If a script encounters an error (e.g., missing file, network timeout), it must print a clear, human-readable error message to `stderr` so the agent can read the error and explain the problem to the user.
- **Standardized CLI Arguments:** All Python scripts must use the standard library `argparse` with clear `--help` descriptions. Positional arguments should be avoided in favor of explicit flags (e.g., `--title`, `--url`) to prevent the LLM from passing arguments in the wrong order.

## 6. Screen Formatting & Output Rules
When generating responses and interacting with the user on the screen:
- **Anti-Spam Link Previews:** Whenever an agent outputs a URL to a chat platform (like Discord or Slack), it MUST wrap the URL in angle brackets (e.g., `<https://example.com>`). This suppresses massive, unwanted link previews that clutter the screen.
- **The "Silent Cron" Rule:** If a skill is designed to run automatically (like a daily digest or fetcher) and it finds no new data, the agent MUST output exactly `[SILENT]` and nothing else. This prevents the agent from sending empty "I found nothing today!" messages to the user every day.

## 7. Prompt & Instruction Writing
When drafting the `SKILL.md` file instructions:
- **Explicit Trigger Conditions:** Every `SKILL.md` must have a `## Trigger` or `## When to use` section clearly defining the exact phrasing or context in which the LLM should invoke the skill.
- **Step-by-Step Determinism:** Complex operations must be broken down into numbered lists (e.g., 1. Check Duplicates, 2. Fetch Data, 3. Write File). Agents perform much more reliably when instructions are numbered rather than written as paragraphs.

## 8. Domain Consistency & Grouping
When creating or modifying multiple skills that belong to the same logical domain, they must adhere to the registered categories, shared variables, and assets below:

### Registered Categories
Skills could be assigned to one of these valid categories in their frontmatter:
- **`GAS`**: Skills managing the Gruppo Acquisto Solidale (`gas-agentmail`, `gas-process-updates`).

### Common Environment Variables
Skills within a specific group must tap into these registered environment variables:
- **`GAS`**:
  - `${BRAIN_ROOT_PATH}`: Root of the BRAIN knowledge base.
  - `${AGENTMAIL_GASTRONAUTI_API_KEY}`: API key for the GAS mailbox.

### Shared Assets & References
Skills must reference the existing central assets for their group instead of creating redundant definitions:
- **`GAS`** (Stored centrally in the `gas-process-updates` skill folder):
  - `assets/template-fornitore.md` and `assets/template-membro.md`: Templates for entities.
  - `references/brain-structure.md`: Detailed map of the GAS knowledge base.
  - `${BRAIN_ROOT_PATH}/bulletin/`: Folder containing the daily bulletins.

## 9. How to Add New Rules in the Future
To add new rules that apply globally to all skills in this folder, simply edit this `AGENTS.md` file and append the new rule in the most appropriate section.
