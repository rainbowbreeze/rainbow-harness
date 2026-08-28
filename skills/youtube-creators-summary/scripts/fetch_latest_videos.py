import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import json

import sys

def fetch_rss(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        return None

def parse_rss(xml_content):
    root = ET.fromstring(xml_content)
    ns = {'ns': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}
    videos = []
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=24)
    
    for entry in root.findall('ns:entry', ns):
        published_elem = entry.find('ns:published', ns)
        if published_elem is None: continue
        published_str = published_elem.text
        published = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        link_elem = entry.find('ns:link', ns)
        if link_elem is None: continue
        link = link_elem.attrib['href']
        
        # Skip YouTube Shorts
        if "/shorts/" in link:
            continue
            
        if published > threshold:
            media_group = entry.find('media:group', ns)
            description = media_group.find('media:description', ns).text if media_group is not None and media_group.find('media:description', ns) is not None else ""
            videos.append({
                'video_id': entry.find('yt:videoId', ns).text,
                'title': entry.find('ns:title', ns).text,
                'published': published.strftime('%Y-%m-%d %H:%M:%S'),
                'link': link,
                'description': description
            })
    return videos

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_latest_videos.py <path_to_creators.json>", file=sys.stderr)
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        creators = json.load(f)
        
    group_a = creators.get("GROUP_A", {})
    group_b = creators.get("GROUP_B", {})
    
    report = {"group_a": {}, "group_b": {}}
    for handle, cid in group_a.items():
        xml = fetch_rss(cid)
        if xml:
            v = parse_rss(xml)
            if v: report["group_a"][handle] = v
    for handle, cid in group_b.items():
        xml = fetch_rss(cid)
        if xml:
            v = parse_rss(xml)
            if v: report["group_b"][handle] = v
    print(json.dumps(report))

if __name__ == "__main__":
    main()
