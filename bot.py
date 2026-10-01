import urllib.request
import subprocess
import random
import time

print("Huzurlu, sıcak bir oda görseli hazırlanıyor...")

rastgele_sayi = random.randint(1, 10000)
prompt = f"Cozy_warm_living_room_cute_dog_sleeping_peacefully_on_a_sofa_large_window_showing_heavy_rain_outside_warm_lamp_light_cinematic_vertical_{rastgele_sayi}"
url_ai = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"
url_yedek = "https://picsum.photos/1080/1920"

req = urllib.request.Request(url_ai, headers={'User-Agent': 'Mozilla/5.0'})

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

print("Video renderlanıyor (Sinematik Zoom ve Tok Yağmur Sesi ekleniyor)...")

# Mor ekrana sebep olan 'noise/blend' filtreleri çöpe atıldı.
# Yerine resme hayat veren yavaş bir "Kamera Yakınlaştırma (zoompan)" efekti koyduk.
ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
    "-f", "lavfi", "-i", "anoisesrc=a=0.3:c=brown,lowpass=f=800",
    "-t", "60",
    "-vf", "crop=iw:ih*0.95:0:0,scale=1080:1920,zoompan=z='min(zoom+0.0005,1.1)':d=1800:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu, check=True)
print("İşlem Tamam! yeni_short_video.mp4 hazır.")
