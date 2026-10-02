import os
import requests
import subprocess
import httpx
import replicate

# Zaman aşımını (timeout) tamamen kaldırıyoruz. Yapay zeka uyanana kadar sabırla bekleyecek.
sinirsiz_istemci = httpx.Client(timeout=None)
api = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"), client=sinirsiz_istemci)

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor (Yapay zekanın uyanması 1-2 dakika sürebilir)...")

# 'replicate.run' yerine oluşturduğumuz sabırlı 'api.run' kalkanını kullanıyoruz
image_output = api.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

image_url = str(image_output[0])
print(f"Görsel üretildi, indiriliyor...")
with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli Başlıyor)...")

video_output = api.run(
    "kwaivgi/kling-v1.6-standard/image-to-video",
    input={
        "image": open("source_image.jpg", "rb"),
        "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
        "duration": 5,
        "mode": "standard"
    }
)

video_url = str(video_output)
print(f"Hareketli video hazırlandı, indiriliyor...")
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
print("İşlem Başarılı! final_shorts.mp4 oluşturuldu.")
