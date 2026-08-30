---
name: gas-process-updates
description: Processa i nuovi aggiornamenti del GAS dalle email, aggiorna il BRAIN, elimina le email elaborate e genera un riepilogo. Usa questa skill per gestire comunicazioni e ordini del GAS.
version: 1.2.0
author: Rainbowbreeze
license: MIT
metadata:
  hermes:
    tags: ["GAS", "gruppo acquisto solidale", "community management"]
    category: GAS
    config:
      - key: BRAIN_ROOT_PATH
        description: "Path to the BRAIN knowledge base directory"
        default: "/opt/data/BRAIN"
        prompt: "Where is the root of the BRAIN knowledge base?"
---

# 🔄 Process GAS Updates

## Trigger
Usa questa skill regolarmente (es. tramite cron job) o quando l'utente richiede esplicitamente di controllare le nuove email, processare gli ordini del GAS o aggiornare il BRAIN con le ultime comunicazioni.

Questa skill definisce il flusso di lavoro per elaborare le comunicazioni in arrivo dalla mailing list del GAS e mantenere sincronizzata la base di conoscenza `BRAIN`.

## Reference Files
- `references/brain-structure.md`: Detailed map and rules for the `${BRAIN_ROOT_PATH}/` knowledge base.
- `assets/template-fornitore.md`: Template for new suppliers.
- `assets/template-membro.md`: Template for new members.

## 📦 Gestione Ordini (Deterministica)
La gestione degli ordini è automatizzata tramite lo script `scripts/order_manager.py`.
- **Azioni supportate**: `insert`, `archive`, `delete`, `check`.
- **Percorso script**: `scripts/order_manager.py`.
- **Esecuzione**: Usa sempre `python3`.
- **Esempi di utilizzo**:
  - **Inserimento**: `python3 scripts/order_manager.py insert --data '{"Fornitore": "...", "Referente": "...", ...}'`
  - **Archiviazione (scaduti)**: `python3 scripts/order_manager.py archive`
  - **Cancellazione (errore)**: `python3 scripts/order_manager.py delete --fornitore "Nome Fornitore"`
  - **Controllo Scadenze**: `python3 scripts/order_manager.py check` (Ritorna JSON con scadenze "oggi" e "prossime").

Gli ordini in `chiusi_in_attesa_consegna` vengono spostati in `storico.json` quando la `Data Consegna` è passata.


## 🛠️ Flusso di Lavoro

Quando attivata, esegui questi passaggi in ordine:

### 1. Recupero Nuove Email
- Usa la skill `gas-agentmail` per scaricare gli ultimi messaggi da `gastronauti@agentmail.to`.
- Leggi e analizza tutte le email non lette, in particolare quelle riguardanti ordini, consegne o informazioni sui fornitori.
- **Gestione Rumore**: Email automatiche che non contengono informazioni (es. "Oggi non hai nessun evento in programma" da Google Calendar) devono essere eliminate immediatamente per mantenere pulita la casella, senza generare aggiornamenti nel report.

### 2. Aggiornamento del BRAIN
Elabora il contenuto delle email e aggiorna la directory `BRAIN`:
- **Fornitori (`BRAIN/fornitori/`)**: Aggiorna le schede dei fornitori menzionati. Se viene menzionato un nuovo fornitore, crea una nuova scheda partendo da `assets/template-fornitore.md`. Registra problemi di qualità, note logistiche o **istruzioni post-consegna (es. pagamenti, integrazioni)** nella sezione "Note Operative".
  - **Identificazione Prodotti**: Se un'email menziona un prodotto (es. "Avena") non esplicitamente mappato in un fornitore:
    1. Esegui `grep -ri "<prodotto>" ${BRAIN_ROOT_PATH}/fornitori/` per cercare menzioni passate.
    2. Cerca il mittente in `BRAIN/membri/referenti.md` per vedere quali fornitori gestisce.
    3. Se il prodotto è generico (es. alimentari), usa il fornitore "Alimentari" principale (es. IRIS) e menziona l'assunzione nel report finale, senza chiedere chiarimenti.
  - **Mappatura Referenti**: Quando aggiungi un nuovo fornitore o modifichi un referente, aggiorna sempre `BRAIN/membri/referenti.md` per mantenere la matrice di responsabilità sincronizzata.
