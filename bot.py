import os
import time
import requests
import subprocess
import replicate

def guvenli_yapay_zeka_calistir(model_adi, girdi_verisi, deneme_hakkasi=4):
    """Yapay zeka uyuyorsa veya yoğunsa çökmeden tekrar tekrar dener."""
    for deneme in range(deneme_hakkasi):
        try:
            return replicate.run(model_adi, input=girdi_verisi)
        except Exception as e:
            print(f"Yapay zeka uyanıyor/yoğun. Bekleniyor... (Deneme {deneme+1}/{deneme_hakkasi}) Hata: {e}")
            time.sleep(10)  # Çökmeden önce 10 saniye soluklanıp tekrar dener
    raise Exception("Yapay zeka sunucusu şu an çok yoğun, işlem tamamlanamadı.")

print("1. Aşama: Sinematik Anime Oda ve Yağmur Görseli Üretiliyor...")

image_output = guvenli_yapay_zeka_calistir(
    "black-forest-labs/flux-schnell",
    {
        "prompt": "Anime Studio Ghibli style, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed, massive window looking outside at heavy rain, street lights glowing in rain, cinematic lighting, masterpiece, 8k, vertical aspect ratio",
        "aspect_ratio": "9:16",
        "output_format": "jpg"
    }
)

image_url = str(image_output[0])
print("Görsel başarıyla üretildi, indiriliyor...")
with open("source_image.jpg", "wb") as f:
    f.write(requests.get(image_url).content)

print("2. Aşama: Görsel Canlandırılıyor (Hareketli Video Modeli Başlıyor)...")

# 'with open' kullanarak dosya kilitleme hatalarının önüne geçiyoruz
with open("source_image.jpg", "rb") as image_file:
    video_output = guvenli_yapay_zeka_calistir(
        "kwaivgi/kling-v1.6-standard/image-to-video",
        {
            "image": image_file,
            "prompt": "Raindrops falling down the window glass, gentle rain ripples, soft breathing of sleeping person, smooth looping motion, cozy ambiance",
            "duration": 5,
            "mode": "standard"
        }
    )

video_url = str(video_output)
print("Hareketli video hazırlandı, indiriliyor...")
with open("raw_loop.mp4", "wb") as f:
    f.write(requests.get(video_url).content)

print("3. Aşama: 60 Saniyeye Uzatma ve Tok Yağmur Sesi Ekleme...")

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
print("İşlem Başarılı! final_shorts.mp4 kusursuz şekilde oluşturuldu.")
