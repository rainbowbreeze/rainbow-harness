---
name: youtube-creators-summary
description: "Use this skill when the user asks to generate a daily intelligence report of new YouTube videos from a specific list of technical and financial creators."
tags: [youtube, monitoring, rss, research, intelligence]
---

# YouTube Creators Summary

This skill monitors a curated list of YouTube channels and generates a structured intelligence report for videos published in the last 24 hours. It categorizes creators into "Basic Info" (Group A) and "AI Summary" (Group B).

## Scheduling & Delivery
- **Target Discord Channel:** `1485386401242677491` (#hermes-youtube-createtors-report)
- **Character Limit:** 5,000 characters per message.
- **Sectioning:** The "Upcoming Events" section (if present) must be sent in a separate message from the main summary.

## Workflow
1. **Fetch Data:** Execute `scripts/fetch_latest_videos.py`. This script queries YouTube RSS feeds for ~50 channels and returns a JSON of new videos.
2. **Filter Content:** **Exclude YouTube Shorts** from the report.
3. **Analyze Group B:** For Group B creators, perform a deep dive using `web_extract` on the video URL or search for content summaries to provide a "actual content" summary rather than just the description.
4. **Format for Intelligence:** Use the `investigative-correspondent` persona style (Headline, Lead, Key Facts, Chronology, Sources).
5. **URL Suppression:** Wrap ALL URLs in `<>` (e.g., `<https://youtube.com/...>`) to suppress Discord link previews.
6. **Delivery Logic:**
   - **Manual/Scheduled Run:** Use the `send_message` tool for the target Discord channel.
   - **Individual Delivery:** For each video or logical group (e.g., all of Group A), call `send_message` immediately. **Do NOT aggregate multiple videos into a single giant message** to avoid rate limits and length issues.
   - **Cron Context:** If the job prompt explicitly says "do NOT use send_message," produce the final report as the tool output.

## Creators List
- **Group A (Basic Info):** Includes technical channels like @ETAPRIME, @JeffGeerling, @mr_rip, @PietroMichelangeli, and @home_assistant.
- **Group B (AI Summary):** Includes high-impact creators like @NetworkChuck, @mkbhd, @CiaoElsa, and @thebull_finance.

## Support Files
- `scripts/fetch_latest_videos.py`: Main data extraction script.
- `scripts/discord_notifier.py`: Standalone notifier using standard libraries for cron environments.

## Pitfalls
- **Aggregation Failure:** Sending too many videos in one message will exceed the 5000-character limit and trigger Discord's block. Always split by video or category.
- **Preview Spam:** Forgetting the `<>` wrappers around links will fill the channel with enormous video previews, making the report unreadable.
- **Shorts Noise:** RSS feeds often include Shorts; these must be filtered out manually by checking for `/shorts/` in the URL.
