---
name: gas-agentmail
description: "Gestione email per il GAS GAStronauti tramite AgentMail. Permette di leggere, inviare e cancellare email dalla casella gastronauti@agentmail.to."
version: 1.0.0
license: MIT
author: Rainbowbreeze
metadata:
  hermes:
    tags: ["GAS", "gruppo acquisto solidale", "community management", "email", "agentmail.to"]
    category: GAS
    config:
      - key: AGENTMAIL_GASTRONAUTI_API_KEY
        description: "API KEY per gestire la casella di posta dei GAStronauti"
        default: "ADD_ME"
        prompt: "Qual'è la API KEY per accedere alla casella di posta su agentmail?"
---

# AgentMail GAStronauti

Questa skill permette a GAStronAI di gestire la corrispondenza del GAS utilizzando le API di AgentMail.

## Pitfalls & SDK Quirks
The `agentmail` Python SDK has specific attribute naming conventions (e.g., `from_` instead of `from_email`). Consult `references/sdk-quirks.md` for a full list of troubleshooting tips and attribute mappings.

## Reference Files
- `references/sdk-quirks.md`: Essential attribute mappings and debugging for the AgentMail SDK.

## Comandi Disponibili

> [!TIP]
> Se l'ambiente non ha il pacchetto `agentmail` installato nel venv predefinito, usa `uv run --with agentmail` per eseguirlo in un ambiente isolato con le dipendenze necessarie.

### Lettura Email
Per visualizzare le ultime email ricevute:
```bash
uv run --with agentmail scripts/mail_manager.py list --limit 10
```
> [!IMPORTANT]
> Il comando `list` restituisce solo un'anteprima (snippet) del testo. Per estrarre IBAN, tabelle prezzi o dettagli di eventi, usa SEMPRE `get-message` con l'ID specifico.

### Lettura Singolo Messaggio
Per visualizzare il contenuto completo di un messaggio (necessario per estrarre IBAN o tabelle):
```bash
uv run --with agentmail scripts/mail_manager.py get-message --message_id "<ID_MESSAGGIO>"
```

### Invio Email
Per inviare una nuova email a un fornitore o referente:
```bash
uv run --with agentmail scripts/mail_manager.py send --to "email@esempio.com" --subject "Oggetto" --text "Corpo del messaggio"
```

### Cancellazione Thread
Per rimuovere un thread di email dopo che è stato processato:
```bash
uv run --with agentmail scripts/mail_manager.py delete --thread_id "TH_..."
```
> [!NOTE]
> Se `list` mostra più messaggi con lo stesso `thread_id` (una conversazione con più risposte), basta eseguire `delete` una sola volta su quel `thread_id` per eliminare l'intero scambio.

## Flusso di Lavoro Consigliato
1. Usare `list` per controllare nuovi ordini o comunicazioni dai fornitori.
2. **Noise Reduction**: Eliminare immediatamente email automatiche irrilevanti (es. avvisi di calendario vuoto) per mantenere la casella pulita.
3. Analizzare il contenuto e aggiornare il BRAIN se necessario.
3. Rispondere o inviare solleciti con `send`.
4. Una volta completata la gestione di una pratica, usare `delete` per mantenere la casella pulita.
