import json
import os
import sys
from datetime import datetime

# Path assoluti basati sulla configurazione del GAS
BRAIN_PATH = os.path.expandvars("${BRAIN_ROOT_PATH}/ordini")
CORRENTI_FILE = os.path.join(BRAIN_PATH, "correnti.json")
STORICO_FILE = os.path.join(BRAIN_PATH, "storico.json")

def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def insert_order(order_data):
    """Inserisce un nuovo ordine nella sezione 'aperti'."""
    correnti = load_json(CORRENTI_FILE, {"aperti": [], "chiusi_in_attesa_consegna": [], "problemi_segnalati": []})
    correnti["aperti"].append(order_data)
    save_json(CORRENTI_FILE, correnti)
    return f"Ordine per '{order_data.get('Fornitore')}' inserito con successo in 'aperti'."

def archive_expired():
    """Sposta gli ordini con Data Consegna passata dallo stato corrente allo storico."""
    correnti = load_json(CORRENTI_FILE, {"aperti": [], "chiusi_in_attesa_consegna": [], "problemi_segnalati": []})
    storico = load_json(STORICO_FILE, [])
    
    today = datetime.now().strftime("%Y-%m-%d")
    new_chiusi = []
    to_archive = []
    
    # Gli ordini in attesa di consegna vengono archiviati se la data è passata
    for order in correnti.get("chiusi_in_attesa_consegna", []):
        delivery_date = order.get("Data Consegna")
        if delivery_date and delivery_date < today:
            to_archive.append(order)
        else:
            new_chiusi.append(order)
            
    if to_archive:
        correnti["chiusi_in_attesa_consegna"] = new_chiusi
        storico.extend(to_archive)
        save_json(CORRENTI_FILE, correnti)
        save_json(STORICO_FILE, storico)
        return f"Storicizzati {len(to_archive)} ordini (consegna precedente al {today})."
    return "Nessun ordine scaduto da storicizzare."

def delete_order(fornitore):
    """Elimina un ordine corrente per un determinato fornitore senza storicizzarlo."""
    correnti = load_json(CORRENTI_FILE, {"aperti": [], "chiusi_in_attesa_consegna": [], "problemi_segnalati": []})
    deleted_count = 0
    for section in ["aperti", "chiusi_in_attesa_consegna", "problemi_segnalati"]:
        initial_len = len(correnti[section])
        correnti[section] = [o for o in correnti[section] if o.get("Fornitore") != fornitore]
        deleted_count += (initial_len - len(correnti[section]))
            
    if deleted_count > 0:
        save_json(CORRENTI_FILE, correnti)
        return f"Eliminati {deleted_count} ordini per il fornitore '{fornitore}'."
    return f"Nessun ordine trovato per il fornitore '{fornitore}' nelle sezioni correnti."

def check_deadlines():
    """Ritorna un dizionario con gli ordini che hanno scadenze (chiusura o consegna) oggi o domani."""
    correnti = load_json(CORRENTI_FILE, {"aperti": [], "chiusi_in_attesa_consegna": [], "problemi_segnalati": []})
    today = datetime.now().strftime("%Y-%m-%d")
    
    deadlines = {"oggi": [], "prossime": []}
    
    for section in ["aperti", "chiusi_in_attesa_consegna"]:
        for order in correnti.get(section, []):
            dates = {
                "Chiusura": order.get("Data Chiusura"),
                "Consegna": order.get("Data Consegna")
            }
            for label, date in dates.items():
                if not date or date == "Da definire":
                    continue
                if date == today:
                    deadlines["oggi"].append({"Fornitore": order["Fornitore"], "Tipo": label, "Data": date})
                elif date and date > today:
                    try:
                        # Inseriamo solo le scadenze imminenti (es. nei prossimi 3 giorni)
                        delta = (datetime.strptime(date, "%Y-%m-%d") - datetime.now()).days
                        if delta <= 3:
                            deadlines["prossime"].append({"Fornitore": order["Fornitore"], "Tipo": label, "Data": date})
                    except ValueError:
                        continue
    
    return json.dumps(deadlines, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage active and archived orders for GAS.")
    subparsers = parser.add_subparsers(dest="action", required=True, help="Action to perform")
    
    # insert
    parser_insert = subparsers.add_parser("insert", help="Insert a new order")
    parser_insert.add_argument("--data", required=True, help="Order JSON data string")
    
    # archive
    parser_archive = subparsers.add_parser("archive", help="Archive expired orders")
    
    # delete
    parser_delete = subparsers.add_parser("delete", help="Delete an order by supplier name")
    parser_delete.add_argument("--fornitore", required=True, help="Name of the supplier to delete")
    
    # check
    parser_check = subparsers.add_parser("check", help="Check for impending deadlines")
    
    args = parser.parse_args()
    
    try:
        if args.action == "insert":
            order_data = json.loads(args.data)
            print(insert_order(order_data))
        elif args.action == "archive":
            print(archive_expired())
        elif args.action == "delete":
            print(delete_order(args.fornitore))
        elif args.action == "check":
            print(check_deadlines())
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
