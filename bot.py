import os
import time
import requests
import subprocess
import replicate

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

# Flux modelini "Asenkron" (Beklemeli) modda başlatıyoruz
gorsel_islem = replicate.predictions.create(
    model="black-forest-labs/flux-schnell",
    input={
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

# Zaman aşımını (Timeout) çöpe attık. İşlem bitene kadar bıkmadan durumunu soruyoruz.
while gorsel_islem.status not in ["succeeded", "failed", "canceled"]:
    print(f"-> Görsel Çiziliyor (Durum: {gorsel_islem.status})...")
    time.sleep(3)
    gorsel_islem.reload()

if gorsel_islem.status != "succeeded":
    raise Exception(f"Görsel üretilemedi: {gorsel_islem.error}")

image_url = str(gorsel_islem.output[0])
print("-> Görsel başarıyla üretildi, bilgisayara indiriliyor...")

# Görseli mutlaka bilgisayara indiriyoruz (422 hatasını önlemek için)
with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli Başlıyor)...")

# Resmi Replicate'in anlayacağı şekilde (dosya olarak) yüklüyoruz
with open("source_image.jpg", "rb") as image_file:
    video_islem = replicate.predictions.create(
        model="kwaivgi/kling-v1.6-standard",
        input={
            "image": image_file,
            "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
            "duration": 5
        }
    )

# Video üretimi ağır olduğu için 10 saniyede bir sorarak sunucunun çökmesini engelliyoruz
while video_islem.status not in ["succeeded", "failed", "canceled"]:
    print(f"-> Video İşleniyor (Durum: {video_islem.status})...")
    time.sleep(10)
    video_islem.reload()

if video_islem.status != "succeeded":
    raise Exception(f"Video üretilemedi: {video_islem.error}")

video_url = str(video_islem.output)
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
