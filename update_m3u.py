import requests
import json
import os

# Veriyi çekeceğimiz kaynak URL
JSON_URL = "https://raw.githubusercontent.com/dominoiptv/dominotv/main/liste.json"
OUTPUT_M3U = "liste.m3u"

def fetch_and_convert():
    print(f"{JSON_URL} adresinden veriler çekiliyor...")
    
    try:
        # İnternetten JSON dosyasını indir
        response = requests.get(JSON_URL, timeout=15)
        response.raise_for_status() # Eğer 404 veya 403 hatası varsa burada durdurur
        data = response.json()
        print("JSON verisi başarıyla indirildi!")
    except requests.exceptions.RequestException as e:
        print(f"Hata: URL'den veri çekilemedi! Linki veya deponun gizlilik (private) ayarlarını kontrol edin. Detay: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Hata: Çekilen veri geçerli bir JSON formatında değil! Detay: {e}")
        return

    # Veriyi listeye çevirme ve düzleştirme
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        item["category_from_dict"] = key
                        items.append(item)
            else:
                items.append(val)

    # M3U Dosyasını oluşturma
    count = 0
    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            # Etiket eşleştirmeleri
            name = item.get("name", item.get("title", item.get("kanal_adi", "İsimsiz Kanal")))
            url = item.get("url", item.get("link", item.get("stream", "")))
            logo = item.get("logo", item.get("tvg-logo", item.get("image", "")))
            category = item.get("category", item.get("group", item.get("kategori", item.get("category_from_dict", "Diğer"))))
            
            if not url:
                continue
                
            extinf_line = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n'
            f.write(extinf_line)
            f.write(f"{url}\n")
            count += 1
            
    print(f"Başarılı! Toplam {count} kanal {OUTPUT_M3U} dosyasına yazıldı.")

if __name__ == "__main__":
    fetch_and_convert()
