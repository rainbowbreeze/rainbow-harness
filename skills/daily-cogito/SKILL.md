---
name: daily-cogito
description: "Use this skill when the user wants to extract wisdom or add a new thought (from a text snippet or a YouTube video) to their archive, or when they ask to retrieve a random thought or wisdom from the archive."
author: Rainbowbreeze
license: MIT
version: 1.0.4
metadata:
  hermes:
    required_environment_variables:
      - name: BRAIN_WISDOMDB_PATH
        prompt: Where should the thoughts archive be stored?
        help: Absolute path to the JSON file where the thoughts are stored.
        required_for: full functionality
---

# Daily Cogito

This skill manages an archive of thoughts. It can add thoughts from a provided text snippet or a YouTube video, summarizing them into key topics and extracting any aphorisms or quotes. It also allows retrieving a random thought from the archive.

## Trigger Conditions
Use this skill when:
- The user asks to extract wisdom from a text or a YouTube video.
- The user asks to add a thought from text.
- The user asks to add a thought from a YouTube URL.
- The user asks to retrieve a random thought.

## Workflow for Adding a YouTube Video
1. **Check if Already Added**: First, check if the video has already been added to the archive by running `uv run python scripts/manage_archive.py --action check --url "<VIDEO_URL>"`. If the script returns `EXISTS`, inform the user that the video is already in the archive and abort the workflow. If it returns `NOT_FOUND`, proceed to the next step.
2. **Summarize Video**: Delegate the summarization of the video to the existing video summarization skill. Instruct it to extract exactly five key topics and any aphorisms or quotes from philosophers or authors. Ensure the summary is detailed, but not extremely detailed.
3. **Present for Review**: Present the returned summarization to the user.
4. **Ask for Confirmation**: Ask the user for confirmation to store it, whether they want to cancel the operation, or if they have any changes to the content before storing it. Wait for the user's reply.
5. **Store Thought**: Once approved or modified by the user, execute `scripts/manage_archive.py` using `uv run python scripts/manage_archive.py --action add --body "<FINALIZED_BODY>" --url "<VIDEO_URL>"`. Ensure that environment variable `${BRAIN_WISDOMDB_PATH}` is available.
6. **Confirm Success**: Confirm success to the user.

## Workflow for Adding Text
1. **Summarize Text**: Analyze the provided text and summarize it into exactly five key topics. Ensure the summary is detailed, but not extremely detailed.
2. **Extract Quotes**: Extract any aphorisms or quotes and list them below the key topics.
3. **Present for Review**: Present the summarization to the user.
4. **Ask for Confirmation**: Ask the user for confirmation to store it, whether they want to cancel the operation, or if they have any changes to the content before storing it. Wait for the user's reply.
5. **Store Thought**: Once approved or modified by the user, execute `scripts/manage_archive.py` using `uv run python scripts/manage_archive.py --action add --body "<FINALIZED_BODY>"`. If a source URL was provided, include it with `--url "<SOURCE_URL>"`. Ensure that environment variable `${BRAIN_WISDOMDB_PATH}` is available.
6. **Confirm Success**: Confirm success to the user.

## Workflow for Retrieving a Random Thought
1. **Retrieve Thought**: Execute `scripts/manage_archive.py` using `uv run python scripts/manage_archive.py --action random`. Ensure that environment variable `${BRAIN_WISDOMDB_PATH}` is available.
2. **Present Thought**: Display the retrieved thought to the user (excluding the submission date). Ensure to include the source URL if present, wrapping it in angle brackets (e.g., `<URL>`) to prevent chat clients from generating link previews.
