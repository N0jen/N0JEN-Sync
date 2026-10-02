import os
import time
import requests
import subprocess

TOKEN = os.environ.get("REPLICATE_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def guvenli_yapay_zeka(model_yolu, girdi):
    print(f"-> {model_yolu} başlatılıyor...")
    url = f"https://api.replicate.com/v1/models/{model_yolu}/predictions"
    
    # İşlemi başlatıyoruz (Burada bekleme olmaz, sadece emri veririz)
    baslat = requests.post(url, headers=HEADERS, json={"input": girdi}, timeout=30)
    baslat.raise_for_status()
    kontrol_linki = baslat.json()["urls"]["get"]
    
    # İşlemin bitmesini sabırla ve kopmadan bekleyen döngümüz
    while True:
        time.sleep(5)  # Sistemi boğmamak için 5 saniyede bir soruyoruz
        durum_cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = durum_cevap["status"]
        
        if durum == "succeeded":
            print("-> Yapay zeka işlemini başarıyla bitirdi!")
            return durum_cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Model hata verdi: {durum_cevap.get('error')}")
        else:
            print(f"-> Model çalışıyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

# 1. Flux modeli ile görsel üretimi
image_output = guvenli_yapay_zeka(
    "black-forest-labs/flux-schnell",
    {
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

# Çıkan resmin sadece bulut linkini alıyoruz (indirmeden)
image_url = image_output[0] if isinstance(image_output, list) else image_output
print(f"Görsel Linki Alındı: {image_url}")

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli Başlıyor)...")

# 2. Resmi indirmeden doğrudan Kling modeline yolluyoruz (Çok daha hızlı ve güvenli)
video_output = guvenli_yapay_zeka(
    "kwaivgi/kling-v1.6-standard",
    {
        "image": image_url,
        "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
        "duration": 5,
        "mode": "standard"
    }
)

video_url = str(video_output)
print("Hareketli video bulutta hazırlandı, bilgisayara indiriliyor...")

# Sadece nihai videoyu bilgisayara indiriyoruz
with open("raw_loop.mp4", "wb") as f:
    f.write(requests.get(video_url).content)

print("3. Aşama: 60 Saniyeye Uzatma ve Tok Yağmur Sesi Ekleme...")

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-stream_loop", "-1", "-i", "raw_loop.mp4",
    "-f", "lavfi", "-i", "anoisesrc=a=0.3:c=brown,lowpass=f=700",
    "-t", "60",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "final_shorts.mp4"
]

subprocess.run(ffmpeg_cmd, check=True)
print("İşlem Başarılı! final_shorts.mp4 kusursuz şekilde oluşturuldu.")
