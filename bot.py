import urllib.request
import os
import subprocess
import random

print("Görsel hazırlanıyor...")

# A Planı: Yapay Zeka (Pollinations)
rastgele_sayi = random.randint(1, 1000)
prompt = f"cyberpunk_city_in_heavy_rain_neon_lights_vertical_{rastgele_sayi}"
url_ai = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

# B Planı: Asla silinmeyecek ve engellenmeyecek %100 çalışan sabit bir Neon Şehir görseli (Wikimedia)
url_yedek = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Tokyo_Shinjuku_Kabukicho_Neon_Night.jpg/1080px-Tokyo_Shinjuku_Kabukicho_Neon_Night.jpg"

req = urllib.request.Request(
    url_ai, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    # 1. Adım: Yapay Zekayı Dene
    print("Yapay zekadan görsel talep ediliyor...")
    with urllib.request.urlopen(req, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Görsel yapay zekadan başarıyla indirildi!")
    
except Exception as e:
    # 2. Adım: Hata verirse çökmek yerine yedek görseli kullan
    print(f"Yapay zeka sunucusu yanıt vermedi ({e}). B planı devreye giriyor...")
    req_yedek = urllib.request.Request(url_yedek, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_yedek, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Yedek cyberpunk görseli başarıyla indirildi!")

# 3. Adım: FFmpeg ile Video Render
print("Video renderlanıyor (60 Saniye Shorts)...")

ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.1:c=brown",
    "-t", "60",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! yeni_short_video.mp4 hazır.")
