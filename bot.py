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
    print(f"-> {model_yolu} için güvenli bağlantı kuruluyor...")
    
    # 1. Akıllı Versiyon Çözücü: Modelin en güncel ve izinli versiyon şifresini (hash) bulur
    bilgi_cevap = requests.get(f"https://api.replicate.com/v1/models/{model_yolu}", headers=HEADERS, timeout=30)
    
    if bilgi_cevap.status_code == 200 and bilgi_cevap.json().get("latest_version"):
        # Versiyon bulundu, en sağlam kapıdan (predictions API) giriş yapıyoruz
        v_id = bilgi_cevap.json()["latest_version"]["id"]
        baslat_url = "https://api.replicate.com/v1/predictions"
        payload = {"version": v_id, "input": girdi}
    else:
        # Donanım modelleri (ör. Flux) için standart giriş
        baslat_url = f"https://api.replicate.com/v1/models/{model_yolu}/predictions"
        payload = {"input": girdi}
        
    # 2. Emri gönderiyoruz
    baslat = requests.post(baslat_url, headers=HEADERS, json=payload, timeout=30)
    
    if baslat.status_code != 201:
        raise Exception(f"Model İşlemi Reddetti! Hata Detayı: {baslat.text}")
        
    kontrol_linki = baslat.json()["urls"]["get"]
    
    # 3. Sonucu sabırla bekliyoruz
    while True:
        time.sleep(10)
        durum_cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = durum_cevap["status"]
        
        if durum == "succeeded":
            print(f"-> {model_yolu} işlemini başarıyla tamamladı!")
            return durum_cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Model kendi içinde çöktü: {durum_cevap.get('error')}")
        else:
            print(f"-> Model çalışıyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

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

print("2. Aşama: Görsel Canlandırılıyor (Luma Ray Sinematik Motoru Başlatılıyor)...")

# Kling yerine, erişimi tamamen açık ve mükemmel sonuç veren Luma Dream Machine (Ray) motoruna geçtik
video_output = guvenli_dogrudan_baglanti(
    "luma/ray",
    {
        "image": image_url,
        "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance"
    }
)

# Yapay zekanın çıktısını güvenli bir şekilde metin (link) haline getiriyoruz
video_url = video_output[0] if isinstance(video_output, list) else str(video_output)
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
