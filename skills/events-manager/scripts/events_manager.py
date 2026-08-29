#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re
from datetime import datetime
def lint_events(data: list) -> list:
    """Core linting logic that checks an in-memory list of events for consistency."""
    errors = []
    if not isinstance(data, list):
        return [f"Database must be a JSON array, got {type(data).__name__}"]
        
    slugs = set()
    urls = set()
    
    required_fields = ["slug", "titolo", "data_inizio", "data_fine", "luogo", "fonte_url", "descrizione"]
    
    for i, event in enumerate(data):
        if not isinstance(event, dict):
            errors.append(f"Event at index {i} is not an object.")
            continue
            
        # Check required fields
        for field in required_fields:
            if not event.get(field) or not str(event[field]).strip():
                errors.append(f"Event at index {i} (slug: {event.get('slug', 'UNKNOWN')}) is missing or has empty required field: '{field}'")
                
        slug = event.get("slug", "")
        url = event.get("fonte_url", "")
        
        # Check uniqueness
        if slug:
            if slug in slugs:
                errors.append(f"Duplicate slug found: '{slug}' at index {i}")
            slugs.add(slug)
            
        if url:
            if url in urls:
                errors.append(f"Duplicate fonte_url found: '{url}' at index {i}")
            urls.add(url)
            
        # Check date logical consistency
        data_inizio = event.get("data_inizio")
        data_fine = event.get("data_fine")
        
        start_dt = None
        end_dt = None
        
        if data_inizio:
            try:
                start_dt = datetime.strptime(data_inizio, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Event at index {i} has invalid data_inizio format: '{data_inizio}'. Expected YYYY-MM-DD.")
                
        if data_fine:
            try:
                end_dt = datetime.strptime(data_fine, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Event at index {i} has invalid data_fine format: '{data_fine}'. Expected YYYY-MM-DD.")
                
        if start_dt and end_dt and start_dt > end_dt:
            errors.append(f"Event at index {i} has data_inizio ({data_inizio}) after data_fine ({data_fine}).")

    return errors

def generate_slug(title: str, start_date: str) -> str:
    """Generate a kebab-case slug from start date (YYYYMMDD) and title."""
    date_formatted = start_date.replace("-", "")
    title_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    slug = f"{date_formatted}-{title_slug}"
    return slug

def get_db_path(category: str) -> str:
    """Determine the database path based on the BRAIN_EVENTSDB_PATH env var and category."""
    base_path = os.environ.get("BRAIN_EVENTSDB_PATH")
    if not base_path:
        print("Error: BRAIN_EVENTSDB_PATH environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    
    # Fallback to default if category is somehow empty
    if not category:
        category = "default"
        
    return os.path.join(base_path, category, "events.json")

def load_events(db_path: str) -> list:
    """Load events from the JSON file."""
    if not os.path.exists(db_path):
        return []
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: The file {db_path} is not valid JSON. Starting fresh.", file=sys.stderr)
        return []

def save_events(db_path: str, events: list):
    """Save events to the JSON file after linting them for consistency."""
    errors = lint_events(events)
    if errors:
        print("Error: In-memory database failed consistency linting. Aborting save.", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)
        
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

def cmd_add(args):
    """Handle the 'add' operation mode."""
    # Strict validation of date format
    try:
        datetime.strptime(args.start_date, "%Y-%m-%d")
        datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be strictly in YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)
        
    db_path = get_db_path(args.category)
    events = load_events(db_path)
    
    slug = generate_slug(args.title, args.start_date)
    
    # Deduplication check: slug OR url
    for event in events:
        if event.get("slug") == slug or event.get("fonte_url") == args.url:
            print(f"Error: Event already exists (matching slug or url). Slug: {event.get('slug')}", file=sys.stderr)
            sys.exit(1)
            
    new_event = {
        "slug": slug,
        "titolo": args.title,
        "data_inizio": args.start_date,
        "data_fine": args.end_date,
        "luogo": args.location,
        "descrizione": args.description,
        "fonte_url": args.url
    }
    
    events.append(new_event)
    save_events(db_path, events)
    print(f"Event was added successfully. Slug: {slug}")

def cmd_remove(args):
    """Handle the 'remove' operation mode."""
    db_path = get_db_path(args.category)
    events = load_events(db_path)
    
    # Derive the target slug
    if args.slug:
        target_slug = args.slug
    elif args.title and args.start_date:
        target_slug = generate_slug(args.title, args.start_date)
    else:
        print("Error: Must provide either --slug OR both --title and --start-date to remove an event.", file=sys.stderr)
        sys.exit(1)
        
    initial_count = len(events)
    events = [e for e in events if e.get("slug") != target_slug]
    
    if len(events) == initial_count:
        print(f"Error: Event with slug '{target_slug}' could not be found.", file=sys.stderr)
        sys.exit(1)
        
    save_events(db_path, events)
    print(f"Event '{target_slug}' successfully removed.")

def cmd_query(args):
    """Handle the 'query' operation mode."""
    try:
        query_start = datetime.strptime(args.start_date, "%Y-%m-%d")
        query_end = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be strictly in YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)
        
    db_path = get_db_path(args.category)
    events = load_events(db_path)
    
    matching_events = []
    for event in events:
        try:
            ev_start = datetime.strptime(event.get("data_inizio"), "%Y-%m-%d")
            ev_end = datetime.strptime(event.get("data_fine"), "%Y-%m-%d")
        except (ValueError, TypeError):
            continue # Skip events with badly formatted dates
            
        # An event overlaps with the query range if its start date is before the query end 
        # AND its end date is after the query start.
        if ev_start <= query_end and ev_end >= query_start:
            matching_events.append(event)
            
    # Output JSON directly to stdout
    print(json.dumps(matching_events, indent=2, ensure_ascii=False))

def cmd_archive(args):
    """Handle the 'archive' operation mode."""
    try:
        cutoff_date = datetime.strptime(args.before_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be strictly in YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)
        
    db_path = get_db_path(args.category)
    archive_path = db_path.replace("events.json", "events_archive.json")
    
    events = load_events(db_path)
    archive_events = load_events(archive_path)
    
    active_events = []
    moved_count = 0
    
    for event in events:
        try:
            ev_end = datetime.strptime(event.get("data_fine"), "%Y-%m-%d")
        except (ValueError, TypeError):
            # If we can't parse the end date, keep it in active
            active_events.append(event)
            continue
            
        if ev_end < cutoff_date:
            archive_events.append(event)
            moved_count += 1
        else:
            active_events.append(event)
            
    if moved_count > 0:
        save_events(db_path, active_events)
        save_events(archive_path, archive_events)
        
    print(f"Archived {moved_count} events that ended before {args.before_date}.")

def main():
    parser = argparse.ArgumentParser(description="Local Events Manager CLI")
    parser.add_argument("--category", type=str, default="default", help="Event category (sub-directory). Defaults to 'default'.")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 'add' command
    parser_add = subparsers.add_parser("add", help="Add a new event")
    parser_add.add_argument("--title", required=True, help="Title of the event")
    parser_add.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser_add.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    parser_add.add_argument("--description", required=True, help="Description of the event")
    parser_add.add_argument("--url", required=True, help="Source URL")
    parser_add.add_argument("--location", required=True, help="Location/Venue")
    parser_add.set_defaults(func=cmd_add)
    
    # 'remove' command
    parser_remove = subparsers.add_parser("remove", help="Remove an event")
    parser_remove.add_argument("--slug", required=False, help="Target slug to remove")
    parser_remove.add_argument("--title", required=False, help="Title of the event (used with --start-date to derive slug)")
    parser_remove.add_argument("--start-date", required=False, help="Start date (YYYY-MM-DD) (used with --title to derive slug)")
    parser_remove.set_defaults(func=cmd_remove)
    
    # 'query' command
    parser_query = subparsers.add_parser("query", help="Query events by date range")
    parser_query.add_argument("--start-date", required=True, help="Query start date (YYYY-MM-DD)")
    parser_query.add_argument("--end-date", required=True, help="Query end date (YYYY-MM-DD)")
    parser_query.set_defaults(func=cmd_query)
    
    # 'archive' command
    parser_archive = subparsers.add_parser("archive", help="Archive past events")
    parser_archive.add_argument("--before-date", required=True, help="Archive events ending before this date (YYYY-MM-DD)")
    parser_archive.set_defaults(func=cmd_archive)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
