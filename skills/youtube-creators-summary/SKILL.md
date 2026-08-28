---
name: youtube-creators-summary
description: "Use this skill when the user asks to generate a daily intelligence report of new YouTube videos from a specific list of technical and financial creators."
tags: [youtube, monitoring, rss, research, intelligence]
---

# YouTube Creators Summary

This skill monitors a curated list of YouTube channels and generates a structured intelligence report for videos published in the last 24 hours. It categorizes creators into "Quick Summary" and "Deep Dive" tiers.

## Workflow
1. **Fetch Data:** Execute `scripts/fetch_latest_videos.py` passing the creators list `assets/creators.json` as an argument. This script queries YouTube RSS feeds and returns a JSON of new videos.
2. **Filter Content:** **Exclude YouTube Shorts** from the report.
3. **Analyze Deep Dive Tier:** For "Deep Dive" creators, delegate the video content summarization to a subagent. Instruct the subagent to use the specialized YouTube video summarization skill on the video URL, and to format its output strictly according to the "Deep Dive Format" defined below. Wait for the subagent to return the pre-formatted results before proceeding.
4. **Format for Intelligence:** Strictly use the following standard formats for the two groups:
   - **Quick Summary Format:**
     - **Title:** `Video Title`
     - **Creator:** `@CreatorName`
     - **Link:** `<URL>`
     - **Tags:** [e.g., #Hardware, #Networking]
     - **Summary:** A single-sentence summary based on the title and description.
   - **Deep Dive Format:**
     - **Title & Creator:** `Video Title` by `@CreatorName`
     - **Link:** `<URL>`
     - **Headline:** Catchy, high-level summary of the video's premise.
     - **The Lead:** 2-3 sentences explaining what the video covers and why it matters.
     - **Key Facts:** Exactly 5 bullet points of the most critical arguments, data points, or evidence.
5. **URL Suppression:** Wrap ALL URLs in `<>` (e.g., `<https://youtube.com/...>`) to suppress automatic link previews.
6. **Delivery Logic:** Produce the final report directly as the tool output.
7. **Validation:** Verify that the report is accurately formatted and successfully generated without truncation.

## Creators List
The full list of monitored creators is maintained in `assets/creators.json`. They are categorized into `GROUP_A` (Quick Summary) and `GROUP_B` (Deep Dive).

## Support Files
- `scripts/fetch_latest_videos.py`: Main data extraction script.
- `assets/creators.json`: JSON file containing the monitored creators.

## Pitfalls
- **Preview Spam:** Forgetting the `<>` wrappers around links can cause enormous video previews in some chat clients, making the report unreadable.
- **Shorts Noise:** RSS feeds often include Shorts; these must be filtered out manually by checking for `/shorts/` in the URL.
