import json
import os

INPUT_JSON = "liste.json"
OUTPUT_M3U = "liste.m3u"

def convert_json_to_m3u():
    # 1. Dosya kontrolü
    if not os.path.exists(INPUT_JSON):
        print(f"Hata: '{INPUT_JSON}' dosyası aynı dizinde bulunamadı!")
        print("Lütfen deponuzdaki json dosyasının adının tam olarak 'liste.json' olduğundan emin olun.")
        return

    # 2. JSON dosyasını okuma (İnternetsiz, doğrudan diskten)
    print("liste.json dosyası okunuyor...")
    try:
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Hata: JSON dosyasının formatı bozuk! Lütfen JSON yapınızı kontrol edin. Detay: {e}")
        return
    except Exception as e:
        print(f"Hata: Dosya okunurken beklenmedik bir sorun oluştu! {e}")
        return

    # 3. Veriyi M3U formatına uygun ayıklama
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

    # 4. M3U dosyasını oluşturma
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
    convert_json_to_m3u()
