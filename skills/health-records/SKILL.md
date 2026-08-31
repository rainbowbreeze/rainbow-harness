---
name: health-records
description: "Management of the health record for family members: clinical picture, medical history, reports, medication reconciliation, and follow-ups."
version: 1.2.2
author: Rainbowbreeze
metadata:
  hermes:
    tags: [health, medical, tracker, reports, symptoms, medications]
    category: health
required_environment_variables:
  - name: BRAIN_HEALTHRECORDS_PATH
    prompt: Where can I store the medical health records of your family?
    help: Path to store the health records files
    required_for: full functionality
---

# Health Records Management

## Language & Localization Policy
> [!IMPORTANT]
> **Preserve Input & Document Language:**
> Despite this `SKILL.md` file being written in English for system compatibility, **the content must be managed in the language of the user's input or the uploaded document**.
> Specifically, if a document or report is in Italian, **all notes, headings, table summaries, and modifications to the files inside the `${BRAIN_HEALTHRECORDS_PATH}` folder must be written in Italian** (e.g., *Quadro Clinico*, *Cronologia*, *Referto*, *Sintesi*, *Azione Richiesta*, *Scadenze e Promemoria*, *Farmaci Attivi*). Never force-translate Italian health reports or clinical notes into English when writing to disk.

## When to activate this skill
Use this skill when the user provides medical information, lab reports (*referti di analisi*), photographic reports (*referti fotografici*), symptoms (*sintomi*), therapies/medications (*terapie*), follow-up schedules, or general health status updates (*salute*) for themselves or any family member.

---

## 1. Family Member Alias & Relationship Resolution
Before modifying any files, explicitly verify **which family member** the input pertains to:
- **Canonical Folder Naming:** Every family member has a folder in lowercase hyphen-separated format: `${BRAIN_HEALTHRECORDS_PATH}/<first-last-name>/` (e.g., `mario-rossi`).
- **Alias & Relationship Mapping:**
  - If the user refers to pronouns or relationships (e.g., *"my wife"*, *"my son Sofia"*, *"my lab results"*), map the entity to their canonical `<first-last-name>` directory.
  - **Ambiguity Rule:** If the subject is ambiguous or omitted (e.g., *"Add this blood pressure reading: 130/80"* when multiple family profiles exist), **ask the user for confirmation** before inserting or overwriting clinical data.

---

## 2. BRAIN Project Structure
Each family member's health dossier adheres to the following structure:
```text
${BRAIN_HEALTHRECORDS_PATH}/<first-last-name>/
├── quadro_clinico.md                         <-- Current clinical snapshot, active/discontinued meds, follow-ups
├── cronologia.md                             <-- Sequential clinical diary (reverse chronological order)
└── referti/                                  <-- Folder for physical documents, images, and structured summaries
    ├── 20260715-emocromo.pdf                 <-- Raw uploaded medical report / scan
    └── 20260715-emocromo.summary.md          <-- Extracted structured summary & lab tables (OCR / transcript)
```

---

## 3. Operative Procedure

> [!IMPORTANT]
> **Language & Localization Rule:**
> Although this skill specification (`SKILL.md`) is written in English for system consistency, **all dossier files, notes, summaries, and updates inside `${BRAIN_HEALTHRECORDS_PATH}` must be managed in the language of the input document or user conversation**.
> For example, if a report is in Italian or the user speaks Italian, all content written to `quadro_clinico.md`, `cronologia.md`, and `referti/*.summary.md`—including headings, notes, lab summaries, and follow-up reminders—**must be written in Italian** (e.g., *Sintesi*, *Referto*, *Azione Richiesta*, *Scadenze e Promemoria*, *Farmaci Attivi*, *Farmaci Sospesi*). Never force-translate Italian health records or lab summaries into English.

When processing a health update or uploaded document, execute the following steps sequentially:

### Step 1: Saving Reports & Companion Summaries (`referti/`)
- **Save Raw Asset:** If a document or image is uploaded, save it physically inside `referti/`.
- **Strict Naming Convention:** `YYYYMMDD-reportname.ext` (e.g., `20260715-emocromo.pdf`).
  - *Timestamp Rule:* `YYYYMMDD` **must** be the actual date the exam, test, or event occurred (read from the report text or EXIF metadata), NOT the date of file upload.
