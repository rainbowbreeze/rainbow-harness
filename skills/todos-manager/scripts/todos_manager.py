#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re
from datetime import datetime

def lint_todos(data: list) -> list:
    """Core linting logic that checks an in-memory list of todos for consistency."""
    errors = []
    if not isinstance(data, list):
        return [f"Database must be a JSON array, got {type(data).__name__}"]
        
    slugs = set()
    
    required_fields = ["slug", "title", "description", "source"]
    
    for i, todo in enumerate(data):
        if not isinstance(todo, dict):
            errors.append(f"Todo at index {i} is not an object.")
            continue
            
        for field in required_fields:
            if not todo.get(field) or not str(todo[field]).strip():
                errors.append(f"Todo at index {i} is missing or has empty required field: '{field}'")
                
        slug = todo.get("slug", "")
        
        if slug:
            if slug in slugs:
                errors.append(f"Duplicate slug found: '{slug}' at index {i}")
            slugs.add(slug)
            
        # Check source validity
        source = todo.get("source")
        if source and source not in ["email", "user-command", "unknown"]:
            errors.append(f"Todo at index {i} has invalid source '{source}'. Must be one of: email, user-command, unknown.")
            
        # Check due date logical consistency
        due_date = todo.get("due_date")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Todo at index {i} has invalid due_date format: '{due_date}'. Expected YYYY-MM-DD.")
                
    return errors

def generate_slug(title: str, creation_date: str) -> str:
    """Generate a kebab-case slug from creation date (YYYYMMDD) and title."""
    date_formatted = creation_date.replace("-", "")
    title_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    slug = f"{date_formatted}-{title_slug}"
    return slug

def get_db_path() -> str:
    """Determine the database path based on the BRAIN_TODOSDB_PATH env var."""
    base_path = os.environ.get("BRAIN_TODOSDB_PATH")
    if not base_path:
        print("Error: BRAIN_TODOSDB_PATH environment variable is not set.", file=sys.stderr)
        sys.exit(1)
        
    return os.path.join(base_path, "todos.json")

def load_todos(db_path: str) -> list:
    """Load todos from the JSON file."""
    if not os.path.exists(db_path):
        return []
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: The file {db_path} is not valid JSON. Starting fresh.", file=sys.stderr)
        return []

def save_todos(db_path: str, todos: list):
    """Save todos to the JSON file after linting them for consistency."""
    errors = lint_todos(todos)
    if errors:
        print("Error: In-memory database failed consistency linting. Aborting save.", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)
        
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)

def cmd_add(args):
    """Handle the 'add' operation mode."""
    if args.due_date:
        try:
            datetime.strptime(args.due_date, "%Y-%m-%d")
        except ValueError:
            print("Error: due-date must be strictly in YYYY-MM-DD format.", file=sys.stderr)
            sys.exit(1)
            
    db_path = get_db_path()
    todos = load_todos(db_path)
    
    creation_date = datetime.now().strftime("%Y-%m-%d")
    slug = generate_slug(args.title, creation_date)
    
    for todo in todos:
        if todo.get("slug") == slug:
            print(f"Error: Todo already exists (matching slug). Slug: {todo.get('slug')}", file=sys.stderr)
            sys.exit(1)
            
    new_todo = {
        "slug": slug,
        "title": args.title,
        "description": args.description,
        "source": args.source
    }
    
    if args.due_date:
        new_todo["due_date"] = args.due_date
        
    todos.append(new_todo)
    save_todos(db_path, todos)
    print(f"Todo was added successfully. Slug: {slug}")

def cmd_remove(args):
    """Handle the 'remove' operation mode."""
    db_path = get_db_path()
    todos = load_todos(db_path)
    
    target_slug = args.slug
        
    initial_count = len(todos)
    todos = [t for t in todos if t.get("slug") != target_slug]
    
    if len(todos) == initial_count:
        print(f"Error: Todo with slug '{target_slug}' could not be found.", file=sys.stderr)
        sys.exit(1)
        
    save_todos(db_path, todos)
    print(f"Todo '{target_slug}' successfully removed (completed).")

def cmd_update(args):
    """Handle the 'update' operation mode."""
    db_path = get_db_path()
    todos = load_todos(db_path)
    
    target_slug = args.slug
    found = False
    
    for todo in todos:
        if todo.get("slug") == target_slug:
            if args.title is not None:
                todo["title"] = args.title
            if args.description is not None:
                todo["description"] = args.description
            if args.due_date is not None:
                if args.due_date == "":
                    todo.pop("due_date", None)
                else:
                    try:
                        datetime.strptime(args.due_date, "%Y-%m-%d")
                        todo["due_date"] = args.due_date
                    except ValueError:
                        print("Error: due-date must be strictly in YYYY-MM-DD format.", file=sys.stderr)
                        sys.exit(1)
            if args.source is not None:
                if args.source not in ["email", "user-command", "unknown"]:
                    print(f"Error: invalid source '{args.source}'. Must be one of: email, user-command, unknown.", file=sys.stderr)
                    sys.exit(1)
                todo["source"] = args.source
            
            found = True
            break
            
    if not found:
        print(f"Error: Todo with slug '{target_slug}' could not be found.", file=sys.stderr)
        sys.exit(1)
        
    save_todos(db_path, todos)
    print(f"Todo '{target_slug}' successfully updated.")

def cmd_query(args):
    """Handle the 'query' operation mode."""
    db_path = get_db_path()
    todos = load_todos(db_path)
    
    matching_todos = []
    for todo in todos:
        match = True
        if args.source and todo.get("source") != args.source:
            match = False
            
        if match:
            matching_todos.append(todo)
            
    # Output JSON directly to stdout
    print(json.dumps(matching_todos, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="Local Todos Manager CLI")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 'add' command
    parser_add = subparsers.add_parser("add", help="Add a new todo")
    parser_add.add_argument("--title", required=True, help="Title of the todo")
    parser_add.add_argument("--description", required=True, help="Description of the todo")
    parser_add.add_argument("--source", required=True, choices=["email", "user-command", "unknown"], help="Source of the todo")
    parser_add.add_argument("--due-date", required=False, help="Due date (YYYY-MM-DD)")
    parser_add.set_defaults(func=cmd_add)
    
    # 'remove' command
    parser_remove = subparsers.add_parser("remove", help="Remove (complete) a todo")
    parser_remove.add_argument("--slug", required=True, help="Target slug to remove")
    parser_remove.set_defaults(func=cmd_remove)
    
    # 'update' command
    parser_update = subparsers.add_parser("update", help="Update an existing todo")
    parser_update.add_argument("--slug", required=True, help="Target slug to update")
    parser_update.add_argument("--title", required=False, help="New title")
    parser_update.add_argument("--description", required=False, help="New description")
    parser_update.add_argument("--due-date", required=False, help="New due date (YYYY-MM-DD) or empty string to clear")
    parser_update.add_argument("--source", required=False, choices=["email", "user-command", "unknown"], help="New source")
    parser_update.set_defaults(func=cmd_update)
    
    # 'query' command
    parser_query = subparsers.add_parser("query", help="Query todos")
    parser_query.add_argument("--source", required=False, choices=["email", "user-command", "unknown"], help="Filter by source")
    parser_query.set_defaults(func=cmd_query)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
