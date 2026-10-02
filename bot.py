import os
import time
import requests
import subprocess
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class RainVideoGenerator:
    def __init__(self):
        self.api_token = os.environ.get("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN çevre değişkeni (secret) bulunamadı!")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.model_url = "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions"
        
    def _wait_for_result(self, check_url: str, timeout_seconds: int = 120) -> str:
        """API'den sonucun gelmesini bekler."""
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            time.sleep(5)
            response = requests.get(check_url, headers=self.headers, timeout=30).json()
            status = response.get("status")
            
            if status == "succeeded":
                output = response.get("output")
                return output[0] if isinstance(output, list) else output
            elif status in ["failed", "canceled"]:
                raise Exception(f"Görsel üretimi başarısız oldu. Hata: {response.get('error')}")
            else:
                logging.info(f"Çiziliyor... (Durum: {status})")
                
        raise TimeoutError("Görsel üretimi zaman aşımına uğradı.")

    def generate_image(self, output_path: str = "source_image.jpg") -> str:
        """Flux modeli ile görseli üretir ve kaydeder."""
        logging.info("1. Aşama: Camında yağmur damlaları olan 8K görsel çiziliyor...")
        
        prompt = (
            "Masterpiece, cozy warm bedroom interior, a person sleeping peacefully under a warm blanket in bed. "
            "Massive window looking outside at heavy rain. MACRO PHOTOGRAPHY CLOSE UP of window glass completely "
            "covered in heavy water drops and dynamic rain streams sliding down the glass, reflecting warm street lights. "
            "Cinematic lighting, 8k resolution, perfectly proportioned, studio ghibli anime style."
        )
        
        payload = {
            "input": {
                "prompt": prompt,
                "aspect_ratio": "9:16",
                "output_format": "jpg"
            }
        }
        
        response = requests.post(self.model_url, headers=self.headers, json=payload, timeout=30)
        
        if response.status_code != 201:
            raise Exception(f"API İsteği Reddedildi: {response.text}")
            
        check_url = response.json()["urls"]["get"]
        image_url = self._wait_for_result(check_url)
        
        logging.info("Görsel çizildi, indiriliyor...")
        img_data = requests.get(image_url, timeout=30).content
        
        with open(output_path, "wb") as f:
            f.write(img_data)
            
        return output_path

    def create_video(self, image_path: str, output_video: str = "final_shorts.mp4", duration: int = 60):
        """İndirilen görseli dalgalanan yağmur sesleriyle birleştirerek video oluşturur."""
        logging.info("2. Aşama: Dinamik yağmur sesi ile FFmpeg montajı yapılıyor...")
        
        # SES MÜHENDİSLİĞİ: Yağmur şiddeti her 12 saniyede bir yavaşça artıp azalır.
        audio_filtergraph = (
            "anoisesrc=a=0.3:c=pink,highpass=f=300,lowpass=f=2500[base_rain]; "
            "anoisesrc=a=0.4:c=brown,highpass=f=200,lowpass=f=1200,"
            "volume='0.5+0.5*sin(2*PI*t/12)':eval=frame[gusts]; "
            "[base_rain][gusts]amix=inputs=2:duration=first:dropout_transition=2,volume=1.2[a_out]"
        )

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-framerate", "30", "-i", image_path,
            "-f", "lavfi", "-i", "anullsrc",
            "-t", str(duration),
            "-filter_complex", audio_filtergraph,
            "-map", "0:v", "-map", "[a_out]",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            output_video
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            logging.info(f"İşlem Başarılı! Dinamik yağmur sesli '{output_video}' oluşturuldu.")
        except subprocess.CalledProcessError as e:
            logging.error("FFmpeg işlemi sırasında bir hata oluştu.")
            raise e

if __name__ == "__main__":
    try:
        generator = RainVideoGenerator()
        image_file = generator.generate_image()
        generator.create_video(image_path=image_file)
    except Exception as err:
        logging.error(f"Sistem Hatası: {err}")