- **Generate Companion Structured Summary (`.summary.md`):**
  - Whenever a lab report or medical document is ingested, create a companion Markdown file in `referti/` named `YYYYMMDD-reportname.summary.md`.
  - Extract all structured quantitative data into a standardized table format so values are permanently searchable and verifiable:
    ```markdown
    # Summary: [Report Title] (Date: YYYY-MM-DD)
    - **Facility / Doctor:** [Name]
    - **Clinical Conclusion:** [Brief summary of findings]

    ### Extracted Lab Biomarkers
    | Metric | Observed Value | Unit | Reference Range | Status |
    | :--- | :--- | :--- | :--- | :--- |
    | Hemoglobin | 13.8 | g/dL | 13.0 - 17.5 | NORMAL |
    | LDL Cholesterol | 165 | mg/dL | < 115 | **HIGH** |
    ```

### Step 2: Updating Chronology (`cronologia.md`) with Anchor IDs
- Insert a new entry at the **very top** of `cronologia.md` so the diary remains in **reverse chronological order**.
- **Mandatory Anchor ID:** Include an explicit HTML/Markdown anchor (`{#YYYYMMDD-event-id}`) in the heading so self-reported symptoms or home vitals without a physical PDF can be linked directly from `quadro_clinico.md`.
- **Format:**
  ```markdown
  ### DD Month YYYY - [Event/Exam Title] {#YYYYMMDD-event-id}
  - **Summary:** [Summary of results, symptoms, or home measurement]
  - **Report / Evidence:** [Relative link to `[Report Name](referti/YYYYMMDD-name.ext)` OR `Self-reported home measurement`]
  - **Action Required:** [Follow-up tests, dosage changes, or doctor referrals]
  ```

### Step 3: Reconciling Clinical Snapshot (`quadro_clinico.md`)
Evaluate how the new event impacts the ongoing clinical snapshot in `quadro_clinico.md`. Organize `quadro_clinico.md` into standard sections:

1. **Pending Follow-ups & Reminders (`Scadenze`)**
   - Whenever a doctor or report recommends future testing or follow-up visits, add a task item at the top of `quadro_clinico.md`:
     ```markdown
     ## Pending Follow-ups & Reminders
     - [ ] **YYYY-MM-DD**: [Action description, e.g., Repeat lipid panel in 90 days] ([Source](referti/20260715-emocromo.summary.md))
     ```

2. **Current Health Status & Vitals**
   - Update current baseline vitals (blood pressure, weight, heart rate, cholesterol, HbA1c).
   - **100% Traceability Rule:** Every metric in `quadro_clinico.md` **must link** to its source evidence:
     - If backed by a document: link to the report summary `[20260715-emocromo](referti/20260715-emocromo.summary.md)`.
     - If self-reported without a document: link to the chronology entry anchor `[Chronology 2026-08-16](cronologia.md#20260816-fever)`.

3. **Medication Reconciliation (Active vs. Discontinued)**
   - When a medication is newly prescribed, adjusted, or stopped:
     - **Active Medications:** List current drug, dosage, frequency, start date, and indication.
     - **Discontinued Auditing:** NEVER silently erase or overwrite a stopped medication. Move stopped medications to a **`Discontinued / Past Medications`** table with the end date and clinical reason:
       ```markdown
       ### Discontinued Medications
       | Medication | Dosage | Started | Stopped | Reason / Replaced By |
       | :--- | :--- | :--- | :--- | :--- |
       | Ibuprofen | 400mg | 2026-06-01 | 2026-06-10 | Gastric irritation - replaced with Paracetamol |
       ```

---

## 4. Correction & Amendment Protocol
If a report is amended by a clinic, or if an extraction/entry error is discovered:
1. **Amended Reports:** If a clinic issues an updated PDF for an existing exam date, save the new file as `YYYYMMDD-reportname-AMENDED.ext`, update the companion `.summary.md` file, and mark the old file header as `[SUPERSEDED BY AMENDED REPORT]`.
2. **Chronology Audit Note:** Do not silently alter historical logs without context; add an `[AMENDED YYYY-MM-DD]` callout to the affected entry in `cronologia.md` documenting what value was corrected.
3. **Reconcile Snapshot:** Verify and correct the values in `quadro_clinico.md` to reflect the amended data.
