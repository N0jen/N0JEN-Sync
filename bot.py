import os
import time
import requests
import subprocess

TOKEN = os.environ.get("REPLICATE_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def guvenli_dogrudan_baglanti(model_yolu, girdi):
    print(f"-> {model_yolu} modeline bağlanılıyor...")
    
    # Tüm kilitleri aşan evrensel API giriş kapısı
    baslat_url = f"https://api.replicate.com/v1/models/{model_yolu}/predictions"
    baslat = requests.post(baslat_url, headers=HEADERS, json={"input": girdi}, timeout=30)
    
    if baslat.status_code != 201:
        raise Exception(f"Model Kapalı veya İzin İstiyor! Hata Detayı: {baslat.text}")
        
    kontrol_linki = baslat.json()["urls"]["get"]
    
    while True:
        time.sleep(10)
        durum_cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = durum_cevap["status"]
        
        if durum == "succeeded":
            print(f"-> İşlem başarıyla bitti!")
            return durum_cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Model kendi içinde çöktü: {durum_cevap.get('error')}")
        else:
            print(f"-> Model çalışıyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

# Flux modeli ile sorunsuz görsel üretimi
image_output = guvenli_dogrudan_baglanti(
    "black-forest-labs/flux-schnell",
    {
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

image_url = image_output[0] if isinstance(image_output, list) else image_output
print(f"-> Görsel başarıyla çizildi. Link: {image_url}")

print("2. Aşama: Görsel Canlandırılıyor (Stable Video Diffusion Motoru Başlatılıyor)...")

# Tamamen AÇIK KAYNAKLI, sözleşme veya onay istemeyen rock-solid (kaya gibi sağlam) motor!
# Yağmur, su ve rüzgar gibi doğal hareketleri mükemmel şekilde canlandırır.
video_output = guvenli_dogrudan_baglanti(
    "stability-ai/stable-video-diffusion",
    {
        "image": image_url,
        "sizing_strategy": "maintain_aspect_ratio",
        "frames_per_second": 16,
        "motion_bucket_id": 127
    }
)

# Çıktı formatını güvenceye alıyoruz
video_url = video_output if isinstance(video_output, str) else video_output[0]
print("-> Hareketli video hazırlandı, bilgisayara indiriliyor...")

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
