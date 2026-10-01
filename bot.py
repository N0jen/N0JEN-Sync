import urllib.request
import os
import subprocess
import random

# 1. Aşama: Şifresiz/Bedava Yapay Zeka ile Görsel Üretimi (Pollinations.ai)
# Her seferinde farklı bir görsel çıkması için prompt sonuna rastgele bir sayı ekliyoruz
rastgele_sayi = random.randint(1, 1000)
prompt = f"cyberpunk_city_in_heavy_rain_neon_lights_vertical_{rastgele_sayi}"
url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

print("Yapay zekadan görsel indiriliyor...")
urllib.request.urlretrieve(url, "arkaplan.jpg")
print("Görsel başarıyla indirildi!")

# 2. Aşama: FFmpeg ile Görseli ve Yapay Yağmur Sesini (White Noise) Birleştirme
# 60 saniyelik (Shorts) dikey video oluşturuyoruz.
# anoisesrc=color=brown -> Yağmur ve rüzgar hissiyatı veren beyaz/kahverengi gürültü frekansı
print("Video renderlanıyor (60 Saniye Shorts)...")

ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", "arkaplan.jpg",                   # Görseli döngüye al
    "-f", "lavfi", "-i", "anoisesrc=a=0.1:c=brown",       # Yağmur/Rüzgar benzeri ses üret
    "-t", "60",                                           # 60 saniye süre sınırı (Shorts)
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", # Dikey formata (9:16) zorla
    "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", # YouTube uyumlu video formatı
    "-c:a", "aac", "-b:a", "128k",                        # Ses formatı
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! yeni_short_video.mp4 hazır.")
