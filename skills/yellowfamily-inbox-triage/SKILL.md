---
name: yellowfamily-inbox-triage
description: "Scans YellowFamily emails to distinguish between appointments (calendar events) and tasks (TODOs). Trigger this skill when the user asks to triage, check, or process the family emails or inbox."
version: 1.1.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: [google-gmail, reminders, calendar, archiving, autonomous, automation]
    config:
      - key: YELLOWFAMILY_CALENDAR_ID
        description: "Google Calendar ID for the Yellow Family"
        prompt: "What is the Calendar ID for the Yellow Family?"
---

# YellowFamily Inbox Triage

This skill automates the process of checking family emails to distinguish between appointments (calendar events) and tasks (TODOs).

## Dependencies
- Ensure the `google-workspace` skill is available.
- Ensure the `todos-manager` skill is available for managing tasks.

## Trigger
Use this skill when the user asks to "triage family emails", "check the YellowFamily inbox", "process new emails for the family", or when a cron job runs to triage the YellowFamily inbox automatically.

## Resources
- **Yellow Family Calendar ID**: `${YELLOWFAMILY_CALENDAR_ID}`

## Instructions

1. Use `google-workspace` to search for recent emails (`is:unread -label:Processed`).
   - **Pitfall**: Avoid starting a Gmail search query with `-` (e.g., `-label:Processed`) as the CLI wrapper may misinterpret it as a flag. Use `is:unread -label:Processed` or `in:inbox -label:Processed` instead.
2. Analyze the email content to classify it as an **Appointment** or a **Task**.
3. For every email analyzed:
   - Apply the label `Processed` to indicate it has been triaged.
   - Note: Triaged emails may still be marked as `UNREAD` in the inbox; always filter them out using `-label:Processed` to avoid re-processing.
4. If an item is identified:
   - **Appointments**: Create an event in the "Yellow family" Google Calendar. Label the email `Processed/Appointment`.
   - **Tasks**: Delegate task creation to the `todos-manager` skill. You must provide the following parameters to the skill:
     - `operation_mode`: `add`
     - `source`: `email`
     - `title`: A concise title extracted from the email subject or content.
     - `description`: Relevant details and context from the email body.
     - `due_date`: (Optional) The deadline in `YYYY-MM-DD` format, if one is specified in the email.
     After delegating, apply the Gmail label `Processed/Reminder` to the email.
     - **Exception**: Skip bills and invoices that are paid automatically via SDD (Direct Debit), Domiciliazione, or recurring credit card payments (e.g., Octopus Energy, TIM, utility bills, etc.). These do not require manual intervention and should not be added to the TODO list. Just label the email `Processed` and move on.
     - **Exception**: Skip informational receipts and order confirmations (e.g., "Ricevuta pagamento", "Conferma ordine").
     - **Exception**: Skip generic school newsletters or informational circulars (e.g., "Mailing classe", "Documento di valutazione", "Consigli di Classe"). Only create tasks for school emails if a clear manual action is demanded (e.g., "Sign and return", "Buy these specific books"). Do not create generic "Verify [Subject]" tasks for every email with an attachment.
     - **Exception**: Skip utility promotional or informational notices (e.g., Octopus Power Up free energy periods) unless they require manual account action.

## Pitfalls
- **CLI Label Modification**: When adding or removing multiple labels using `google_api.py gmail modify`, IDs must be comma-separated without spaces (e.g., `--add-labels ID1,ID2`). Providing them as separate arguments will cause a CLI error.
- **Empty Email Body**: Some automated emails (like those from school systems) may return an empty `body` via `google_api.py gmail get`. In these cases, rely on the `snippet` from the search result or check the message metadata.
- **Attachments**: Currently, the triage process cannot directly read PDF or image attachments. If an email indicates that crucial information (like a schedule) is in an attachment, create a "Verify [Subject]" task via the `todos-manager` rather than attempting to guess the details.
- **Search Verification**: If `is:unread -label:Processed` returns "No messages found", you can verify the labels of the most recent message using `gmail search "all" --max 1` to ensure the triage logic is working as expected.

## Cron Execution
When running as a scheduled job:
- If there are no new emails to triage, the final response must be exactly `[SILENT]` to suppress unnecessary delivery.

## Appointments Strategy
- **Multi-day Events**: For emails describing recurring or multi-day activities with consistent daily times (e.g., "Summer School 8:30-16:30, June 22-26"), create a separate calendar event for each day to ensure accuracy in daily agendas.
- **Timezones**: Always include the timezone offset (e.g., `+02:00` for CEST) in the ISO 8601 strings passed to `calendar create`.

## References
- `references/gmail-labels.md` — Specific Gmail Label IDs for the YellowFamily account.
