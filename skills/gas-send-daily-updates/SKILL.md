---
name: gas-send-daily-updates
description: Legge il bollettino giornaliero dal BRAIN e lo invia ai membri del GAS. Usa questa skill per distribuire le comunicazioni e le scadenze.
version: 1.3.1
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: ["GAS", "gruppo acquisto solidale", "communications"]
    category: GAS
required_environment_variables:
  - name: BRAIN_ROOT_PATH
    prompt: Where is the root of the BRAIN knowledge base?
    help: Path to the BRAIN knowledge base directory
    required_for: full functionality
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
   - Converti il contenuto del bollettino dal formato Markdown al formato HTML seguendo queste regole:
     - Ignora le linee orizzontali (es. `---` o simili).
     - Converti i normali elementi Markdown (titoli, liste, grassetto, a capo) nei rispettivi tag HTML.
     - **Tabelle**: trasformale in liste non ordinate (`<ul>`).
       - Le righe diventano elementi della lista (`<li>`), concatenando il contenuto delle diverse colonne della stessa riga.
   - Usa la skill `gas-agentmail` per inviare un'email.
   - **Destinatario**: `info@rainbowbreeze.it`
   - **Oggetto**: "Aggiornamenti GAS del [giorno] [Mese]" (es. "Aggiornamenti GAS del 20 Agosto").
   - **Corpo del messaggio**: Il contenuto del bollettino convertito in formato HTML.
   - **Gestione Errori**: Se la skill `gas-agentmail` restituisce un errore durante l'invio, interrompi l'esecuzione e mostra un messaggio di errore esplicito.

3. **Post-Invio**:
   - Lascia il file del bollettino inalterato nella sua posizione originale. Non cancellarlo o spostarlo.
