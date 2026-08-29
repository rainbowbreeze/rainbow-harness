---
name: news-report-pavia
description: Generates a structured daily report in Italian about Pavia city and its province using specific sources.
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [journalism, news]
    category: rainbowskills
---

# News Report Pavia Skill

This skill automates the generation of a daily report in Italian covering local news for Pavia and its province.

## Sources

### News (Pavia & Province)
- **Source List**: See `assets/news-sources.json` for the complete list of news websites and their respective RSS feeds.

## Core Execution Workflow

1. **Information Gathering - News (Last 24h)**:
   - **Primary Method**: Run the included Python script `scripts/parse_rss.py` via the terminal. This script automatically parses the RSS feeds listed in `assets/news-sources.json` and outputs articles from the last 24 hours in JSON format. **Use this script only for sources that have an RSS feed defined in the JSON file.** For sources without an RSS feed, directly use web scraping (`web_extract` or `web_search`).
   - **Primary Focus**: Pavia city.
   - **Volume Limits**: Minimum 10 news items. Maximum 3 items related to the wider province.
   - **Exclusions**: Do NOT include commercial, advertising, crime news, or sports news.

2. **Output Structure & Tone (STRICTLY ITALIAN)**:
   - **Language**: Strictly Italian.
   - **Tone**: Professional and journalistic. Focus on clarity, objectivity, and precision.
   - **Format Template**: You MUST exactly match this Markdown template structure:
     ```markdown
     # Notiziario di Pavia: [YYYY-MM-DD]

     ## Sintesi della Giornata
     [Paragrafo 1: Sintesi delle notizie più importanti]
     
     [Paragrafo 2: Altri dettagli di rilievo]

     ## Ultime Notizie
     * **[Titolo della Notizia]** - [YYYY-MM-DD]
       - **URL**: [Link]
       - **Descrizione**: [Breve riassunto]
     * **[Titolo della Notizia]** - [YYYY-MM-DD]
       - **URL**: [Link]
       - **Descrizione**: [Breve riassunto]
     ```

3. **Delivery Instructions**:
   - Provide the structured report directly as your final response to be delivered to the destination specified in the job context.

## Pitfalls & Resilience

- **Extraction Failures**: If the primary RSS script (`scripts/parse_rss.py`) fails, returns empty results for some sources, or if additional non-RSS sources need checking, fall back to web extraction using `web_extract` or `web_search`. If `web_extract` hits errors (e.g., "Payment Required" or 403 Forbidden) or `web_search` hits rate limits, try using specific date queries: `notizie Pavia ultime 24 ore "DD Mese YYYY"`.
- **Content Filtering**: Ensure "Sports" and "Advertising" news are excluded as per requirements, even when using broader search results.
