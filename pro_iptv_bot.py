import cloudscraper
import re
import urllib3
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"
}

# Normal requests yerine Cloudflare atlatıcı scraper kullanıyoruz
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})

def get_base_url():
    try:
        res = scraper.get("https://raw.githubusercontent.com/patr0nq/veriler/refs/heads/main/siteurl.txt", timeout=5, verify=False)
        for line in res.text.split('\n'):
            line = line.strip()
            if line.startswith("diziyou:"):
                return line.replace("diziyou:", "").strip().rstrip('/')
    except:
        pass
    return "https://www.diziyou.one"

def get_metadata(soup, html):
    title = soup.find("meta", property="og:title")
    title = title["content"] if title else "Bilinmeyen İçerik"
    
    poster = soup.find("meta", property="og:image")
    poster = poster["content"] if poster else ""
    
    desc = soup.find("meta", property="og:description")
    desc = desc["content"] if desc else "Açıklama bulunmuyor."
    
    imdb_match = re.search(r'IMDb[\s:]*([0-9.]+)', html, re.IGNORECASE)
    imdb = imdb_match.group(1) if imdb_match else "N/A"
    
    if "Sezon" in title and "Bölüm" in title:
        group = "Güncel Diziler"
    else:
        group = "Güncel Filmler"
        
    return title, poster, desc, imdb, group

def process_page_links(base_url, page_num):
    print(f"\n[+] Sayfa {page_num} taranıyor...")
    page_url = f"{base_url}/page/{page_num}/" if page_num > 1 else base_url
    
    try:
        res = scraper.get(page_url, headers=HEADERS, verify=False, timeout=15)
        
        if res.status_code != 200:
            print(f"[-] HATA: Sayfa erişimi reddedildi. Status Kodu: {res.status_code}")
            return []
            
        soup = BeautifulSoup(res.text, "html.parser")
        all_links = soup.find_all('a', href=True)
        
        content_links = set()
        for a in all_links:
            href = a.get('href', '')
            full_url = urljoin(base_url, href)
            
            if base_url in full_url and not any(x in full_url for x in ['/kategori/', '/tag/', '/author/', '/page/', 'wp-admin']):
                if full_url.count('/') > 3 and full_url != base_url + "/":
                    content_links.add(full_url)
                    
        return list(content_links)
    except Exception as e:
        print(f"[-] Sayfa {page_num} alınamadı: {e}")
        return []

def extract_video_sources(url, base_url):
    try:
        res = scraper.get(url, headers=HEADERS, verify=False, timeout=10)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        
        iframe_match = re.search(r'<iframe[^>]+(?:id=["\']diziyouPlayer["\'][^>]+src=["\']([^"\']+)["\']|src=["\']([^"\']+)["\'][^>]+id=["\']diziyouPlayer["\'])', html, re.I)
        
        if not iframe_match:
            return None
            
        iframe_src = iframe_match.group(1) or iframe_match.group(2)
        item_id = iframe_src.split('/')[-1].split('.html')[0]
        
        storage_base = base_url.replace("www.", "storage.")
        if "://" not in storage_base:
            storage_base = "https://" + storage_base.split("//")[-1]

        title, poster, desc, imdb, group = get_metadata(soup, html)
        
        sources = []
        if 'id="turkceAltyazili"' in html or ('turkceDublaj' not in html):
            sources.append({
                "name": f"{title} (Altyazılı)",
                "link": f"{storage_base}/episodes/{item_id}/play.m3u8",
                "poster": poster,
                "desc": desc,
                "imdb": imdb,
                "group": group
            })
            
        if 'id="turkceDublaj"' in html:
            sources.append({
                "name": f"{title} (Dublaj)",
                "link": f"{storage_base}/episodes/{item_id}_tr/play.m3u8",
                "poster": poster,
                "desc": desc,
                "imdb": imdb,
                "group": group
            })
            
        return sources
    except:
        return None

def main():
    print("==================================================")
    print("   OTOMATİK GITHUB IPTV M3U OLUŞTURUCU (CLOUDSCRAPER)  ")
    print("==================================================")
    
    base_url = get_base_url()
    
    max_pages = 5
    m3u_content = ["#EXTM3U\n"]
    basarili_sayisi = 0
    
    for page in range(1, max_pages + 1):
        links = process_page_links(base_url, page)
        print(f"[*] Sayfa {page}'de {len(links)} içerik bulundu.")
        
        for link in links:
            time.sleep(0.5) 
            
            sources = extract_video_sources(link, base_url)
            if sources:
                for src in sources:
                    imdb_text = f" [IMDb: {src['imdb']}]" if src['imdb'] != "N/A" else ""
                    display_name = f"{src['name']}{imdb_text}"
                    clean_desc = src['desc'].replace('"', "'").replace('\n', ' ').replace('\r', '')
                    
                    extinf = f'#EXTINF:-1 tvg-logo="{src["poster"]}" group-title="{src["group"]}" description="{clean_desc}", {display_name}'
                    
                    m3u_content.append(extinf)
                    m3u_content.append(f"{src['link']}\n")
                    basarili_sayisi += 1
                print(f"[✔] Eklendi: {sources[0]['name']}")
                
    with open("vip_iptv.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_content))
        
    print(f"\n[+] İŞLEM BİTTİ! Toplam {basarili_sayisi} medya çekildi ve m3u güncellendi.")

if __name__ == "__main__":
    main()
