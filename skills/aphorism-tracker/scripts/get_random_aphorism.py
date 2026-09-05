#!/usr/bin/env python3
"""
Script to extract a random aphorism from the provided JSON file.
"""

import os
import sys
import json
import random
import argparse

def main():
    # Setup argparse for standardized CLI arguments as per rules
    parser = argparse.ArgumentParser(description="Fetch a random aphorism from a JSON file.")
    # Explicit flag for the file path, making it mandatory
    parser.add_argument("--file", required=True, help="Path to the aphorisms.json file")
    
    args = parser.parse_args()
    json_file_path = args.file

    # Error Handling: Check if the file exists
    if not os.path.isfile(json_file_path):
        sys.stderr.write(f"Error: The aphorisms file was not found at {json_file_path}\n")
        sys.exit(1)

    # 1. Read and parse the JSON file
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            aphorisms = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Failed to parse JSON file at {json_file_path}. Details: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: An unexpected error occurred while reading the file. Details: {e}\n")
        sys.exit(1)

    # Error Handling: Check if the list is empty
    if not aphorisms:
        sys.stderr.write("Error: The aphorisms list is empty.\n")
        sys.exit(1)

    # 2. Extract a random aphorism
    try:
        random_entry = random.choice(aphorisms)
        
        text = random_entry.get("text", "Unknown quote")
        authors = random_entry.get("author", [])
        source = random_entry.get("source", "")
        
        author_str = ", ".join(authors) if authors else "Unknown Author"
        
        # 3. Format and print the result to stdout
        output = f'"{text}"\n- {author_str}'
        if source:
            output += f' ({source})'
            
        print(output)
        
    except Exception as e:
        sys.stderr.write(f"Error: Failed to extract or format a random aphorism. Details: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
