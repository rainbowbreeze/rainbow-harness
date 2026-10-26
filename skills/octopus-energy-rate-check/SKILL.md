---
name: octopus-energy-rate-check
description: Fetches the latest electricity tariff price from Octopus Energy and compares it against the user's reference contract rate. Use this skill when the user asks to check Octopus Energy prices, update their stored reference electricity rate, check if the fixed electricity rate dropped, or when monitoring energy rates on a recurring schedule.
author: Rainbowbreeze
license: MIT
version: 1.0.0
metadata:
  hermes:
    category: rainbowskills
    tags: [price-tracker]
---

# Octopus Energy Rate Check

Checks the current "Octopus Fissa" electricity tariff (`€/kWh`) from Octopus Energy Italy, compares it against the reference contract rate stored in agent memory (`OCTOPUS_ENERGY_CONTRACT_RATE`), and outputs a strict, minimal result with a price-drop alert when cheaper.

## When to use

Use this skill when:
- The user asks to check the current Octopus Energy rate or "Octopus Fissa" price.
- The user asks if the Octopus electricity tariff has dropped or is cheaper than their contract.
- The user asks to set or update their stored Octopus reference rate (`OCTOPUS_ENERGY_CONTRACT_RATE`).
- The agent runs on a recurring schedule to monitor energy price changes.

## Workflow

1. **Resolve Reference Rate in Memory (`OCTOPUS_ENERGY_CONTRACT_RATE`)**:
   - **Direct Update Request**: If the user explicitly provides a new contract rate (e.g., *"Set my Octopus rate to 0.1815"*), normalize the decimal separator to a dot (`.`), save the float to agent memory under `OCTOPUS_ENERGY_CONTRACT_RATE`, confirm the update in one line, and stop (unless they also asked to check the current web rate).
   - **Lookup**: Inspect agent memory for `OCTOPUS_ENERGY_CONTRACT_RATE`.
   - **Missing Rate**: If `OCTOPUS_ENERGY_CONTRACT_RATE` is not found in memory:
     - Ask the user: *"What is your current electricity contract rate in €/kWh? I will save it to memory as `OCTOPUS_ENERGY_CONTRACT_RATE`."*
     - Wait for the user's reply, normalize any comma decimal separator to a dot (e.g., `0,195` -> `0.195`), store it in agent memory as `OCTOPUS_ENERGY_CONTRACT_RATE`, and proceed to Step 2.

2. **Extract Current Electricity Rate from Web (with URL Fallback)**:
   - Primary URL: `<https://octopusenergy.it/le-nostre-tariffe>`
   - Use `web_extract` on the primary URL to find the **"Octopus Fissa"** (e.g., *"Octopus Fissa 24M"* or *"Octopus Fissa 12M"*) electricity section.
   - **Extraction Guardrails**:
     - Extract ONLY the **Electricity raw material price (*Materia prima Luce*)** in `€/kWh`.
     - Ignore monthly commercialization fees (*Commercializzazione*), Gas rates (`€/Smc`), and *PLACET Fissa* plans.
     - **Decimal Normalization**: Convert the Italian comma decimal separator to a dot before comparison (e.g., `0,1815` -> `0.1815`).
   - **URL Fallback & Change Detection**:
     - If the primary URL returns a 404, fails to load, or no longer contains the tariffs:
       1. Use `web_extract` or search on `<https://octopusenergy.it>` to locate the updated tariffs page URL (look for *"Tariffe"*, *"Offerte"*, or *"Luce"*).
       2. If a new URL is found, extract the rate from the new URL and prepend this notice to the final output:
          `⚠️ The Octopus Energy tariffs URL has changed to <NEW_URL>.`
       3. If no replacement URL can be found, output:
          `❌ Unable to reach <https://octopusenergy.it/le-nostre-tariffe> or locate the updated tariffs page. Please provide the new URL.`
          and terminate the workflow.

3. **Compare Rates**:
   - Compare the normalized extracted `current_rate` against `reference_rate` (`OCTOPUS_ENERGY_CONTRACT_RATE`).
   - Calculate `drop = reference_rate - current_rate` and `pct = (drop / reference_rate) * 100`.

4. **Output Results (Strict Minimalist Template)**:
   - Always output the result (including on scheduled runs). Do NOT include conversational filler, greetings, or extra tariff conditions.
   - **If `current_rate >= reference_rate`**:
     ```markdown
     ⚡ **Octopus Fissa**: [current_rate] €/kWh (Your rate: [reference_rate] €/kWh)
     ```
   - **If `current_rate < reference_rate`**:
     ```markdown
     ⚡ **Octopus Fissa**: [current_rate] €/kWh (Your rate: [reference_rate] €/kWh)
     🚨 **ALERT**: Rate dropped by [drop] €/kWh (-[pct]%)!
     Would you like to update `OCTOPUS_ENERGY_CONTRACT_RATE` to [current_rate] €/kWh?
     ```
   - If the user replies confirming the update, overwrite `OCTOPUS_ENERGY_CONTRACT_RATE` in agent memory with `current_rate`.
