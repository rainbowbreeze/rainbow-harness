# Schools (`schools/`) — Directory Resolver

> **Primary Home for:** Public and private school complexes, institutes, and educational campuses.

---

## 1. What Goes Here
- Any comprehensive school complex (*istituto comprensivo*), high school (*liceo*, *istituto tecnico/professionale*), elementary/middle school campus, or university/educational institution.
- Slug convention: `school-name-city.md` (lowercase, hyphens for spaces, including the city name to prevent collisions across cities).

## 2. What Does NOT Go Here
- Individual school principals, teachers, or digital animators [`people/`](../people/README.md)
- Specific workshops, courses, or active software builds organized with the school [`projects/`](../projects/README.md)
- Assemblies, summits, or public demo days hosted at the school [`events/`](../events/README.md)
- Universal pedagogical frameworks or manifestos like *Patti Digitali Pavesi* [`concepts/`](../concepts/README.md)

---

## 3. School Page Template

```markdown
---
type: school
id: school-name-city
title: School Name
aliases: ["Alternate Name", "Official Code"]
status: active # active | inactive | evaluating | historical
tags: [school, city-name, elementary, middle-school]
city: "City Name"
addresses:
  - "Primary Seat Address"
  - "Secondary Branch / Plesso Address"
class_levels:
  - infant      # Scuola dell'infanzia
  - elementary  # Scuola primaria
  - middle      # Scuola secondaria di primo grado
  - high-school # Scuola secondaria di secondo grado
principal: "people/principal-slug"
digital_animator: "people/animator-slug"
contacts:
  - "people/contact-slug"
patti_digitali_pavesi: true
patti_digitali_subscribed_at: "YYYY-MM-DD"
relations:
  - target: "people/principal-slug"
    type: "principal"
  - target: "people/animator-slug"
    type: "digital-animator"
  - target: "people/contact-slug"
    type: "contact"
  - target: "projects/project-slug"
    type: "organized-project"
  - target: "concepts/patti-digitali-pavesi"
    type: "manifesto-subscriber"
updated_at: "YYYY-MM-DD"
---

# School Name

> Executive summary: Core 1-2 sentence distillation of the school complex, its locations, educational identity, and digital participation.

## Identity & Locations
- **City**: City Name
- **Class Levels**: List of educational levels offered (`infant`, `elementary`, `middle`, `high-school`)
- **Locations / Plessi**:
  1. *Primary Seat*: Address 1
  2. *Branch*: Address 2
- **Official Website / Meccanografico Code**: URL and Code

## Leadership & Key Contacts
- **Dirigente Scolastico (Principal)**: [Principal Name](../people/principal-slug.md) — *source: [Citation], confidence: high*
- **Animatore Digitale (Digital Animator)**: [Animator Name](../people/animator-slug.md) — *source: [Citation], confidence: high*
- **Liaisons & Contacts**:
  - [Contact Name](../people/contact-slug.md) — Role / relationship

## Patti Digitali Pavesi & Digital Culture
- **Status**: Subscribed / Not Subscribed (`patti_digitali_pavesi: true/false`)
- **Subscription Date**: YYYY-MM-DD
- **Local Implementation & Digital Stance**:
  - Details on smartphone guidelines, digital literacy programs, and parental involvement — *source: [Citation], confidence: medium*

## Projects & Collaborations

### Past Projects
| Project / Event | Dates | Scope / Role | Epistemic Status |
| :--- | :--- | :--- | :--- |
| [Project Name](../projects/project-slug.md) | Date Range | Summary of school's participation | *source: [...], confidence: high* |

### Future & Active Projects
| Project / Event | Planned Target | Scope / Status | Epistemic Status |
| :--- | :--- | :--- | :--- |
| [Project Name](../projects/project-slug.md) | Planned Date | Summary of planned scope | *source: [...], confidence: medium* |

## Open Threads
- Pending actions, workshops to schedule, or missing contact verifications

## See Also
- [Principal Name](../people/principal-slug.md)
- [Patti Digitali Pavesi](../concepts/patti-digitali-pavesi.md)

---

## Timeline
- **YYYY-MM-DD** | [Source Type: Source Name] — Dated, immutable evidence log entry (e.g. initial contact, workshop completed, subscription to Patti Digitali).
```
