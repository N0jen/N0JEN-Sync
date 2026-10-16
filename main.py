from curl_cffi import requests
import json
import re

BASE_URL = "https://ydfvfdizipanel.ru"
API_TOKEN = "9iQNC5HQwPlaFuJDkhncJ5XTJ8feGXOJatAA"

HEADERS = {
    "hash256": "711bff4afeb47f07ab08a0b07e85d3835e739295e8a6361db77eebd93d96306b",
    "signature": "3082058830820370a00302010202145bbfbba9791db758ad12295636e094ab4b07dc24300d06092a864886f70d01010b05003074310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e205669657731143012060355040a130b476f6f676c6520496e632e3110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643020170d3231313231353232303433335a180f32303531313231353232303433335a3074310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e205669657731143012060355040a130b476f6f676c6520496e632e3110300e060355040b1307416e64726f69643110300e06035504031307416e64726f696430820222300d06092a864886f70d01010105000382020f003082020a0282020100a5106a24bb3f9c0aaf3a2b228f794b5eaf1757ba758b19736a39d1bdc73fc983a7237b8d5ca5156cfa999c1dab3418bbc2be0920e0ee001c8aa4812d1dae75d080f09e91e0abda83ff9a76e8384a4429f4849248069a59505b12ac2c14ba2e4d1a13afcdaf54e508697ff928a9f738e6f4a6fc27409c55329eb149b5ff89c5a2d7c06bf9e62086f955cad17d7be2623ee9d5ec56068eadc23cb0965a13ff97d49fe10ef41afc6eeca36b4ace9582097faff89f590bc831cdb3a69eec5d15b67c3f2cad49e37ed053733e3d2d400c47755b932bdbe15d749fd6ad1dce30ba5e66094dfb6ee6f64cafb807e11b19a990c5d078c6d6701cda0bdeb21e99404ff166074f4c89b04c418f4e7940db5c78647c475bcfb85d4c4e836ee7d7c1d53e9e736b5d96d4b4d8b98209064b729ac6a682d55a6a930e518d849898bb28329ca0aaa133b5e5270a9d5940cac6af4802a57fd971efda91abb602882dd6aa6ce2b236b57b52ee2481498f0cacbcc2c36c238bc84becad7eaaf1125b9a1ca9ded6c79f3f283a52050377809b2a9995d66e1636b0ed426fdd8685c47cb18e82077f4aefcc07887e1dc58b4d64be1632f0e7b4625da6f40c65a8512a6454a4b96963e7f876136e6c0069a519a79ad632078ed965aa12482458060c030ed50db706d854f88cb004630b49285d8af8b471ff8f6070687826412287b50049bcb7d1b6b62ef90203010001a310300e300c0603551d13040530030101ff300d06092a864886f70d01010b0500038202010051c0b7bd793181dc29ca777d3773f928a366c8469ecf2fa3cfb076e8831970d19bb2b96e44e8ccc647cf0696bb824ac61c23d958525d283cab26037b04d58aa79bf92192db843adf5c26a980f081d2f0e14f759fc5ff4c5bb3dce0860299bfe7b349a8155a2efaf731ba25ce796a80c1442c7bf80f8c1a7912ff0b6f6592264315337251a846460194fa594f81f38f9e5233a63201e931ad9cab5bf119f24025613f307194eaa6eb39a83f3c05a49ba34455b1aff7c6839bbb657d9392ffdf397432af6e56ba9534a8b07d7060fe09691c6cf07cb5324f67b3cc0871a8c621d81fe71d71085c55206a4f57e25f774fd4b979b299e8bb076b50fca42fa57da2d519fd35a4a7c0137babaed4345f8031b63b6a71f5e8268f709d658ccd7c2a58849379d25bfa598c3f4a2c3d9b7d89285fefeb7f0ec65137d38b08ce432a15688b624a179e6a4a505ebc3bcdfbc4d4330508ee2d8d0f016924dcec21a6838ef7d834c6f43bde4a5201ed0b3bb4e9bd377b470e36bcf5bc3d56169dbd8e39567aa7dce4d1a8a8a54a5e1aa6fb1a8aab0062669a966f96e15ccce6fe12ea5e6a8b8c8823bdc94988ca39759fd1cc8fd8ae5c3d74db50b174cf7d77655016c075c91d439ed01cc0a9f695c99fad3b5495fb6cb1e01a5fa020cc6022a85c07ec55f9eba89719f86e49d34ab5bd208c5f70cced2b7b7963c014f8404432979b506de29e",
    "User-Agent": "EasyPlex (Android 14; SM-A546B; Samsung Galaxy A54 5G; tr)",
    "Accept": "application/json"
}

