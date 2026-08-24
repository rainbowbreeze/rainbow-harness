---
name: personal-audio-diary
description: Use when processing, correcting, and formatting voice note transcriptions for user's personal diary. Helps handle raw transcription errors, structure monthly log entries, and maintain durable facts.
version: 1.2.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: [diary, transcription, voice-notes, personal]
    category: rainbowskills
required_environment_variables:
  - name: BRAIN_PERSONALDIARY_PATH
    prompt: Personal Diary folder in the BRAIN knowledge repository 
    help: Define where the personal diary notes folder should be, generally /opt/data/BRAIN/personal-diary
    required_for: full functionality

---

# Audio Diary Processing & Management

## Overview
This skill guides the processing of Alfredo's personal diary, which is primarily updated via voice notes. To preserve strict privacy, all transcription and processing remain local. The primary goal is to turn raw, often phonetically distorted, local speech-to-text (STT) transcriptions into accurate, polished Italian diary entries while updating chronological monthly logs and extracting durable life facts.

## When to Use
- When Alfredo sends a voice message or raw transcribed text intended for his personal diary.
- When Alfredo asks "Puoi processare queste note?" or similar "catch-up" requests without explicitly providing the content (implying the gateway has already transcribed them).
- When reviewing, updating, or maintaining the personal diary directory structure under `$BRAIN_PERSONALDIARY_PATH/`.
- When updating `$BRAIN_PERSONALDIARY_PATH/life_facts.md`.

## Workflow & Guidelines

### 1. Verification of Raw Transcription
- Always include the resolved date and the raw transcript of the voice note exactly as received at the very beginning of your response for the user's verification.
- Format the date and the raw transcript like this:
  **Data Rilevata:** [YYYY-MM-DD] (e.g. "Mercoledì, 24 Agosto 2026")
  > «[Raw Transcription Text]»
- Below the raw transcription, provide a polished and grammatically correct Italian interpretation of what the user actually said. Example:
  *(Interpretazione corretta: «Ieri siamo stati a Torino...»)*

### 2. Tone and Style
- **Realistic & Professional**: Maintain a warm but grounded and professional tone. 
- **Substance over Validation**: Avoid effusive praise or "hyped" language (e.g., "brilliant insight", "incredibly smart move"). Focus on the content of the reflection rather than exaggerated validation.
- **Conciseness**: Keep interpretations and context descriptions focused and substantive.

### 3. State Recovery (Handling catch-up requests)
If the user asks to "process these notes" but no new notes are in the immediate turn:
- **Check Gateway Logs**: Run `strings $HERMES_HOME/logs/gateway.log | grep "inbound message"` to identify recent timestamps of received messages.
- **Search Sessions**: Use `session_search()` with recent queries or date-based terms to find transcribed voice notes that might have been received but not yet written to the logs (often due to mid-turn interruptions).
- **Verify Files**: Cross-reference the found notes with the latest entries in `$BRAIN_PERSONALDIARY_PATH/logs/YYYY-MM.md` to ensure you don't create duplicates.
- **Gateway Errors**: If voice notes fail to reach the agent, check `$HERMES_HOME/logs/gateway.log` for "unpack" errors. See [references/gateway-log-recovery.md](references/gateway-log-recovery.md) and [references/gateway-transcription-error-unpack.md](references/gateway-transcription-error-unpack.md).

