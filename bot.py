import urllib.request
import os
import subprocess
import random

rastgele_sayi = random.randint(1, 1000)
prompt = f"cyberpunk_city_in_heavy_rain_neon_lights_vertical_{rastgele_sayi}"
url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

print("Yapay zekadan görsel indiriliyor...")

# Yapay zeka sunucusundan engellenmemek için kendimizi normal bir Chrome tarayıcısı gibi gösteriyoruz
req = urllib.request.Request(
    url, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
)

try:
    with urllib.request.urlopen(req) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Görsel başarıyla indirildi!")
except Exception as e:
    print(f"Hata: Yapay zeka sunucusu şu an yanıt vermiyor -> {e}")
    exit(1)

print("Video renderlanıyor (60 Saniye Shorts)...")

ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.1:c=brown",
    "-t", "60",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! yeni_short_video.mp4 hazır.")