# Impersonate ile Cloudflare'i gerçek bir tarayıcı olduğumuza ikna edip, 
# User-Agent'ı uygulamanın (EasyPlex) ki ile eziyoruz.
session = requests.Session(impersonate="chrome110")
session.headers.update(HEADERS)

def extract_mediafire(url):
    try:
        # Mediafire için standart başlık yetiyor
        res = session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        match = re.search(r'id="downloadButton"\s+href="([^"]+)"', res.text, re.IGNORECASE) or \
                re.search(r'href="([^"]+)"\s+id="downloadButton"', res.text, re.IGNORECASE)
        if match:
            return match.group(1)
    except:
        pass
    return url

def get_main_page_items():
    endpoints = [
        {"cat": "movies", "url": f"{BASE_URL}/public/api/movies/popular/{API_TOKEN}"},
        {"cat": "movies", "url": f"{BASE_URL}/public/api/movies/latest/{API_TOKEN}"},
        {"cat": "series", "url": f"{BASE_URL}/public/api/series/popular/{API_TOKEN}"},
        {"cat": "series", "url": f"{BASE_URL}/public/api/series/latest/{API_TOKEN}"}
    ]
    items = []
    for ep in endpoints:
        try:
            res = session.get(ep["url"], timeout=15)
            
            if res.status_code != 200:
                print(f"[{res.status_code}] API Erişilemiyor: {ep['url']}")
                continue
                
            data = res.json()
            results = data.get("movies", []) or data.get("series", [])
            for r in results:
                is_anime = "anime" in str(r.get("genres", "")).lower() or "anime" in str(r.get("name", "")).lower()
                cat = "anime" if is_anime else ep["cat"]
                
                items.append({
                    "id": r["id"],
                    "title": r.get("name", r.get("title", "")),
                    "type": "serie" if ep["cat"] == "series" else "movie",
                    "poster": r.get("poster_path", ""),
                    "category": cat
                })
        except json.JSONDecodeError:
            print(f"Sunucu JSON döndürmedi! API URL: {ep['url']}")
        except Exception as e:
            print(f"Hata ({ep['url']}): {e}")
            
    return items

def get_streams(item_id, item_type):
    url = f"{BASE_URL}/public/api/{'media' if item_type == 'movie' else 'series'}/{'detail' if item_type == 'movie' else 'show'}/{item_id}/{API_TOKEN}"
    streams = []
    try:
        res = session.get(url, timeout=15)
        if res.status_code != 200:
            return streams
            
        data = res.json()
        if item_type == "movie":
            videos = data.get("videos", [])
            for v in videos:
                link = v.get("link") or v.get("youtubelink") or v.get("embed")
                if link:
                    if "mediafire.com" in link:
                        link = extract_mediafire(link)
                    streams.append(link)
        else:
            seasons = data.get("seasons", [])
            for s in seasons:
                episodes = s.get("episodes", [])
                for e in episodes:
                    videos = e.get("videos", [])
                    for v in videos:
                        link = v.get("link") or v.get("youtubelink") or v.get("embed")
                        if link:
                            if "mediafire.com" in link:
                                link = extract_mediafire(link)
                            streams.append(link)
    except Exception as e:
        pass
        
    return list(set(streams))

def main():
    print("İçerikler Çekiliyor... (Bypass Aktif)")
    items = get_main_page_items()
    
    if not items:
        print("Uyarı: Hiç içerik bulunamadı. Lütfen API'nin aktif olduğundan emin olun.")
        return

    m3u_files = {
        "movies": "#EXTM3U\n",
        "series": "#EXTM3U\n",
        "anime": "#EXTM3U\n",
        "all": "#EXTM3U\n"
    }

    processed = set()
    
    for item in items:
        if item["id"] in processed:
            continue
        processed.add(item["id"])
        
        print(f"İşleniyor: {item['title']} ({item['category']})")
        streams = get_streams(item["id"], item["type"])
        
        for stream in streams:
            if not stream: continue
            
            if not re.search(r'\.(m3u8|mp4|mkv)', stream, re.I):
                stream += "#.mkv"
                
            entry = f'#EXTINF:-1 tvg-id="{item["id"]}" tvg-logo="{item["poster"]}" group-title="{item["category"].capitalize()}", {item["title"]}\n{stream}\n'
            
            m3u_files[item["category"]] += entry
            m3u_files["all"] += entry

    for name, content in m3u_files.items():
        with open(f"{name}.m3u", "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"Tüm dosyalar oluşturuldu. Toplam İşlenen: {len(processed)} içerik.")

if __name__ == "__main__":
    main()
