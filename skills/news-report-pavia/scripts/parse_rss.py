#!/usr/bin/env python3
"""
RSS Feed Parser for Pavia News
==============================
This script reads the news sources from the assets/news-sources.json file,
fetches their RSS feeds, and extracts articles published within the last 24 hours.

It uses only Python standard libraries to avoid external dependencies.
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

def parse_rss(url):
    """
    Fetches and parses an RSS feed from the given URL.
    
    Args:
        url (str): The URL of the RSS feed.
        
    Returns:
        list: A list of dictionaries representing the articles.
    """
    try:
        # Create a request with a User-Agent to prevent 403 Forbidden errors
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Fetch the RSS feed with a 10-second timeout
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
        except urllib.error.URLError as url_err:
            print(f"URL Error when fetching {url}: {url_err}", file=sys.stderr)
            return []
        except Exception as fetch_err:
            print(f"Network error when fetching {url}: {fetch_err}", file=sys.stderr)
            return []
            
        # Parse the XML content
        try:
            root = ET.fromstring(content)
        except ET.ParseError as parse_err:
            print(f"XML Parsing Error for {url}: {parse_err}", file=sys.stderr)
            return []
            
        items = []
        now = datetime.now(timezone.utc)
        twenty_four_hours_ago = now - timedelta(hours=24)
        
        # Iterate through all <item> tags in the RSS feed
        for item in root.findall('.//item'):
            try:
                title_el = item.find('title')
                link_el = item.find('link')
                pubdate_el = item.find('pubDate')
                desc_el = item.find('description')
                
                # Skip items that are missing essential fields
                if title_el is None or link_el is None or pubdate_el is None:
                    continue
                    
                title = title_el.text
                link = link_el.text
                pubdate_str = pubdate_el.text
                desc = desc_el.text if desc_el is not None else ""
                
                # Attempt to parse the publication date
                try:
                    pubdate = parsedate_to_datetime(pubdate_str)
                    # Normalize to UTC time
                    if pubdate.tzinfo is None:
                        pubdate = pubdate.replace(tzinfo=timezone.utc)
                    else:
                        pubdate = pubdate.astimezone(timezone.utc)
                except Exception as date_err:
                    print(f"Date parsing error for item '{title}': {date_err}", file=sys.stderr)
                    continue
                    
                # Only include items from the last 24 hours
                if pubdate >= twenty_four_hours_ago:
                    items.append({
                        "title": title,
                        "link": link,
                        "published": pubdate.strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "description": desc
                    })
            except Exception as item_err:
                # Handle any unexpected error while parsing a single item
                print(f"Unexpected error processing an item from {url}: {item_err}", file=sys.stderr)
                continue
                
        return items
        
    except Exception as e:
        # Catch-all for any unforeseen errors in the parse_rss function
        print(f"Critical error in parse_rss for {url}: {e}", file=sys.stderr)
        return []

def main():
    """
    Main execution flow. Reads sources, fetches RSS, and outputs JSON.
    """
    try:
        # Determine the absolute path to the assets file relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(script_dir, '..', 'assets', 'news-sources.json')
        
        # Ensure the sources file exists
        if not os.path.exists(assets_path):
            error_msg = {"error": f"Sources file not found at {assets_path}"}
            print(json.dumps(error_msg))
            sys.exit(1)
            
        # Load the JSON file safely
        try:
            with open(assets_path, 'r', encoding='utf-8') as f:
                sources = json.load(f)
        except json.JSONDecodeError as json_err:
            print(json.dumps({"error": f"Invalid JSON in {assets_path}: {json_err}"}))
            sys.exit(1)
        except Exception as io_err:
            print(json.dumps({"error": f"Error reading {assets_path}: {io_err}"}))
            sys.exit(1)
            
        all_news = {}
        
        # Iterate over each source and parse if an RSS feed is provided
        for source in sources:
            try:
                if source.get('rss'):
                    rss_url = source['rss']
                    name = source.get('name', 'Unknown Source')
                    # Parse the RSS feed and store the results
                    all_news[name] = parse_rss(rss_url)
            except Exception as source_err:
                print(f"Error processing source '{source.get('name')}': {source_err}", file=sys.stderr)
                continue
                
        # Output the aggregated news as a formatted JSON string to stdout
        print(json.dumps(all_news, indent=2, ensure_ascii=False))
        
    except Exception as main_err:
        # Ultimate catch-all for the main execution block
        print(json.dumps({"error": f"Critical error in main script execution: {main_err}"}))
        sys.exit(1)

if __name__ == '__main__':
    main()
