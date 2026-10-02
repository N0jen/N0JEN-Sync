import os
import time
import requests
import subprocess

TOKEN = os.environ.get("REPLICATE_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def bekle_ve_al(kontrol_linki):
    while True:
        time.sleep(10)
        cevap = requests.get(kontrol_linki, headers=HEADERS, timeout=30).json()
        durum = cevap["status"]
        if durum == "succeeded":
            print("-> İşlem başarıyla bitti!")
            return cevap["output"]
        elif durum in ["failed", "canceled"]:
            raise Exception(f"Hata: {cevap.get('error')}")
        else:
            print(f"-> İşleniyor (Durum: {durum})... Bekleniyor.")

print("1. Aşama: Geniş Açılı, Orantılı Oda Çiziliyor...")

# Odanın yamulmaması için komuta "wide angle" (geniş açı) ve "perfectly proportioned" (kusursuz orantı) eklendi.
baslat_flux = requests.post(
    "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
    headers=HEADERS,
    json={
        "input": {
            "prompt": "Wide angle shot, perfectly proportioned cozy bedroom interior, a person sleeping perfectly still under a warm blanket in bed, massive window looking outside at heavy rain, cinematic lighting, symmetric, 8k, highly detailed",
            "aspect_ratio": "9:16",
            "output_format": "jpg"
        }
    },
    timeout=30
)

if baslat_flux.status_code != 201:
    raise Exception(f"Flux Reddedildi: {baslat_flux.text}")

image_output = bekle_ve_al(baslat_flux.json()["urls"]["get"])
image_url = image_output[0] if isinstance(image_output, list) else image_output
print(f"-> Görsel çizildi. Link: {image_url}")

print("2. Aşama: Sabit Oda, Hareketli Yağmur (SVD Motoru)...")

# Hareket şiddeti (motion_bucket_id) 127'den 40'a düşürüldü! 
# Böylece yatak/duvar erimeyecek, sadece hafif ve doğal hareketler (yağmur) olacak.
baslat_svd = requests.post(
    "https://api.replicate.com/v1/predictions",
    headers=HEADERS,
    json={
        "version": "3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        "input": {
            "input_image": image_url,
            "sizing_strategy": "maintain_aspect_ratio",
            "motion_bucket_id": 40, 
            "cond_aug": 0.02,
            "frames_per_second": 6
        }
    },
    timeout=30
)

if baslat_svd.status_code != 201:
    raise Exception(f"SVD Reddedildi: {baslat_svd.text}")

video_output = bekle_ve_al(baslat_svd.json()["urls"]["get"])
video_url = video_output if isinstance(video_output, str) else video_output[0]
print("-> Hareketli video indiriliyor...")

with open("raw_loop.mp4", "wb") as f:
    f.write(requests.get(video_url).content)

print("3. Aşama: Orantıyı Bozmadan 60 Saniyeye Uzatma...")

# FFmpeg'in görüntüyü zorla sündürüp yamultmasını engelledik. 
# Artık orijinal yüksekliği koruyup, eksik kalan yerleri kırpmadan merkeze oturtacak.
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-stream_loop", "-1", "-i", "raw_loop.mp4",
    "-f", "lavfi", "-i", "anoisesrc=a=0.3:c=brown,lowpass=f=700",
    "-t", "60",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k",
    "final_shorts.mp4"
]

subprocess.run(ffmpeg_cmd, check=True)
print("İşlem Başarılı! Orantısı düzeltilmiş final_shorts.mp4 hazır.")
