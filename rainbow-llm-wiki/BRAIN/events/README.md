# Events (`events/`) — Directory Resolver

> **Primary Home for:** Industry conferences, developer summits, hackathons, demo days, webinars, workshops, product launches, and community meetups.

---

## 1. What Goes Here
- Multi-person public or industry gatherings where the user attends, speaks, hosts, or tracks.
- Slug convention: `YYYY-MM-DD-event-name.md` (e.g. `2026-10-12-ai-developer-summit.md`).

## 2. What Does NOT Go Here
- Specific 1:1 syncs, internal team meetings, or board calls --> [`meetings/`](../meetings/README.md).
- The ongoing software code or specification presented at the event --> [`projects/`](../projects/README.md) (link the event to the project).
- Commercial funding term sheets discussed at a demo day --> [`deals/`](../deals/README.md).

---

## 3. Event Page Template

```markdown
---
type: event
id: YYYY-MM-DD-event-name
title: Event Title
aliases: ["Short Name", "Event Hashtag"]
status: upcoming # upcoming | attending | speaking | completed | cancelled
tags: [conference, ai, devtools]
relations:
  - target: "companies/organizer-slug"
    type: "organizer"
  - target: "people/speaker-slug"
    type: "speaker"
start_date: "YYYY-MM-DD"
end_date: "YYYY-MM-DD"
location: "San Francisco, CA" # or "Virtual"
url: "https://example.com/event"
updated_at: "YYYY-MM-DD"
---

# Event Title

> Executive summary: What the event is, its strategic relevance, and objectives for attending.

## State
- **Dates:** YYYY-MM-DD to YYYY-MM-DD
- **Location:** San Francisco, CA / Virtual
- **Role:** Attendee / Speaker / Sponsor / Organizer
- **Key Organizers:** [Organizer Name](../companies/organizer-slug.md)

## Key Themes & Agenda
- Core topics, keynote highlights, and major panel discussions.

## Speakers & Notable Attendees
- [Speaker Name](../people/speaker-slug.md) — Topic: Keynote Speech

## People Met & Connections Made
- [Contact Name](../people/contact-slug.md) — Context: Met at session, discussed collaboration.

## Takeaways & Follow-ups
- Key insights, learnings, and next action items.

## Open Threads
- Pending follow-ups or intros to send after the event.

## See Also
- [Related Company](../companies/organizer-slug.md)
- [Related Project](../projects/project-slug.md)

---

## Timeline
- **YYYY-MM-DD** | [Registration / Attendance] — Event milestone logged.
```