### 4. Phonetic Decoding of STT Anomalies
Local STT transcription models frequently produce phonetic misspellings of names, places, and cultural references in Italian. You must actively cross-reference these anomalies:
- **Names / Brands / Artists / Nicknames:** Look up context (e.g. "egie restolidese" -> "Elio e le Storie Tese", "Cloudy" -> "i fiati" or "i flauti", "Fighters" -> "Foo Fighters", "le parche" / "parche" -> "I Pachi", which is the nickname of Simone and Eleonora, "l'evo" -> "Leo", "avrò anche venire salita, sarà Giuliani" -> "sia venuta anche Sara Giuliani").
- **Locations / Events / Landmarks:** Search for matching local events, landmarks, or news (e.g. "atturino al Concerto dei Rockie mille" -> "a Torino al concerto dei Rockin' 1000", "fiumi alticino" -> "fiume Ticino", "ponte delle parche" -> "Ponte delle Barche", "grillo bar" -> "Grillo Verde", "Trascini" -> "[Teatro] Fraschini", "canottieri" -> "Canottieri").
- **Common Words / Expressions:** Pay attention to phonetic mishearings of everyday vocabulary:
  - "rifuso" -> "rifugio" (in the context of friends meeting up at a regular spot)
  - "pirra" -> "birra"
  - "picañha" -> "picanha" (Brazilian beef cut)
  - "lucidori" or "cintori" -> "genitori"
  - "figura di pigmento" -> "figura di riferimento"
  - "un volo" -> "un ruolo"
  - "donate" -> "tornati"
  - "entrare al pene" -> "entrare al pelo" (fitting perfectly/exactly in an angle or space)
  - "lignine" or "vigine" -> "glicine" (wisteria climbing plant) or "confine" (border) / "vicino" (neighbor)
  - "comiriccio" -> "pomeriggio" (afternoon)
  - "dopo paura" -> "dopo un'ora" (after an hour)
  - "l'olio è un punto" -> "non in un punto" (not in a point)
  - "sopra il dubbio" -> "sopraffatto dal sonno" (overcome by sleep)
  - "16 centimetri" -> "16 millimetri" (when discussing domestic garden irrigation tubes, where centimeter ranges are unrealistic)
  - "sornata" -> "giornata" (day)
  - "costino" -> "Costantino" (neighbor's name)
  - "al tornegu' un chiaro" -> "Antonello e Chiara" (neighbors' names)
  - "sabbono" -> "sabato" (Saturday)
  - "Domenico" -> "domenica" (Sunday - watch for context where the day is personified or misheard as a name)
  - "10 giorni super braccia" -> "10 ore sulle braci" (10 hours on the coals - contextual for BBQ/slow-cooking)
  - "fenmentino inudile" -> "filmettino inutile" (useless little movie)
  - "pur et pork" -> "pulled pork"
- **Verification Rule:** Always ask or check facts (using local search tools or past session context) if a transcription segment sounds nonsensical or out of context.

### 5. Local Transcription Fallback (Plan B)
If the gateway logs show "The user sent a message with no text content" or if no transcription is found in `session_search()` for a recent voice note:
1. **Locate the Audio**: Check `$HERMES_HOME/audio_cache/` for the most recent `.ogg` file (`ls -ltr $HERMES_HOME/audio_cache/ | tail`).
2. **Local Inference**: Use `execute_code` to run `faster_whisper` (which is installed in the environment) on the file. Use `model_size="base"` for a balance of speed and accuracy.
3. **Merge & Process**: Once the transcript is obtained, proceed with the standard polishing and logging workflow.

### 6. File Updates and Structure
The personal diary lives in `$BRAIN_PERSONALDIARY_PATH/`. Every new entry requires:

#### Monthly Log (`logs/YYYY-MM.md`)
Append the entry under the correct date. 

**Date Resolution Fallback Hierarchy:**
1. **Explicit Dates**: Use explicit dates mentioned in the text (e.g., "ieri", "il 5 ottobre").
2. **Context**: Use context from previous related notes via `session_search()`.
3. **Midnight Boundary**: If system time is 00:00 - 04:00 AM, treat "oggi" or "stasera" as yesterday.
4. **Ask User**: If ambiguity remains, stop and explicitly ask the user for the correct date *before* writing.

**Standard Template for Log Entries (`$BRAIN_PERSONALDIARY_PATH/logs/YYYY-MM.md`):**
```markdown
## [YYYY-MM-DD] [Optional Day of Week]

**[HH:MM]** 
> «[Raw Transcription Text]»
*(Interpretazione corretta: «[Polished Italian Text]»)*

[Context, reflection, or summary of the entry]

![[Optional Image Description]](../images/YYYY/YYYYMMDD-nome-breve.ext)
```

#### Image Attachments (`images/`)
If the user uploaded/attached an image, save it completely unmodified (no AI processing, no visual edits):
- Inquire/extract the current date: `YYYYMMDD`.
- Infer a short, hyphenated, descriptive name in Italian (e.g., `visita-reggia-di-venaria`, `cena-famiglia`) strictly from the accompanying transcription/text notes of that session—never use AI vision models on the image itself.
- Rename and copy/move the image to `$BRAIN_PERSONALDIARY_PATH/images/YYYY/YYYYMMDD-nome-breve.ext` (where `YYYY` is the current year, maintaining the original extension).
- Add a standard markdown link to the image in the monthly log under the entry (e.g., `![[Descrizione breve]](../images/YYYY/YYYYMMDD-nome-breve.ext)`).

#### Life Facts (`life_facts.md`)
Check if any *durable, long-term facts* emerged. Extract and append them. (Note: When adding facts here or to logs, **never** add anything to the LLM Wiki; they must remain strictly separate).

**Standard Template for `$BRAIN_PERSONALDIARY_PATH/life_facts.md`:**
```markdown
# Personal Life Facts

## 📋 Informazioni Personali e Abitudini
- [YYYY-MM-DD] [Fact details, e.g., Uses Proxmox/Ollama for local AI]

## 👥 Persone e Relazioni
- [YYYY-MM-DD] [Fact details, e.g., Emanuele has two kids]

## 🎯 Obiettivi e Decisioni
- [YYYY-MM-DD] [Fact details, e.g., Started focusing on 'Consapevolezza Genitoriale']

## 📈 Cronologia dei Cambiamenti di Stato
- [YYYY-MM-DD] [Significant daily milestone]
```

### 7. Privacy & Test Session Cleanup (Hygiene)
When Alfredo runs voice tests or requests a privacy-based cleanup of a session or test messages ("cancella le memorie", "non lasciare tracce", etc.), execute a thorough purge of all transient traces:
- **Audio Cache:** Scan `$HERMES_HOME/audio_cache/` for any recently created `.ogg` files (e.g. within the hour or linked to the session) and delete them.
- **Log Files:** Scan `$HERMES_HOME/logs/agent.log`, `$HERMES_HOME/logs/gateway.log`, and `$HERMES_HOME/logs/errors.log`. Replace any lines containing the active test `session_id` or exact transcript substrings of test messages with `[LOG ENTRY REDACTED FOR PRIVACY]`.
- **Database Messages:** Open `$HERMES_HOME/state.db` using Python's `sqlite3` module. Locate the messages for the test session in the `messages` table and delete them (FTS search indexes will be automatically updated by SQLite triggers).

### 8. Whisper Hallucinations (Silent/Low Audio)
When the voice message is silent, contains only sighs, breathing, or background noise, the local Whisper model frequently hallucinates specific fixed Italian phrases:
- *«Sottotitoli e revisione a cura di QTSS»*
- *«Sottotitoli creati dalla comunità Amara.org»*
- **Handling:** If the transcription matches these phrases exactly, do NOT treat them as actual spoken text. Address them humorously and politely as a known Whisper hallucination due to silence or background noise, ask the user if they'd like to repeat, and log the event as a system/silent test rather than an actual diary entry.

### 9. Accidental / Ultra-short Voice Notes (Discord Errors) & Fragment Merging
Sometimes Alfredo might accidentally record a voice note on Discord, such as pressing the record button but lifting his finger immediately before the recording actually starts or finishes. 
- **Rule for Accidental Notes**: If the transcript of the voice note has **no more than 6 words** (ultra-short) and contains no clear narrative fragment or incomplete thought (e.g. just a greeting or silent noise), it must be considered an accidental Discord recording error.
- **Handling of Accidental Notes**: Ignore these notes completely. Do not write them to the monthly logs, do not update `life_facts.md`, and do not save any associated files. Simply ignore the entry, and if appropriate, politely and briefly acknowledge that the recording was likely too short or accidental.
- **Rule for Fragmented / Cut-off Notes**: If an ultra-short note contains an incomplete sentence or narrative hook (e.g., "martedì l'ho passato praticamente a...", "volevo dirti che...") and the user immediately follows up with a continuation voice note (often beginning with "Dicevo che...", "Stavo dicendo...", "Sì, ..."), do NOT treat them as separate or ignorable events.
- **Handling of Fragmented Notes**: Hold the first fragment in context. Once the continuation is received, **merge** both transcriptions, provide a single polished Italian interpretation, and record them together under a single, unified log entry for that day. This keeps the monthly diary cohesive and preserves the original narrative flow.

## Common Pitfalls
1. **Failing to include the raw transcript:** The user needs to verify the raw transcript to spot any misunderstanding. Always supply it.
2. **Accepting nonsensical transcriptions literally:** Always attempt to phonetically decode and offer a corrected interpretation of distorted Italian words.
3. **Blindly trusting system time:** Do not automatically log entries under today's date. Always apply the Date Resolution Fallback Hierarchy to ensure the entry is placed on the actual day the events occurred.
4. **Writing too much narration:** Keep the conversation concise, warm, emotionally intelligent, but focused. Alfredo prefers a direct and professional tone.

## Verification Checklist
- [ ] Resolved date and raw transcription included at the start of the response.
- [ ] Polished Italian interpretation supplied.
- [ ] Log entry appended to the correct `$BRAIN_PERSONALDIARY_PATH/logs/YYYY-MM.md` file following the template.
- [ ] Durable facts extracted to `$BRAIN_PERSONALDIARY_PATH/life_facts.md` following the template (if applicable).
