# Skills Repository

This repository contains a collection of the skills I created and my agents use, organized with one skill per subfolder. 

## Common Principles

Across all skills in this repository, the following design principles and conventions apply:
- **Centralized Knowledge Base (`BRAIN`)**: All skills that need to memorize or retrieve information rely on a common `BRAIN` folder. Inside this folder, information is organized into dedicated subfolders for each specific skill's domain.
- **Metadata Compatibility**: The `SKILL.md` frontmatter for every skill must be compatible with both the **AgentSkills.io** standard and the **Hermes Agent** specific format metadata.
- **Consistent Design**: The `AGENTS.md` file in this root folder enforces common design principles and conventions to ensure all skills are built and behave in a unified, consistent way.


## Available Skills

* **[aphorism-tracker](./aphorism-tracker/)**: Use to save text/image quotes or aphorisms to the BRAIN.
* **[collect-links](./collect-links/)**: Use this skill when the user provides one or more web links/URLs to store, save, bookmark, or summarize, or asks to save a link to the BRAIN links repository.
* **[events-manager](./events-manager/)**: Add, remove and query a list of events across different categories, like concerts, sports, social events, etc.
* **[events-report-pavia](./events-report-pavia/)**: Generates a structured daily report in Italian about upcoming events in Milan and Pavia using specific sources.
* **[gas-agentmail](./gas-agentmail/)**: Email management for the GAStronauti GAS via AgentMail. Allows reading, sending, and deleting emails from the gastronauti@agentmail.to inbox.
* **[gas-process-updates](./gas-process-updates/)**: Processes new GAS updates from emails, updates the BRAIN, deletes processed emails, and sends a summary on Discord.
* **[health-records](./health-records/)**: Management of the health record for family members: clinical picture, medical history, reports, medication reconciliation, and follow-ups.
* **[manage-projects](./manage-projects/)**: Use this skill when the user asks to list active projects, create a new project, archive an existing project, or append ideas, tasks, or updates to a project.
* **[news-report-pavia](./news-report-pavia/)**: Generates a structured daily report in Italian about Pavia city and its province using specific sources.
* **[personal-audio-diary](./personal-audio-diary/)**: Use when processing, correcting, and formatting voice note transcriptions for user's personal diary. Helps handle raw transcription errors, structure monthly log entries, and maintain durable facts.
* **[youtube-creators-summary](./youtube-creators-summary/)**: Use this skill when the user asks to generate a daily intelligence report of new YouTube videos from a specific list of technical and financial creators.

## Installation

To install these skills in Hermes Agent

Install the rainbowskills skills repo:
```bash
hermes skills tap add rainbowbreeze/rainbow-harness
```

Install the specific skill:
```bash
hermes skills install --category rainbowskills rainbowbreeze/rainbow-harness/health-records
```

Update all the skills if the version of the locally installed skill is lower than the version of the skill in this repo:
```bash
hermes skills update
```