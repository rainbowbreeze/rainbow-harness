---
name: health-records
description: "Gestione del fascicolo sanitario nel BRAIN per i membri della famiglia: quadro clinico, cronologia medica e referti."
version: 1.1.0
author: Rainbowbreeze
metadata:
  hermes:
    tags: [health, medical, tracker, referti]
    category: health
    config:
      - key: BRAIN_HEALTHRECORDS_PATH
        description: "Path to store the health records files"
        default: "/opt/data/BRAIN/fascicolo-sanitario"
        prompt: "Where can I store the medical health records of your family?"
---

# Gestione Fascicolo Sanitario

## Quando attivare questa skill
Usa questa skill quando l'utente fornisce informazioni mediche, referti di analisi, referti fotografici, sintomi, terapie o aggiornamenti sullo stato di salute per sé o per un membro della famiglia.

## Struttura del progetto BRAIN
Il fascicolo sanitario è situato in `$BRAIN_HEALTHRECORDS_PATH/<nome-cognome>/`.
Ogni cartella contiene:
- `quadro_clinico.md`: Fotografia attuale dello stato di salute (aggiornato con le ultime novità).
- `cronologia.md`: Diario clinico sequenziale (ordine cronologico inverso).
- `referti/`: Cartella contenente i documenti medici salvati e le immagini.

## Procedura Operativa

1. **Salvataggio Referti (se presenti):**
   - Se l'utente fornisce un documento o un'immagine, salvala fisicamente nella cartella `referti/` del membro interessato.
   - Nomenclatura: `YYYYMMDD-nomereferto.ext` (es. `20260715-emocromo.pdf`).
   - *Nota bene:* La data `YYYYMMDD` deve corrispondere alla data dell'evento/esame (leggi la data dal referto, o dall'EXIF se indicato), non necessariamente quella dell'inserimento.

2. **Aggiornamento Cronologia (`cronologia.md`):**
   - Aggiungi una voce in cima alla lista degli eventi.
   - Usa questo formato:
     ```markdown
     ### DD Mese YYYY - [Titolo Evento/Esame]
     - **Sintesi:** [Riassunto dei risultati o del sintomo]
     - **Referto:** [Se applicabile, inserisci il link relativo: `[Nome Referto](referti/YYYYMMDD-nome.ext)`]
     - **Azione:** [Se ha richiesto variazioni terapeutiche o aggiornamenti del quadro clinico]
     ```

3. **Aggiornamento Quadro Clinico (`quadro_clinico.md`):**
   - Valuta se le nuove informazioni modificano il quadro clinico generale (es. allergie scoperte, condizioni croniche, parametri vitali come colesterolo/pressione/peso, o nuove terapie).
   - Se c'è una variazione, modifica direttamente il file `quadro_clinico.md` sovrascrivendo i dati vecchi e mantenendo i valori più recenti.
   - Aggiungi sempre un link testuale Markdown al referto che giustifica il dato aggiornato.
