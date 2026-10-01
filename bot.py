import urllib.request
import os
import subprocess
import random

print("Yatak odası ve pencere manzarası hazırlanıyor...")

rastgele_sayi = random.randint(1, 1000)
prompt = f"Cozy_cyberpunk_bedroom_interior_view_looking_out_of_a_large_window_at_heavy_rain_and_neon_city_lights_steaming_cup_of_coffee_on_the_table_warm_indoor_lighting_cinematic_8k_masterpiece_vertical_{rastgele_sayi}"
url_ai = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

url_yedek = "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?q=80&w=1080&h=1920&fit=crop" 

req = urllib.request.Request(
    url_ai, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    print("Yapay zekadan oda görseli talep ediliyor...")
    with urllib.request.urlopen(req, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Görsel yapay zekadan başarıyla indirildi!")
except Exception as e:
    print(f"Yapay zeka yanıt vermedi ({e}). B planı devreye giriyor...")
    req_yedek = urllib.request.Request(url_yedek, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_yedek, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())

print("Video renderlanıyor (Cızırtı giderildi, görsel düzeltildi)...")

# Mor ekran hatasını önlemek için filtreyi temizledik. Sadece logoyu kesip ekrana tam oturtuyoruz.
# Ses için: Pembe gürültü (pink noise) kullanıp 'lowpass=f=800' filtresiyle ince radyo cızırtılarını kesiyoruz, geriye tok bir yağmur/rüzgar sesi kalıyor.
ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=c=pink:a=0.1,lowpass=f=800,highpass=f=200", 
    "-t", "60",
    "-vf", "crop=iw:ih*0.95:0:0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! Temiz yeni_short_video.mp4 hazır.")