- **Informazioni Generali**: Se ricevi email informative (es. notifiche di calendario, avvisi di riunione), annota le date e includile nel report finale come scadenze/promemoria.
- **Referenti (`BRAIN/membri/referenti.md`)**:
  - Se viene menzionato un nuovo referente o un nuovo abbinamento fornitore-referente, aggiorna la tabella.
  - Ricordati di aggiornare anche la data di `*Ultimo aggiornamento:*` in fondo al file in caso di modifiche.
  - **CRITICO**: Se un membro lascia il gruppo o abbandona un ruolo di referente, rimuovilo da `referenti.md` e aggiorna tutte le schede fornitore in `BRAIN/fornitori/` in cui era indicato, impostando il referente come "Da definire".
- **Ordini (`BRAIN/ordini/`)**:
  - Aggiorna `BRAIN/ordini/correnti.json` con nuovi ordini o cambiamenti di stato (Apertura, Chiusura, Consegna).
  - **Ambiguità Ordini**: Se un'email aggiorna un ordine in modo vago e il referente gestisce più ordini aperti, deduci a quale ordine si riferisce basandoti sul contesto o sulla scadenza più prossima.
  - Sposta gli ordini completati in `BRAIN/ordini/storico.json`.
  - **Post-Consegna (Contabilità)**: Quando ricevi comunicazioni sui conti finali per ordini in `storico.json`, aggiorna le "Note" e la scheda fornitore seguendo questi pattern:
    - **Conguagli/Integrazioni** (es. "vi ho erroneamente restituito", "mi dovete"): Annota chi deve dare quanto nella scheda e nel report.
    - **Elenchi di Pagamento**: Riporta la lista degli importi nel report e aggiorna la scheda fornitore come storico.
    - **Metodi di Pagamento**: Verifica IBAN/Satispay. Segnala discrepanze con l'IBAN nel BRAIN come "Potenziale variazione IBAN" nel report.
- **CRITICO**: Se un ordine presenta problemi (ritardi, mancanze, errori di peso), annotalo nel JSON degli ordini **E** aggiungi il feedback nella scheda del fornitore specifico.

### 3. Generazione Report Finale
- Componi un report testuale dettagliato, conciso e amichevole in italiano (Persona: GAStronAI).
- **Continuità**: Controlla gli ultimi report in `/opt/data/cron/output/` per assicurarti di non ripetere informazioni già inviate o per dare seguito a promesse fatte nel run precedente.
- **Formattazione**:
    - Usa **molte emoji** per migliorare la leggibilità e dare un tono comunitario (es. 🚚, 🍎, 🛑, 🚨).
    - Suddividi il report in sezioni chiare (es. "🚨 SCADENZE DI OGGI", "📅 PROSSIME SCADENZE", "📧 AGGIORNAMENTI DAI SOCI").
    - **CRITICO**: Controlla le scadenze usando `python3 scripts/order_manager.py check`. Prima di generare il report, esegui sempre l'archiviazione degli ordini passati con `python3 scripts/order_manager.py archive`. 
    - **NOTA**: Lo script `archive` sposta solo gli ordini con `Data Consegna` strettamente minore della data odierna. Se un'email conferma la consegna avvenuta **oggi**, devi spostare manualmente l'ordine da `correnti.json` a `storico.json` e aggiornare la scheda fornitore per riflettere lo stato nel report.
    - Se ci sono scadenze **OGGI**, mettile **in cima** al messaggio con emoji vistose (es. 🚨, 📅).
    - Non usare tabelle per lo "Stato Ordini Correnti". Usa invece **elenchi puntati raggruppati per stato**, mettendo PRIMA gli ordini aperti e POI quelli in attesa di consegna. Esempio:
      🛒 **Aperti**
      - Avicola (Luigi) - Scadenza: 05/09
      📦 **In Attesa di Consegna**
      - IRIS (Mario) - Scadenza: 01/09
