---
name: events-manager
description: Add, remove and query a list of events across different categories, like concerts, sports, social events, etc.
version: 1.3.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: [journalism, news, events]
    category: rainbowskills
required_environment_variables:
  - name: BRAIN_EVENTSDB_PATH
    prompt: Folder to store events in the BRAIN knowledge repository 
    help: Define where the event database stores data, generally /opt/data/BRAIN/events-db
    required_for: full functionality
---



# Local Events Manager

This skill governs how you manage, update, query, and deduplicate local event datasets for various geographic regions.

## Core Principles
1. **Strict Deduplication:** Always parse the existing dataset and check against existing event slugs and URLs before appending new discoveries.

## Invocation Parameters

When the skill is invoked, the caller MUST provide the following base parameters:
- **operation_mode** (Mandatory): Must be one of `add`, `remove`, `query`, or `archive`.
- **event_category** (Mandatory): Controls the sub-directory where the event files are saved. If no category is specified by the caller, fallback to using `default`.

Depending on the `operation_mode`, the caller must also provide specific parameters (detailed below). **If any required parameters are missing for the requested mode, you MUST immediately return an error to the caller detailing exactly which parameters are missing, so they understand what is required.**

## Operation Modes & Usage

This skill includes a dedicated Python CLI located at `scripts/events_manager.py`. **Do not attempt to read, write, or modify the JSON event files manually.** Always execute this script to perform operations, as it safely handles slug generation, strict deduplication, and overlapping date queries.

> [!IMPORTANT]
> Because you might be invoked from anywhere in the workspace (e.g. the project root), **always dynamically resolve the absolute path** to `scripts/events_manager.py` before running it, rather than blindly copying the relative path examples below. 

### 1. Add an Event (`operation_mode: add`)
When called to add an event, the caller MUST provide the following parameters:
- `title`
- `start_date` (Format: YYYY-MM-DD)
- `end_date` (Format: YYYY-MM-DD)
- `description`
- `url`
- `location`

Pass these parameters to the script's `add` command:
```bash
$SCRIPT_PATH --category <event_category> add \
    --title "Event Title" \
    --start-date "YYYY-MM-DD" \
    --end-date "YYYY-MM-DD" \
    --description "Description" \
    --url "URL" \
    --location "Venue"
```
- **Output Handling**: If the script fails (e.g., duplicate found), return the error to the calling flow. If it succeeds, return the confirmation and the newly generated slug.

### 2. Remove an Existing Event (`operation_mode: remove`)
When called to remove an event, the caller MUST provide either:
- The `slug` of the event directly.

OR BOTH:
- The `title` of the event.
- The `start_date` of the event (so the slug can be derived).

Pass these parameters to the script's `remove` command:
```bash
# Using slug:
$SCRIPT_PATH --category <event_category> remove --slug "event-slug"

# Using title and start date:
$SCRIPT_PATH --category <event_category> remove --title "Event Title" --start-date "YYYY-MM-DD"
```

### 3. Query the List of Events (`operation_mode: query`)
When called to query events, the caller MUST provide the following parameters:
- `start_date` (Format: YYYY-MM-DD)
- `end_date` (Format: YYYY-MM-DD)

Pass these parameters to the script's `query` command. It will output a JSON array of all events that intersect or overlap with the range.
```bash
$SCRIPT_PATH --category <event_category> query --start-date "YYYY-MM-DD" --end-date "YYYY-MM-DD"
```

### 4. Archive Events (`operation_mode: archive`)
When called to archive past events, the caller MUST provide the following parameter:
- `before_date` (Format: YYYY-MM-DD)

Pass this parameter to the script's `archive` command. The script will find all events that ended before this date, remove them from the active file, and append them to the `events_archive.json` file.
```bash
$SCRIPT_PATH --category <event_category> archive --before-date "YYYY-MM-DD"
```

## Supported Format

All events are stored as JSON datasets relative to the `${BRAIN_EVENTSDB_PATH}` environment variable and the specific `event_category`. Markdown formats are not supported.

- **Active File Pattern**: `${BRAIN_EVENTSDB_PATH}/<event_category>/events.json`
- **Archive File Pattern**: `${BRAIN_EVENTSDB_PATH}/<event_category>/events_archive.json`
- **Format**: JSON Array of Objects managed entirely by `scripts/events_manager.py`.
```json
[
  {
    "slug": "20260829-event-title",
    "titolo": "Event Title",
    "data_inizio": "YYYY-MM-DD",
    "data_fine": "YYYY-MM-DD",
    "luogo": "Venue/Location",
    "descrizione": "Description",
    "fonte_url": "URL"
  }
]
```
