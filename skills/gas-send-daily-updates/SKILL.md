---
name: gas-send-daily-updates
description: Legge il bollettino giornaliero dal BRAIN e lo invia ai membri del GAS. Usa questa skill per distribuire le comunicazioni e le scadenze.
version: 1.0.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: ["GAS", "gruppo acquisto solidale", "communications"]
    category: GAS
    config:
      - key: BRAIN_ROOT_PATH
        description: "Path to the BRAIN knowledge base directory"
        default: "/opt/data/BRAIN"
        prompt: "Where is the root of the BRAIN knowledge base?"
---

# 📤 Send GAS Daily Updates

## Trigger
Usa questa skill durante il giorno (es. tramite cron job) per inviare il riepilogo giornaliero delle attività, ordini e scadenze ai membri del GAS.

## Flusso di Lavoro

1. **Verifica Bollettino**:
   - Controlla l'esistenza del file `${BRAIN_ROOT_PATH}/bulletin/YYYY-MM-DD-bulletin.md` per la data odierna.
   - Se il file non esiste, significa che non ci sono aggiornamenti per oggi. Rispondi esattamente con `[SILENT]` (non inviare nessuna email) e termina l'esecuzione.

2. **Lettura e Invio**:
   - Se il file esiste, leggi il contenuto di `${BRAIN_ROOT_PATH}/bulletin/YYYY-MM-DD-bulletin.md`.
   - Usa la skill `gas-agentmail` per inviare un'email.
   - **Destinatario**: `info@rainbowbreeze.it`
   - **Oggetto**: "Aggiornamenti GAS - YYYY-MM-DD" (sostituisci con la data odierna).
   - **Corpo del messaggio**: Il contenuto testuale del bollettino.

3. **Post-Invio**:
   - Lascia il file del bollettino inalterato nella sua posizione originale. Non cancellarlo o spostarlo.
