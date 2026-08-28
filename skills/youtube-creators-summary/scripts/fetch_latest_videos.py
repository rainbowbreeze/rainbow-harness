import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import json

GROUP_A = {
    "@aiwithbrandon": "UCEzrs7gK6Nf6t_tadEprzxQ",
    "@alessandro-mazza": "UCp-_-rNy3zputgA7FLeaz3g",
    "@andrea.Baccega": "UCAV3KgR3tR9kW1kK_XTAgqw",
    "@andreagaleazziVERIFICATO": "UC5yXB_ThsufRJYMRlzIGoeQ",
    "@AndreaSpiess": "UCY4yG6tPchXKLQ25lU1x37A",
    "@apalrdsadventures": "UCIgNWXsJcFwvFptmUic6wSw",
    "@BeardedTinker": "UCuqokNoK8ZFNQdXxvlE129g",
    "@buildingtheopenmetaverse": "UCCMEsdydTLm-e7gI10v_quA",
    "@d4n87": "UCOuj1cNT-HodW4M5Ve7HqUA",
    "@ETAPRIME": "UC_0CVCfC_3iuHqmyClu59Uw",
    "@fluidotv": "UC51PBqyVRwahWW1rqGKv_Uw",
    "@ILDOPPIATOREMARCHIGIANO": "UCGXRmvJqspFe3DPciaAlSEg",
    "@JeffGeerling": "UCsd6hP-zzIkCpw8XGw7Osyw",
    "@Koinsquare": "UCYFn0YEUnCbBtTkw5S4bhmQ",
    "@LAWRENCESYSTEMS": "UCN80uA4U7H-Bk5uK3NXtMcg",
    "@ledbycommunity": "UCfDfGTKtk2bDUxuUkRCiS4A",
    "@MakeItWorkTech": "UCGoreZKPBtCXCf54F3DF4ug",
    "@mr_rip": "UCBOtZaVafz_5OmUrqJAVStQ",
    "@PaoloColetti": "UCCnqSU06KXxGvPESASofSQA",
    "@smartereveryday": "UC8VkNBOwvsTlFjoSnNSMmxw",
    "@StoriediBrand": "UCal2PGS4ESoEGqRc8bOU6GQ",
    "@TechWithTim": "UCZirJBCIZsSgsSPn-uWVSfg",
    "@TheAIXRPodcast": "UCEh4co_L69LtL9vyUixLMZg",
    "@thecryptogateway": "UC9X2f4pVXSNzsJ2c6ZQVqBQ",
    "@TheHookUp": "UC2gyzKcHbYfqoXA5xbyGXtQ",
    "@Clearmud": "UClMgNsPzvVprkO297NfjDuw",
    "@151eg": "UCVK8kbbyUaudTCttzFYS7FQ",
    "@adhras": "UCtRrFIehQpQii6pu3YVNNig",
    "@theAIsearch": "UCIgnGlGkVRhd4qNFcEwLL4A",
    "@AngeloColomboFi": "UCV_VWoWQo_4NHAE4jZkpERg",
    "@BenFelixCSI": "UCOErWFfNOQzXsgE7f5S_ULw",
    "@CrossTalkSolutions": "UCHkYOD-3fZbuGhwsADBd9ZQ",
    "@EverythingSmartHome": "UCrVLgIniVg6jW38uVqDRIiQ",
    "@fixtse": "UCOY6oNxodGWbFg6CjXtae5g",
    "@home_assistant": "UCbX3YkedQunLt7EQAdVxh7w",
    "@KPeyanski": "UCiyU6otsAn6v2NbbtM85npg",
    "@MattVidPro": "UC06GdmaEdCdCFwR3NvszloQ",
    "@PietroMichelangeli": "UCjbTnxfi2IDF_yGmVkP_2dQ",
    "@SmartHomeJunkie": "UCZ2Ku6wrhdYDHCaBzLaA3bw",
    "@SmartHomeSolver": "UCnvqF2-dOB9qo9EPDHRX9mg",
    "@talksatgoogle": "UCbmNph6atAoGfqLoCL_duAg",
    "@TechnoTim": "UCOk-gHyjcWZNj3Br4oxwh0A",
    "@ThrillSeekerVR": "UCbmRYtcdumLwRJEReqQ16LA",
    "@TizianoTridico": "UCZ-xsxxIGsKwXaZhCFjQr1w",
    "@Veritasium": "UCin0m13qWv3-051xlWlHamA"
}

GROUP_B = {
    "@NetworkChuck": "UCOuGATIAbd2DvzJmUgXn2IQ",
    "@geopop": "UCQgQZdC52kP5V1XI3o5ux4g",
    "@CiaoElsa": "UCBVQ0MSOaWoZu0HimZ-46vw",
    "@matthew_berman": "UCawZsQWqfGSbCI5yjkdVkTA",
    "@mkbhd": "UCG7J20LhUeLl6y_Emi7OJrA",
    "@StartingFinance": "UCBahpZUV9wGy0ZdiVL2rqCA",
    "@thebull_finance": "UCNp1e5n6rlnfm5aWbHe3cJw"
}

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
    report = {"group_a": {}, "group_b": {}}
    for handle, cid in GROUP_A.items():
        xml = fetch_rss(cid)
        if xml:
            v = parse_rss(xml)
            if v: report["group_a"][handle] = v
    for handle, cid in GROUP_B.items():
        xml = fetch_rss(cid)
        if xml:
            v = parse_rss(xml)
            if v: report["group_b"][handle] = v
    print(json.dumps(report))

if __name__ == "__main__":
    main()
