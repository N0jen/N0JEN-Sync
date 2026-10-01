import urllib.request
import os
import subprocess
import random

print("Huzurlu, sıcak bir oda görseli hazırlanıyor...")

# 1. GÖRSEL: Huzurlu Oda (Her seferinde farklı)
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

print("Gerçek yağmur sesi aranıyor...")
# 2. GERÇEK SES: Daha sağlam sunucular ve çökme önleyici (Try-Except) döngüsü
yagmur_sesleri = [
    "https://soundbible.com/mp3/Rain_Background-Mike_Koenig-1681385776.mp3",
    "https://soundbible.com/mp3/Heavy%20Rain-SoundBible.com-1191060410.mp3",
    "https://soundbible.com/mp3/Rain-SoundBible.com-1416973347.mp3"
]

random.shuffle(yagmur_sesleri)
ses_basarili = False

for ses_url in yagmur_sesleri:
    try:
        req_ses = urllib.request.Request(ses_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_ses, timeout=15) as response, open("gercek_yagmur.mp3", 'wb') as out_file:
            out_file.write(response.read())
        print("Gerçek ses başarıyla indirildi!")
        ses_basarili = True
        break  # Başarılı olursa diğer linkleri denemeyi bırak
    except Exception as e:
        print(f"Sunucu meşgul, diğer ses linkine geçiliyor...")

# 3. DİNAMİK YAĞMUR EFEKTİ: Rastgele damla algoritması
yagmur_seed = random.randint(1, 1000)
print("Video renderlanıyor...")

# Mor ekranı çözen ve şeffaf yağmur damlaları yaratan filtre
filter_complex = (
    f"[0:v]crop=iw:ih*0.95:0:0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[bg];"
    f"color=c=black:s=1080x1920:d=60:rate=30[black];"
    f"[black]noise=alls=80:allf=t+u:seed={yagmur_seed},eq=gamma=7,boxblur=1:20,format=yuv420p[rain];"
    f"[bg][rain]blend=all_mode='screen':all_opacity=0.65,format=yuv420p[outv]"
)

# Ses indirilebildiyse gerçek sesi kullan, indirilemediyse acil durum tok uğultusunu kullan
if ses_basarili:
    ffmpeg_komutu = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
        "-stream_loop", "-1", "-i", "gercek_yagmur.mp3",
        "-t", "60",
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "128k",
        "yeni_short_video.mp4"
    ]
else:
    # lowpass=f=400 radyo cızırtısını tamamen filtreler, sadece yağmur/rüzgar uğultusu kalır
    ffmpeg_komutu = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", "30", "-i", "arkaplan.jpg",
        "-f", "lavfi", "-i", "anoisesrc=c=pink:a=0.1,lowpass=f=400,highpass=f=100",
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
