# Gateway Log Recovery for Personal Diary

When the user asks "Puoi processare queste note?" or "Process catch-up", and the notes are not in the current context window, use these steps to find the "lost" transcriptions.

## 1. Locate Inbound Message Timestamps
The gateway logs every message it receives, including the automated transcription text from the STT provider.

```bash
strings logs/gateway.log | grep "inbound message" | tail -n 20
```

Look for messages from `user=RainbowDev` in the relevant diary chat (usually `chat=1510436308546224218`).

## 2. Retrieve Transcripts via Session Search
Timestamps in the log correspond to session starts. Use `session_search` to find sessions created around those times.

```python
# Example: If log shows a message at 2026-06-09 02:14:06
session_search(query="2026-06-09", sort="newest")
```

Or browse recently active sessions:
```python
session_search()
```

## 3. Extract Transcription
Once the session is identified, read it to find the system-generated transcription marker:
`[The user sent a voice message~ Here's what they said: "..."]`

## 4. Deduplication
Before writing to `logs/YYYY-MM.md`, always check the last 3-5 entries in the current month's log to ensure the note hasn't already been processed.

```bash
tail -n 50 BRAIN/personal-diary/logs/YYYY-MM.md
```

## 5. Local Transcription Fallback (Plan B)
If the logs or session search return an empty transcript, use `execute_code` to transcribe the cached audio file manually.

```python
from faster_whisper import WhisperModel
import os

# 1. Identify the latest file in audio_cache
# 2. Run transcription
model = WhisperModel("base", device="cpu", compute_type="int8")
audio_path = "./profiles/chronicler/audio_cache/latest_file.ogg"
segments, info = model.transcribe(audio_path, beam_size=5, language="it")

full_transcript = " ".join([s.text for s in segments])
print(full_transcript)
```
