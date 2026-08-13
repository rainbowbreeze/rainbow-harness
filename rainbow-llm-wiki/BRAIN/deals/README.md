# Deals (`deals/`) — Directory Resolver

> **Primary Home for:** Financial transactions, term sheets, angel/VC investments, M&A, and commercial partnerships.

---

## 1. What Goes Here
- Investment records, SAFE notes, priced rounds, commercial contract negotiations.
- Slug convention: `company-round-year.md` (e.g. `acme-series-a-2026.md`)

## 2. What Does NOT Go Here
- General company profiles [`companies/`](../companies/README.md)
- Investor biographies [`people/`](../people/README.md)

---

## 3. Deal Page Template

```markdown
---
type: deal
id: company-round-year
title: Company Round Year
company: "companies/company-slug"
stage: Series A
amount: "$10M"
lead_investor: "people/investor-slug"
status: closed # evaluating | term-sheet | closed | passed
tags: [tag1, tag2]
updated_at: "YYYY-MM-DD"
---

# Company Round Year

> Executive summary: Terms, strategic rationale, and final outcome.

## State
- **Company:** [Company Name](../companies/company-slug.md)
- **Round / Valuation:** Stage @ Valuation
- **Key Investors:** [Investor Name](../people/investor-slug.md)
- **Status:** Closed / Passed

## Rationale & Deal Dynamics
- Investment thesis, competitive dynamics, and diligence findings.

## Open Threads
- Outstanding legal docs, wire status, or board setup.

---

## Timeline
- **YYYY-MM-DD** | [Term Sheet / Close] — Event logged.
```
