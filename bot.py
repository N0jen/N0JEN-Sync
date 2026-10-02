import os
import requests
import subprocess
import replicate

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

# Kaliteli Anime/Lofi görseli için Flux modeli çalıştırılıyor
image_output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

image_url = str(image_output[0])
with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli)...")

# Görseli videoya dönüştürme (Kling Image-to-Video)
video_output = replicate.run(
    "kwaivgi/kling-v1.6-standard/image-to-video",
    input={
        "image": open("source_image.jpg", "rb"),
        "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
        "duration": 5,
        "mode": "standard"
    }
)

video_url = str(video_output)
with open("raw_loop.mp4", "wb") as f:
    f.write(requests.get(video_url).content)

print("3. Aşama: 60 Saniyeye Uzatma ve Tok Yağmur Sesi Ekleme...")

# 5 saniyelik döngüyü 60 saniyeye tamamlar ve tok yağmur sesi üretir
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
