
import os
import time
import requests
import subprocess

TOKEN = os.environ.get("REPLICATE_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def bekle_ve_al(kontrol_linki):
    while True:
        time.sleep(5)
        cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = cevap["status"]
        if durum == "succeeded":
            print("-> İşlem başarıyla bitti!")
            return cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Hata: {cevap.get('error')}")
        else:
            print(f"-> Çiziliyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Kusursuz 8K Anime Odası Çiziliyor...")

# Sadece Flux kullanıyoruz. Görüntüyü bozacak hiçbir video motoru araya giremez.
baslat_flux = requests.post(
    "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
    headers=HEADERS,
    json={
        "input": {
            "prompt": "Masterpiece, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, 8k resolution, highly detailed, perfect proportions, studio ghibli anime style",
            "aspect_ratio": "9:16",
            "output_format": "jpg"
        }
    },
    timeout=30
)

if baslat_flux.status_code != 201:
    raise Exception(f"Flux Reddedildi: {baslat_flux.text}")

image_output = bekle_ve_al(baslat_flux.json()["urls"]["get"])
image_url = image_output[0] if isinstance(image_output, list) else image_output
print("-> Görsel çizildi, bilgisayara indiriliyor...")

with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Profesyonel Montaj ve Ses Tasarımı (FFmpeg)...")
print("-> Görüntünün bozulmasına/erimesine izin verilmeden doğrudan Lofi kurgusu yapılıyor...")

# Resmi alır, orantısını JİLET gibi koruyarak ekrana oturtur. 
# Üzerine o harika tok yağmur sesini ekler ve 60 saniyelik kusursuz bir video çıkarır.
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "source_image.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.3:c=brown,lowpass=f=700",
    "-t", "60",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "final_shorts.mp4"
]

subprocess.run(ffmpeg_cmd, check=True)
print("İşlem Başarılı! %100 profesyonel görünümlü final_shorts.mp4 oluşturuldu.")
