---
name: octopus-energy-rate-check
description: Fetches the latest electricity tariff price from Octopus Energy Italy (<https://octopusenergy.it/le-nostre-tariffe>) for the 'Octopus Fissa' plan, compares it against the user's reference contract rate stored in agent memory (OCTOPUS_ENERGY_CONTRACT_RATE), outputs the price concisely, and alerts the user if the rate is lower than the reference price. Use this skill when the user asks to check Octopus Energy prices, check if the fixed electricity rate dropped, or when monitoring energy rates on a recurring schedule.
author: Rainbowbreeze
license: MIT
version: 1.0.0
---

# Octopus Energy Rate Check

This skill checks the current fixed electricity tariff from Octopus Energy Italy, compares it against the user's reference contract rate stored in memory, and alerts the user if the market rate is lower than their existing contract.

## When to use

Use this skill when:
- The user asks to check the current Octopus Energy rates or "Octopus Fissa" price.
- The user asks if the Octopus electricity tariff has dropped or is cheaper than their contract.
- The agent runs on a recurring schedule to monitor energy price changes.

## Workflow

1. **Check Reference Price in Memory**:
   - Inspect agent memory for the key `OCTOPUS_ENERGY_CONTRACT_RATE` (expected format: numeric float representing €/kWh, e.g. `0.195`).
   - If `OCTOPUS_ENERGY_CONTRACT_RATE` is not present in memory:
     - Ask the user: *"What is your current electricity contract rate in €/kWh? I will save it to memory as `OCTOPUS_ENERGY_CONTRACT_RATE` to compare against future tariffs."*
     - Wait for user response, parse the numerical price, and store it into agent memory as `OCTOPUS_ENERGY_CONTRACT_RATE`.

2. **Extract Current Tariff from Web (with URL Fallback)**:
   - Primary URL: `<https://octopusenergy.it/le-nostre-tariffe>`
   - Attempt extraction using the `web_extract` tool on the primary URL to locate the **"Octopus Fissa"** (or **"Octopus Fissa 24M"**) electricity plan.
   - **Fallback & URL Change Detection**:
     - If the primary URL returns a 404, fails to load, or redirects to an invalid page:
       1. Search the main domain `<https://octopusenergy.it>` using `web_extract` or search to locate the new tariffs page URL (look for links labeled *"Tariffe"*, *"Offerte"*, or *"Luce e Gas"*).
       2. If a new tariffs URL is found:
          - Extract the rates from this new URL.
          - Explicitly notify the user: *"⚠️ The Octopus Energy tariffs URL has changed. The new page is `<NEW_URL>`."*
       3. If no replacement URL can be found:
          - Report a clear error to the user stating that `<https://octopusenergy.it/le-nostre-tariffe>` is unreachable and ask the user to provide the updated URL.
          - Terminate the workflow.
   - Specifically locate:
     - **Electricity raw material price (*Materia prima Luce*)**: price per kWh (e.g. `0,1815 €/kWh`).
     - **Commercialization fee (*Commercializzazione Luce*)**: monthly fixed fee (e.g. `6 €/mese` or `72 €/anno`).
     - **Tariff validity date** (if displayed, e.g. *"Fino al 27/10/2026"*).

3. **Compare Rates**:
   - Compare the current extracted electricity rate with the reference `OCTOPUS_ENERGY_CONTRACT_RATE`.
   - Calculate the difference: `difference = reference_rate - current_rate`.

4. **Output Results**:
   - **Concise Price Summary**: Present the current offer concisely without unnecessary marketing copy:
     - Plan: Octopus Fissa (Electricity)
     - Current Rate: `X,XXXX €/kWh`
     - Fixed Fee: `X €/mese` (`XX €/anno`)
     - Reference Rate: `X,XXXX €/kWh`
   - **Alert on Price Drop**:
     - If `current_rate < reference_rate`: Display a prominent alert notifying the user that the current offer is lower than their contract rate, specifying the price drop in €/kWh and estimated savings percentage.
     - If `current_rate >= reference_rate`: Inform the user that the current offer is equal to or higher than their existing rate, so switching is not advantageous at this time.
   - **Silent Cron Rule**: If invoked as an automated cron task with no price drop detected (and no URL change to report), output `[SILENT]`.
