import requests
import base64
import json
import wave
from typing import List, Dict

def tts_multi_speakers(
    api_key: str,
    model: str,
    speakers_config: List[Dict[str, str]],
    text: str,
    base_url: str = "https://api.thucchien.ai",
    sample_rate: int = 24000,
    channels: int = 1,
    sample_width: int = 2,
    output_path: str = "output.wav"
) -> None:
    # """
    # Gọi API text-to-speech với nhiều người nói và lưu file WAV.

    # Parameters:
    # - api_key: khóa API của AI Thực Chiến.
    # - model: model ID, ví dụ "gemini-2.5-flash-preview-tts".
    # - speakers_config: Danh sách các dictionary, mỗi dictionary chứa thông tin
    #   về một người nói. Ví dụ: [{"speaker": "Tên1", "voice": "Giọng1"}, ...].
    # - text: Đoạn hội thoại có tên của tất cả người nói.
    # - base_url: URL cơ sở của API.
    # - output_path: Đường dẫn để lưu file WAV đầu ra.

    # Returns: None (lưu file trên đĩa).
    # """

    url = f"{base_url}/gemini/v1beta/models/{model}:generateContent"

    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Tự động tạo cấu hình giọng nói từ danh sách đầu vào
    speaker_voice_configs = [
        {
            "speaker": config["speaker"],
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    "voiceName": config["voice"]
                }
            }
        }
        for config in speakers_config
    ]

    payload = {
        "contents": [
            {
                "parts": [
                    { "text": text }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "multiSpeakerVoiceConfig": {
                    "speakerVoiceConfigs": speaker_voice_configs
                }
            }
        }
    }

    print(json.dumps(payload))
    
    resp = requests.post(url, headers=headers, json=payload)

    # Kiểm tra và in ra lỗi chi tiết nếu có
    if resp.status_code != 200:
        print(f"Lỗi từ API: {resp.status_code}")
        print("Nội dung phản hồi:")
        print(resp.text)
        resp.raise_for_status()

    result = resp.json()

    # Giả sử lấy phần ứng viên đầu tiên
    audio_b64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    audio_bytes = base64.b64decode(audio_b64)

    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

    print(f"✅ File âm thanh đã lưu tại: {output_path}")
    print(f"🎤 Tần số: {sample_rate}Hz")


# --- VÍ DỤ SỬ DỤNG ---
# !!! QUAN TRỌNG: Vui lòng thay thế bằng API key hợp lệ của bạn.
# API key trong ví dụ có thể đã hết hạn.
api_key = "sk-1234" 
model   = "gemini-2.5-flash-preview-tts"

# Cấu hình cho 3 người nói khác nhau (sử dụng các giọng đã biết là hoạt động)
speakers_config = [
    {"speaker": "Narrator", "voice": "Kore"},
    {"speaker": "Wizard", "voice": "Kore"},
    {"speaker": "Knight", "voice": "Kore"} # Tạm thời dùng lại giọng "Kore" để tránh lỗi
]

# Đoạn hội thoại với tên người nói tương ứng (xóa khoảng trắng thừa ở đầu)
text = """Narrator: The brave Knight entered the dark cave, his sword held high.
Knight: Wizard, show yourself! I am not afraid.
Wizard: (cackles) Foolish mortal! You dare challenge me?"""

# Sửa tên file đầu ra cho đúng định dạng
output_path = "logs/test_multi_speaker_dialogue.mp3"

# Gọi hàm mới
tts_multi_speakers(api_key=api_key,
                   model=model,
                   speakers_config=speakers_config,
                   text=text,
                #    base_url="https://generativelanguage.googleapis.com", # Có thể thay đổi nếu cần
                   output_path=output_path)
