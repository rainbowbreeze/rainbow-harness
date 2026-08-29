#!/usr/bin/env python3
import json
import sys
import argparse
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

def lint_db_file(db_path: str) -> list:
    """Reads a database file from disk and lints it."""
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return [f"File not found: {db_path}"]
    except json.JSONDecodeError as e:
        return [f"Invalid JSON in {db_path}: {str(e)}"]
        
    return lint_events(data)

def main():
    parser = argparse.ArgumentParser(description="Lint the Events JSON Database")
    parser.add_argument("db_path", help="Path to the events.json file")
    args = parser.parse_args()
    
    errors = lint_db_file(args.db_path)
    if errors:
        print(f"Linting failed for {args.db_path}:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Linting passed for {args.db_path}. Database is consistent.")
        sys.exit(0)

if __name__ == "__main__":
    main()
