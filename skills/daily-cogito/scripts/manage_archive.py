import os
import sys
import json
import random
import argparse
from datetime import datetime, timezone

def get_archive_path():
    path = os.environ.get("BRAIN_WISDOMDB_PATH")
    if not path:
        print("Error: BRAIN_WISDOMDB_PATH environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return path

def load_archive(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Malformed JSON in archive file at {path}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading archive file: {e}", file=sys.stderr)
        sys.exit(1)

def save_archive(path, data):
    # Ensure directory exists
    dir_path = os.path.dirname(os.path.abspath(path))
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
        
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to archive file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Manage the Daily Cogito thoughts archive.
    Provides functionality to add new thoughts or retrieve a random one.
    """
    parser = argparse.ArgumentParser(description="Manage the Daily Cogito thoughts archive.")
    parser.add_argument('--action', required=True, choices=['add', 'random', 'check'], help="Action to perform.")
    parser.add_argument('--body', type=str, help="Body of the thought (required for 'add' action).")
    parser.add_argument('--url', type=str, default="", help="Source URL of the thought (optional for 'add' action).")
    
    args = parser.parse_args()
    archive_path = get_archive_path()

    if args.action == 'add':
        if not args.body:
            print("Error: --body is required when action is 'add'.", file=sys.stderr)
            sys.exit(1)
        
        archive = load_archive(archive_path)
        new_thought = {
            "submission_date": datetime.now(timezone.utc).isoformat(),
            "body": args.body,
            "url": args.url
        }
        archive.append(new_thought)
        save_archive(archive_path, archive)
        print("Thought successfully added to the archive.")
        
    elif args.action == 'random':
        archive = load_archive(archive_path)
        if not archive:
            print("Error: The archive is empty or does not exist.", file=sys.stderr)
            sys.exit(1)
        
        thought = random.choice(archive)
        # Exclude submission date in the stdout printout, keeping it simple for the LLM to read
        print(f"Body:\n{thought.get('body', '')}\n")
        if thought.get('url'):
            print(f"URL: {thought.get('url')}")

    elif args.action == 'check':
        if not args.url:
            print("Error: --url is required when action is 'check'.", file=sys.stderr)
            sys.exit(1)
            
        archive = load_archive(archive_path)
        for thought in archive:
            if thought.get('url') == args.url:
                print("EXISTS")
                return
        print("NOT_FOUND")

if __name__ == '__main__':
    main()
