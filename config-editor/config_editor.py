#!/usr/bin/env python3
"""
Configuration Editor Script
Edits configuration files by inserting or replacing a block of text identified by an edit ID.
"""

import os
import sys
import argparse
import configparser
import re

# Add abundant comments in the source file as requested by user rule.

def get_markers(filepath, edit_id):
    """
    Returns the appropriate begin and end markers based on the file extension.
    Supported extensions: .yml, .env, .json, .md
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.yml', '.yaml', '.env', '.conf', '.sh', '.py']:
        return f"# BEGIN {edit_id}", f"# END {edit_id}"
    elif ext in ['.json', '.js', '.ts']:
        return f"// BEGIN {edit_id}", f"// END {edit_id}"
    elif ext in ['.md', '.html', '.xml']:
        return f"<!-- BEGIN {edit_id} -->", f"<!-- END {edit_id} -->"
    else:
        # Default to '#' if unknown
        return f"# BEGIN {edit_id}", f"# END {edit_id}"

def process_file(filepath, edit_id, config_content):
    """
    Reads the file, looks for the edit ID block.
    If it exists, replaces it with the new content.
    If not, appends the new content to the end of the file.
    """
    begin_marker, end_marker = get_markers(filepath, edit_id)
    
    core_block = f"{begin_marker}\n{config_content.strip('\n')}\n{end_marker}"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        # Insert error handling block as requested by user rule.
        print(f"- Error reading file {filepath}: {e}")
        return False

    escaped_begin = re.escape(begin_marker)
    escaped_end = re.escape(end_marker)
    
    # Match just the block itself without consuming surrounding whitespace
    pattern = re.compile(rf"{escaped_begin}.*?{escaped_end}", re.DOTALL)
    
    if pattern.search(content):
        print(f"- Updating existing block in: {filepath}")
        new_content = pattern.sub(core_block, content)
    else:
        print(f"- Appending new block to: {filepath}")
        if content:
            if not content.endswith('\n'):
                content += '\n\n'
            elif not content.endswith('\n\n'):
                content += '\n'
        new_content = content + core_block + '\n\n'
        
    # Add a newline after the edited block (at EOF) only if not already present
    if not new_content.endswith('\n'):
        new_content += '\n'

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        # Insert error handling block
        print(f"- Error writing to file {filepath}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Edit configuration files based on a text input file.")
    parser.add_argument("input_config", help="Path to the text file containing the edit configuration.")
    parser.add_argument("search_dir", help="Directory where to start the search.")
    parser.add_argument("-r", dest="recursive", action="store_true", help="Enable recursive search into subdirectories.")
    
    args = parser.parse_args()
    
    input_config_path = args.input_config
    search_dir = args.search_dir
    
    # Check if the input file exists
    if not os.path.isfile(input_config_path):
        print(f"Error: Input configuration file not found: {input_config_path}", file=sys.stderr)
        sys.exit(1)
        
    # Check if the directory exists
    if not os.path.isdir(search_dir):
        print(f"Error: Search directory not found: {search_dir}", file=sys.stderr)
        sys.exit(1)
        
    # Parse the custom text format file
    target_filename = None
    edit_id = None
    content_lines = []
    in_config_content = False
    
    try:
        with open(input_config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            if in_config_content:
                if line.strip() == '```':
                    break  # End of payload block
                content_lines.append(line)
                continue
                
            stripped = line.strip()
            if stripped.startswith('filename') and '=' in stripped:
                target_filename = stripped.split('=', 1)[1].strip()
            elif stripped.startswith('edit_id') and '=' in stripped:
                edit_id = stripped.split('=', 1)[1].strip()
            elif stripped == '```':
                in_config_content = True
                
        if not target_filename or not edit_id or not content_lines:
            raise ValueError("Missing 'filename', 'edit_id', or valid '```' block in input file.")
            
        config_content = "".join(content_lines)
    except Exception as e:
        print(f"Error parsing input file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Target filename: {target_filename}")
    print(f"Edit ID: {edit_id}")
    print(f"Starting search in: {search_dir}")

    files_modified = 0
    # Walk through the directory
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file == target_filename:
                filepath = os.path.join(root, file)
                if process_file(filepath, edit_id, config_content):
                    files_modified += 1
                    
        # If recursive flag is NOT set, clear dirs to prevent descending into subdirectories
        if not args.recursive:
            dirs.clear()

    print(f"Process complete. Modified {files_modified} file(s).")
    print()

if __name__ == "__main__":
    main()