- **Contenuto**:
    - Riepilogo delle email processate ed eliminate.
    - Elenco delle modifiche effettuate ai file nel `BRAIN`. Usa `find ${BRAIN_ROOT_PATH} -mmin -[minuti_sessione]` per identificare rapidamente i file toccati.
    - **Stato Ordini**: Elenca sempre tutti gli ordini presenti in `BRAIN/ordini/correnti.json` con relativo stato e referenti.
    - **Feedback Post-Consegna**: Se un ordine è appena stato consegnato (oggi o ieri), controlla se ci sono nuove informazioni sui pagamenti o problemi nelle email e aggiorna sia la scheda fornitore che `storico.json`.
- **Creazione Bulletin**:
    - Oltre al report generale, genera una versione "pubblica" del report che includa SOLO scadenze, stato ordini e comunicazioni (escludendo il riepilogo delle email eliminate e dei file modificati).
    - Aggiungi (append) questo report pubblico in coda al file `${BRAIN_ROOT_PATH}/bulletin/YYYY-MM-DD-bulletin.md` (es. `2026-08-30-bulletin.md`).
    - Crea la cartella `bulletin` e il file se non esistono. Se il file esiste già per la giornata odierna, separa i nuovi aggiornamenti con una linea orizzontale (`---`).
- **Delivery (Cron)**: Se la skill determina che non c'è nulla da segnalare (nessun aggiornamento e nessun ordine corrente), rispondi esattamente con `[SILENT]`. L'agente chiamante deve rispettare questo segnale e non produrre output.

### 4. Eliminazione Email Elaborate
- **CRITICO**: Elimina i thread corrispondenti dall'inbox di AgentMail SOLO DOPO aver generato con successo il report finale. Questo previene la perdita di dati in caso di crash durante la stesura.
- **IMPORTANTE**: Non inviare MAI email di risposta o nuove email in questo processo.

## ⚠️ Pitfalls
- **Cancellazione Eventi**: Le email automatiche di "Evento Annullato" NON sono rumore. Devono essere segnalate nel report finale per avvisare i soci del cambio di programma, anche se non richiedono modifiche al BRAIN.
- **Patching e Paginazione**: Se un file (come `referenti.md`) è stato letto con `offset` e `limit`, il tool `patch` potrebbe avvertire che la vista è parziale. Assicurati che `old_string` sia unico e contenga contesto sufficiente, o rileggi il file per intero se necessario prima di applicare modifiche.
- **Tabelle Markdown**: Durante l'uso di `patch` su tabelle Markdown, presta estrema attenzione ai separatori `|`. Un errore nel match può portare alla duplicazione dei bordi (es. `||`).
- **Dettagli Email**: Il comando `list` di `mail_manager.py` fornisce solo snippet. Per estrarre informazioni precise (date, nomi, IBAN), usa sempre `get-message` con l'ID del messaggio.
- **Email Informative**: Non ignorare le email di calendario o riunioni; estrai le date e inseriscile come "Promemoria" o "Scadenze" nel report finale prima di eliminare il thread.
- **Python Path**: Use `python3` for execution of internal scripts (e.g. `order_manager.py`). For scripts with external dependencies like `agentmail`, use `uv run --with <package>` if they are missing from the venv.
- **Thread Deletion**: Ensure the `delete` command is used with the explicit flag `--thread_id <id>` (it is not a positional argument). Note that the current `mail_manager.py` wrapper handles permanent deletion without requiring an extra flag.
- **Absolute Paths**: Utilize `${BRAIN_ROOT_PATH}/` for all file operations to ensure reliability.
- **Tracking Modifiche**: Per riportare le modifiche al BRAIN, confronta lo stato attuale con quello all'inizio della sessione o usa `find ${BRAIN_ROOT_PATH} -mmin -[minuti_sessione]` come euristica.
