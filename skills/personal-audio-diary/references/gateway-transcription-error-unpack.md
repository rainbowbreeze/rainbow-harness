# Gateway STT Unpack Error (ValueError)

## Symptom
When a user sends a voice note on Discord without a text caption, the gateway logs show:
`ValueError: too many values to unpack (expected 2)`
And the traceback points to:
`File "$HERMES_HOME/gateway/run.py", line 7479, in _prepare_inbound_message_text`
`message_text, _successful_transcripts = await self._enrich_message_with_transcription(...)`

## Root Cause
In `$HERMES_HOME/gateway/run.py`, the function `_enrich_message_with_transcription` had a logic branch for Discord's "no text" placeholder:
`(The user sent a message with no text content)`

When this placeholder was detected, the function returned `prefix` (a string) instead of the expected `(prefix, successful_transcripts)` (a tuple).

## Fix (Applied 2026-06-15)
The return statements in `_enrich_message_with_transcription` were patched to ensure they always return the `(text, list)` tuple, even when stripping the placeholder.

```python
# Before
if user_text and user_text.strip() == _placeholder:
    return prefix

# After
if user_text and user_text.strip() == _placeholder:
    return prefix, successful_transcripts
```

## Impact on Diary Processing
If this error occurs, the voice note is never passed to the agent, so "Plan B" (local transcription fallback) in the `personal-audio-diary` skill cannot trigger because the agent loop never starts for that message.
