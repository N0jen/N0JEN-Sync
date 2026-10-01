import urllib.request
import subprocess
import random
import time

print("Huzurlu, sıcak bir oda görseli hazırlanıyor...")

# 1. GÖRSEL: Huzurlu Oda ve Uyuyan Köpek
rastgele_sayi = random.randint(1, 10000)
prompt = f"Cozy_warm_living_room_cute_dog_sleeping_peacefully_on_a_sofa_large_window_showing_heavy_rain_outside_warm_lamp_light_cinematic_vertical_{rastgele_sayi}"
url_ai = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

# Asla 404 vermeyecek, her zaman çalışan yedek görsel sunucusu
url_yedek = "https://picsum.photos/1080/1920"

req = urllib.request.Request(url_ai, headers={'User-Agent': 'Mozilla/5.0'})

# Yapay zeka yoğun olduğunda çökmesin diye 60 saniye süre ve 3 kez deneme hakkı verdik
basarili = False
for deneme in range(3):
    try:
        print(f"Yapay zeka deneniyor (Deneme {deneme+1}/3)...")
        with urllib.request.urlopen(req, timeout=60) as response, open("arkaplan.jpg", 'wb') as out_file:
            out_file.write(response.read())
        print("Görsel yapay zekadan başarıyla indirildi!")
        basarili = True
        break
    except Exception as e:
        print(f"Yapay zeka meşgul ({e}). Tekrar deneniyor...")
        time.sleep(2)

if not basarili:
    print("Yapay zeka yanıt vermedi, yedek görsele geçiliyor...")
    req_yedek = urllib.request.Request(url_yedek, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_yedek, timeout=60) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Yedek görsel indirildi.")

yagmur_seed = random.randint(1, 1000)
print("Video renderlanıyor (Damlalar ve Tok Yağmur Sesi ekleniyor)...")

filter_complex = (
    f"[0:v]crop=iw:ih*0.95:0:0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[bg];"
    f"color=c=black:s=1080x1920:d=60:rate=30[black];"
    f"[black]noise=alls=80:allf=t+u,eq=gamma=7,boxblur=1:20,format=yuv420p[rain];"
    f"[bg][rain]blend=all_mode='screen',format=yuv420p[outv]"
)

# Ses: Kahverengi gürültü (brown) üretip ince frekansları (lowpass) keserek kalın uğultu elde ediyoruz
ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.3:c=brown,lowpass=f=800",
    "-t", "60",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", "1:a",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu, check=True)
print("İşlem Tamam! yeni_short_video.mp4 hazır.")
