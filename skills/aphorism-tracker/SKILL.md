---
name: aphorism-tracker
description: Use to save or retrieve text/image quotes or aphorisms to the BRAIN.
version: 1.2.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: [aphorisms, wisdom]
    category: rainbowskills
required_environment_variables:
  - name: BRAIN_APHORISMS_PATH
    prompt: Folder to store aphorisms in the BRAIN knowledge repository 
    help: Define where the projects folder must be, generally /opt/data/BRAIN/aphorisms
    required_for: full functionality
---

# Aphorism Tracker Skill

Use this skill to process and save phrases, quotes, and aphorisms provided by the user.

## 1. Triggers
- **Save a quote:** When the user provides a quote/phrase in text or an image containing text, and indicates it should be saved or tracked.
- **Retrieve a random quote:** When the user asks for a random quote, aphorism, or phrase.

## 2. Processing Steps
1. **Extraction**: 
   - **If text:** Identify the quote text, author(s), and source if provided.
   - **If dictated (voice transcript):** Carefully separate the actual quote from conversational wrappers (e.g., "Save this quote...", "Hey Chronicler..."). Fix missing punctuation, capitalization, and obvious speech-to-text misspellings before constructing the JSON.
   - **If image:** Use the `vision_analyze` tool to extract the text, identifying the quote and author(s). Clean up OCR artifacts or unexpected line breaks.
2. **Translation**:
   - If the original quote is in a language other than Italian, translate it into Italian.
   - **Exception:** If the user explicitly instructs to keep the sentence in the original language, do not translate it.
3. **Deduplication**:
   - Read `${BRAIN_APHORISMS_PATH}/aphorisms.json`.
   - Compare the extracted/translated text with existing entries in the JSON array using semantic/fuzzy matching.
   - If a duplicate is found (matching meaning/key words), provide a brief message stating it's a duplicate, show the existing duplicate phrase, and DO NOT add it. No further explanation is needed.
4. **Image Handling (if applicable)**:
   - Generate a filename formatted as `YYYYMMDD-summary-of-the-aphorism.ext` (using the current date and a brief description of the quote).
   - Move or copy the provided image to `${BRAIN_APHORISMS_PATH}/sources/<filename>`.
5. **JSON Construction**:
   - Create a JSON object matching this schema:
     ```json
     {
       "text": "The extracted and/or translated quote",
       "author": ["Author 1", "Author 2"],
       "source": "Optional source context",
       "imagesrc": "YYYYMMDD-summary-of-the-aphorism.ext"
     }
     ```
   - Omit `imagesrc` or `source` if they are not applicable.
6. **Save**:
   - Append the new object to the array.
   - Write the updated JSON back to `${BRAIN_APHORISMS_PATH}/aphorisms.json`.
7. **Confirmation**:
   - Provide a very brief confirmation that the aphorism was added (e.g. "Frase aggiunta: "), and then the phrase. Do not display the parsed JSON data or explain the steps taken. Do not add comments or consideration on the added sentence.

## 3. Retrieving a Random Aphorism
When the user asks for a random aphorism:
1. Execute the script `scripts/get_random_aphorism.py` using `uv run` and pass the path to the aphorisms JSON file using the `--file` argument: 
   `uv run scripts/get_random_aphorism.py --file ${BRAIN_APHORISMS_PATH}/aphorisms.json`.
2. Display the returned formatted text to the user exactly as it is outputted by the script. Do not add extra commentary.