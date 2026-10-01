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

print("Video renderlanıyor (Gerçekçi Yağmur Damlaları ekleniyor)...")

# Yeni Akıllı Filtre: Resmin boyutu ne olursa olsun altından %5'lik logoyu (ih*0.95) keser, 
# ardından güvenli bir şekilde 1080x1920 Shorts boyutuna sündürmeden oturtur.
filter_complex = (
    "[0:v]crop=iw:ih*0.95:0:0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[img];"
    "color=c=black:s=1080x1920:d=60:rate=30[black];"
    "[black]noise=alls=80:allf=t+u,eq=gamma=5,boxblur=1:20[rain];"
    "[img][rain]blend=all_mode='screen'[outv]"
)

ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.1:c=brown",
    "-t", "60",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", "1:a",
    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! Yağmur efektli yeni_short_video.mp4 hazır.")
