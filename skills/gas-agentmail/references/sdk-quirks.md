# AgentMail Python SDK Quirks

Technical lessons learned while using the `agentmail` SDK (v0.5.3+).

## Attribute Mappings
The `MessageItem` object does not use standard naming for sender fields:
- **WRONG**: `msg.from_email`, `msg.from_address`.
- **CORRECT**: `msg.from_` (this is a string representing the sender address).
- **Preview**: `msg.preview` contains a snippet of the content.
- **Full Text**: `msg.text` (only available when using `get()` on a message, not in `list()`).

## Response Objects
Methods like `client.inboxes.messages.list()` and `client.inboxes.list()` return a response object containing the list, not the list itself.
- **WRONG**: `messages = client.inboxes.messages.list(...)` -> `messages` is NOT iterable.
- **CORRECT**: `messages = client.inboxes.messages.list(...).messages` -> This is the iterable list.
- **Message ID**: The attribute is `message_id`, not `id`.

## Deletion Behavior
Thread deletion is not immediate or visible in the default list unless performed permanently.
- **Method**: `client.inboxes.threads.delete(inbox_id, thread_id, permanent=True)`
- **⚠️ PITFALL**: In some versions of the SDK (or for certain message types), `permanent=True` may raise a `TypeError: delete() got an unexpected keyword argument 'permanent'`. 
- **Workaround**: Implement a try/except block. Attempt with `permanent=True` first, and if a `TypeError` occurs, retry without it.
- **Note**: Omitting `permanent=True` (either by choice or due to the error above) may result in the thread still appearing in subsequent `list()` calls for a short period.

## Environment & Venv
The SDK must be installed via `uv pip install agentmail` and executed using the full path to the virtual environment python: `/opt/hermes/.venv/bin/python3`.
