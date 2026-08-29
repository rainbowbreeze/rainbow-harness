---
name: events-report-pavia
description: Generates a structured daily report in Italian about upcoming events in Milan and Pavia using specific sources.
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [journalism, news, events]
    category: rainbowskills
---


# Events Report Pavia Skill

This skill automates the generation of a daily report in Italian covering upcoming events in Milan and Pavia.

## Sources

### Events (Pavia & Milan)
- **Source List**: See `assets/event-sources.json` for the complete list of event websites and their respective RSS feeds.

## Core Execution Workflow

1. **Prerequisite Check - Local Events Manager**:
   - Before starting any extraction, verify that the `local-events-manager` skill is available.
   - If the skill is missing or unavailable, immediately stop execution and report that the required skill is missing and event retrieval cannot be performed.

2. **Information Gathering & Storage - Events**:
   - Search in the event platforms listed in `assets/event-sources.json` for events occurring in the Province of Pavia and the Metropolitan City of Milan over the next 30 days.
   - Extract: Live URL, Event Name, Precise Location, Date/Time, Description, and Additional Info.
   - **MANDATORY**: Use the `local-events-manager` skill to add *every* newly discovered event into the database (`BRAIN/pavia-events/events_pavia.md`). The manager handles deduplication and updates.

3. **Output Structure & Tone (STRICTLY ITALIAN)**:
   - **Language**: Strictly Italian.
   - **Tone**: Professional and journalistic. Focus on clarity, objectivity, and precision.
   - **Link Previews**: Wrap all URLs in angle brackets (e.g., `<https://.../>`) to prevent Discord from showing link previews.
   - **Format**:
     - **Section 1: Newly Discovered Events**:
       - Mention strictly the new events found during today's scrape that were just added to the database.
       - Format: Unordered bullet list with only `Title`, `Date`, and `URL`.
     - **Section 2: Upcoming 15-Day Agenda**:
       - Instead of just showing scraped events, query the `local-events-manager` (i.e., read `BRAIN/pavia-events/events_pavia.md`) for **ALL** recorded events scheduled in the next 15 days.
       - Format: Unordered list with `Event Title`, `Event Date`, `Event Location`, `Event URL`, `Event Description`.

- **Delivery Instructions**:
  - Provide the structured report directly as your final response to be delivered to the destination specified in the job context.

## Pitfalls & Resilience

- **Cron Delivery & Silent Mode**: When running as a cron job, suppress delivery by responding with exactly `[SILENT]` if no new information is found.
