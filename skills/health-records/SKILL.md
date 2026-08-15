---
name: health-records
description: "Management of the health record for family members: clinical picture, medical history, and reports."
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [health, medical, tracker, health reports, symptoms]
    category: health
    config:
      - key: BRAIN_HEALTHRECORDS_PATH
        description: "Path to store the health records files"
        default: "/opt/data/BRAIN/fascicolo-sanitario"
        prompt: "Where can I store the medical health records of your family?"
---

# Health Records Management

## When to activate this skill
Use this skill when the user provides medical information, lab reports (*referti di analisi*), photographic reports (*referti fotografici*), symptoms (*sintomi*), therapies (*terapie*), or health status updates (*salute*) for themselves or a family member.

## BRAIN Project Structure
The health record is located in `$BRAIN_HEALTHRECORDS_PATH/<first-last-name>/` (`<nome-cognome>`).
Each folder contains:
- `quadro_clinico.md`: Current snapshot of the health status (updated with the latest developments).
- `cronologia.md`: Sequential clinical diary (in reverse chronological order).
- `referti/`: Folder containing saved medical documents and images.

## Operative Procedure

1. **Saving Reports (if present):**
   - If the user provides a document or image, physically save it in the `referti/` folder of the relevant family member.
   - Naming convention: `YYYYMMDD-reportname.ext` (e.g., `20260715-emocromo.pdf`).
   - *Note:* The date `YYYYMMDD` must correspond to the date of the event/exam (read the date from the report, or EXIF metadata if indicated), not necessarily the date of entry.

2. **Updating Chronology (`cronologia.md`):**
   - Add an entry at the top of the event list.
   - Use this format:
     ```markdown
     ### DD Month YYYY - [Event/Exam Title]
     - **Summary:** [Summary of results or symptom]
     - **Report:** [If applicable, insert relative link: `[Report Name](referti/YYYYMMDD-name.ext)`]
     - **Action:** [If therapeutic changes or updates to the clinical picture were required]
     ```

3. **Updating Clinical Snapshot (`quadro_clinico.md`):**
   - Evaluate whether the new information modifies the overall clinical picture (e.g., newly discovered allergies, chronic conditions, vital parameters like cholesterol/blood pressure/weight, or new therapies).
   - If there is a change, directly edit the `quadro_clinico.md` file, overwriting older data while preserving the most recent values.
   - Always add a Markdown text link to the report that justifies the updated value.
