import urllib.request
import os
import subprocess
import random

print("Huzurlu, sıcak bir oda görseli hazırlanıyor...")

# 1. GÖRSEL: Huzurlu Oda (Her seferinde tamamen farklı bir oda ve köpek çizecek)
rastgele_sayi = random.randint(1, 10000)
prompt = f"Cozy_warm_living_room_cute_dog_sleeping_peacefully_on_a_sofa_large_window_showing_heavy_rain_outside_warm_lamp_light_cinematic_vertical_{rastgele_sayi}"
url_ai = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&nologo=true"

url_yedek = "https://images.unsplash.com/photo-1540324758509-34dc3895e347?q=80&w=1080&h=1920&fit=crop"

req = urllib.request.Request(url_ai, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())
    print("Görsel başarıyla indirildi!")
except Exception as e:
    req_yedek = urllib.request.Request(url_yedek, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_yedek, timeout=15) as response, open("arkaplan.jpg", 'wb') as out_file:
        out_file.write(response.read())

# 2. GERÇEK SES: Wikimedia'dan gerçek, organik yağmur sesleri (Cızırtı yok!)
print("Gerçek yağmur sesi aranıyor...")
yagmur_sesleri = [
    "https://upload.wikimedia.org/wikipedia/commons/4/42/Rain_-_Sounds_of_Nature.ogg",
    "https://upload.wikimedia.org/wikipedia/commons/5/52/Rain_Sound.ogg",
    "https://upload.wikimedia.org/wikipedia/commons/b/b5/Rain_on_leaves_and_pavement.ogg"
]
secilen_ses = random.choice(yagmur_sesleri)

req_ses = urllib.request.Request(secilen_ses, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_ses) as response, open("gercek_yagmur.ogg", 'wb') as out_file:
    out_file.write(response.read())
print("Gerçek ses başarıyla indirildi!")

# 3. DİNAMİK YAĞMUR EFEKTİ: Yağmur damlalarının her seferinde farklı düşmesi için rastgele sayı
yagmur_seed = random.randint(1, 1000)

print("Video renderlanıyor (Gerçek ses ve her seferinde farklı damlalar)...")

# Mor ekranı çözen ve yağmuru gerçekçi kılan filtre
filter_complex = (
    f"[0:v]crop=iw:ih*0.95:0:0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[bg];"
    f"color=c=black:s=1080x1920:d=60:rate=30[black];"
    f"[black]noise=alls=80:allf=t+u:seed={yagmur_seed},eq=gamma=7,boxblur=1:20,format=yuv420p[rain];"
    f"[bg][rain]blend=all_mode='screen':all_opacity=0.65,format=yuv420p[outv]"
)

ffmpeg_komutu = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
    "-stream_loop", "-1", "-i", "gercek_yagmur.ogg",  # İndirilen gerçek sesi kullanır ve 60 saniyeye yayar
    "-t", "60",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", "1:a",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-c:a", "aac", "-b:a", "128k",
    "yeni_short_video.mp4"
]

subprocess.run(ffmpeg_komutu)
print("İşlem Tamam! Her seferinde tamamen farklı olan kusursuz videon hazır.")
