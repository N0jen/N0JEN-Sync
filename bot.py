import os
import time
import requests
import subprocess
import base64

TOKEN = os.environ.get("REPLICATE_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def guvenli_dogrudan_baglanti(model_yolu, girdi):
    """Zaman aşımı ve kütüphane çökmelerini engelleyen doğrudan API bağlantısı."""
    print(f"-> {model_yolu} tetikleniyor...")
    url = f"https://api.replicate.com/v1/models/{model_yolu}/predictions"
    
    # İşlem emrini gönderiyoruz
    baslat = requests.post(url, headers=HEADERS, json={"input": girdi}, timeout=30)
    baslat.raise_for_status()
    kontrol_linki = baslat.json()["urls"]["get"]
    
    # İşlemin bitmesini çökmeden, sabırla bekliyoruz
    while True:
        time.sleep(10) # Sunucuyu yormamak için 10 saniyede bir soruyoruz
        durum_cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = durum_cevap["status"]
        
        if durum == "succeeded":
            print("-> Yapay zeka işlemini başarıyla tamamladı!")
            return durum_cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Model hata verdi: {durum_cevap.get('error')}")
        else:
            print(f"-> Model çalışıyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

# Flux modeli ile görsel üretimi
image_output = guvenli_dogrudan_baglanti(
    "black-forest-labs/flux-schnell",
    {
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

image_url = image_output[0] if isinstance(image_output, list) else image_output
print("Görsel başarıyla çizildi, indiriliyor...")
with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli Başlıyor)...")

# Resmi Kling'in hata vermeden okuyabilmesi için Base64 formatına (metne) çeviriyoruz
with open("source_image.jpg", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read()).decode('utf-8')
data_uri = f"data:image/jpeg;base64,{b64_string}"

# Kling'e resmi metin dosyası olarak yolluyoruz, artık 422 hatası veremez
video_output = guvenli_dogrudan_baglanti(
    "kwaivgi/kling-v1.6-standard",
    {
        "image": data_uri,
        "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
        "duration": 5,
        "mode": "standard"
    }
)

video_url = str(video_output)
print("Hareketli video hazırlandı, bilgisayara indiriliyor...")
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
