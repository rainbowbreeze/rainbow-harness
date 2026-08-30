---
name: todos-manager
description: Manage a shared to-do list for the Yellow Family. Use this skill when the user asks to add, remove, update, or query to-dos.
version: 1.1.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: [productivity, task-management]
    category: rainbowskills
    config:
      - key: BRAIN_TODOSDB_PATH
        description: "Path to store the to-do list files"
        default: "/opt/data/BRAIN/todos-db"
        prompt: "Where can I store the list of to-dos?"
---

# Todos Manager

This skill governs how to manage, update, query, and remove to-do items.

## Core Principles
1. **Strict Deduplication:** Always rely on the python script to parse the existing dataset and check against existing to-do slugs before appending new discoveries.
2. **Completion by Removal:** To-dos do not have a "status" field. If a to-do is in the file, it must be done. When you are asked to mark a to-do as completed or done, you must remove it from the database.
3. **Data Consistency:** All to-dos must have a strict JSON schema including `slug`, `title`, `description`, and `source` (`email`, `user-command`, `unknown`).

## Invocation Parameters

When the skill is invoked, the caller MUST provide the following base parameters:
- **operation_mode** (Mandatory): Must be one of `add`, `remove`, `update`, or `query`.

Depending on the `operation_mode`, the caller must also provide specific parameters (detailed below). **If any required parameters are missing for the requested mode, you MUST immediately return an error to the caller detailing exactly which parameters are missing.**

## Operation Modes & Usage

This skill includes a dedicated Python CLI located at `scripts/todos_manager.py`. **Do not attempt to read, write, or modify the JSON files manually.** Always execute this script to perform operations.

> [!IMPORTANT]
> Because you might be invoked from anywhere in the workspace (e.g. the project root), **always dynamically resolve the absolute path** to `scripts/todos_manager.py` before running it.

### 1. Add a To-Do (`operation_mode: add`)
When called to add a to-do, the caller MUST provide:
- `title`
- `description`
- `source` (Must be one of: `email`, `user-command`, `unknown`)

Optional parameters:
- `due_date` (Format: YYYY-MM-DD)

Pass these parameters to the script's `add` command:
```bash
${SCRIPT_PATH} add \
    --title "Buy groceries" \
    --description "Milk, bread, and eggs" \
    --source "user-command" \
    --due-date "2026-09-01"
```

### 2. Remove / Complete a To-Do (`operation_mode: remove`)
When called to complete or remove a to-do, the caller MUST provide:
- `slug` of the to-do.

Pass this parameter to the script's `remove` command:
```bash
${SCRIPT_PATH} remove --slug "20260830-buy-groceries"
```

### 3. Update a To-Do (`operation_mode: update`)
When called to update an existing to-do, the caller MUST provide:
- `slug` of the to-do to update.

And at least one of the fields to update (`--title`, `--description`, `--due-date`, `--source`). To clear an optional field, provide an empty string.

```bash
${SCRIPT_PATH} update --slug "20260830-buy-groceries" --title "Buy more groceries"
```

### 4. Query To-Dos (`operation_mode: query`)
When called to query to-dos, the caller can provide optional filters:
- `source`

```bash
${SCRIPT_PATH} query --source "user-command"
```

## Supported Format

All to-dos are stored as a JSON array relative to the `${BRAIN_TODOSDB_PATH}` environment variable.

- **Active File Pattern**: `${BRAIN_TODOSDB_PATH}/todos.json`
- **Format**: JSON Array of Objects managed entirely by `scripts/todos_manager.py`.
```json
[
  {
    "slug": "20260830-buy-groceries",
    "title": "Buy groceries",
    "description": "Milk, bread, and eggs",
    "source": "user-command",
    "due_date": "2026-09-01"
  }
]
```
