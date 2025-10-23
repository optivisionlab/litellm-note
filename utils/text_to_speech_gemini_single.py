import requests
import base64
import wave
import os


def gemini_tts(
    api_key: str,
    text: str,
    model: str = "gemini-2.5-flash-preview-tts",
    voice_name: str = "Kore",
    sample_rate: int = 24000,
    channels: int = 1,
    sample_width: int = 2,
    style: str | None = None,
    output_path: str = "output.wav"
):
    """
    Hàm gọi API Text-to-Speech của Gemini (AI Thực Chiến)
    và lưu kết quả thành file .wav có thể nghe được.

    Parameters
    ----------
    api_key : str
        Khóa API từ https://thucchien.ai
    text : str
        Văn bản cần đọc.
    model : str
        Mô hình TTS sử dụng (mặc định: 'gemini-2.5-flash-preview-tts')
    voice_name : str
        Giọng đọc (ví dụ: 'Kore', 'Breeze', 'Zephyr', ...)
    sample_rate : int
        Tần số lấy mẫu (Hz), mặc định 24000
    channels : int
        Số kênh (1=mono)
    sample_width : int
        Số byte mỗi mẫu (2 = 16-bit)
    style : str | None
        Phong cách nói (ví dụ: "cheerful", "sad", "serious").
        Nếu có, chỉ thị sẽ được chèn vào text mà không bị đọc ra.
    output_path : str
        File âm thanh đầu ra (.wav)
    """

    # Chuẩn bị payload text
    text_prompt = text
    if style:
        text_prompt = f"Make the voice sound {style}.\n{text}"

    payload = {
        "contents": [
            {"parts": [{"text": text_prompt}]}
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": voice_name}
                }
            }
        }
    }

    url = f"https://api.thucchien.ai/gemini/v1beta/models/{model}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Gọi API
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # Giải mã âm thanh base64
    audio_base64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    audio_bytes = base64.b64decode(audio_base64)

    # Lưu thành WAV (PCM 16-bit, 24kHz)
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

    print(f"✅ File âm thanh đã lưu tại: {output_path}")
    print(f"🎤 Giọng: {voice_name} | Phong cách: {style or 'Mặc định'} | Tần số: {sample_rate}Hz")

    return output_path



print("======= start ======")
# --- Ví dụ sử dụng 1 dọng ---
AI_API_KEY = os.getenv("API_KEY", "sk-1234") # Thay bằng API key của bạn

prompt = """
    Chúc bạn một ngày thật vui vẻ!
"""

gemini_tts(
    api_key=AI_API_KEY, 
    text=prompt, 
    model= "gemini-2.5-flash-preview-tts", 
    voice_name="Kore", 
    style="cheerful",
    output_path="logs/single_speech.wav"
)
print("======= end ======")