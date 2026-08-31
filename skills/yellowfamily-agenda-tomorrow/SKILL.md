---
name: yellowfamily-agenda-tomorrow
description: "Generates the daily agenda for the YellowFamily, consolidating calendar events and BRAIN TODOs. Use this skill when the user asks for tomorrow's agenda, schedule, or upcoming tasks for the family."
version: 1.1.0
author: Rainbowbreeze
license: MIT
category: yellowfamily
metadata:
  hermes:
    tags: [yellowfamily, agenda, calendar, todo]
    config:
      - key: YELLOWFAMILY_CALENDAR_ID
        description: "Calendar ID for Yellow Family events"
        default: "ADD_ME"
        prompt: "What is the Calendar ID for the Yellow Family?"
---

# YellowFamily Agenda Generation

Formalized workflow for producing the daily family agenda.

## Trigger
Use this skill when the user explicitly requests to see tomorrow's agenda, schedule, upcoming tasks, or calendar events for the YellowFamily.

## Resources
- **Yellow Family Calendar ID:** `${YELLOWFAMILY_CALENDAR_ID}`

## Workflow
1. **Fetch Calendar Events:** 
   - Use `google-workspace` to fetch events for the target day.
   - **Crucial:** Always specify the `--calendar` flag with the `${YELLOWFAMILY_CALENDAR_ID}`.
2. **Read Active TODOs:** 
   - Delegate to the `todos-manager` skill to retrieve tasks.
   - Invoke `todos-manager` with `operation_mode: query`.
   - Identify:
     - **Urgent/Overdue:** Items with dates in the past.
     - **Short-term Upcoming:** Items due today, tomorrow, or within the next 3 days. Ignore TODOs further out to keep the report concise.
3. **Consolidate and Report:**
   - Write the report in **Italian** using an ultra-minimalist format.
   - Omit entirely any section that is empty (e.g., if no calendar events, do not print the "🗓️ Eventi in Calendario" header).
   - For TODOs, strip out extra table data (creation date, source). Only show the essentials: Action, Owner, and a brief deadline note (e.g., "🚗 **Rinnovare assicurazione auto** (*Mamma* - Scade domani!)").
   - Use the following sections *only if they have content*:
     - `🗓️ Eventi in Calendario`
     - `⚠️ Scadenze Urgenti e Arretrati`
     - `📝 Prossime Scadenze (3 giorni)`
     - `💡 Nota del Maggiordomo` (Include ONLY if there are critical warnings, like scheduling conflicts. Do not add general tips, greetings, or fluff).

## Pitfalls
- **Default Calendar:** The account's primary calendar is often empty; the family uses the shared "Yellow family" calendar.
- **Date Format:** Ensure the ISO 8601 strings for `google-workspace` are correct (e.g., `YYYY-MM-DDT00:00:00Z`).
- **Omit Empty Sections:** Do not write "Nessun appuntamento" or "Nessuna scadenza". Simply skip the section entirely to keep the report short.