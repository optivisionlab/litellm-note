import requests
import base64
import json
import wave

def tts_two_speakers(
    api_key: str,
    model: str,
    speaker1: str,
    voice1: str,
    speaker2: str,
    voice2: str,
    text: str,
    voice_name: str = "Kore",
    sample_rate: int = 24000,
    channels: int = 1,
    sample_width: int = 2,
    style: str | None = None,
    output_path: str = "output.wav"
) -> None:
    """
    Gọi API text-to-speech với 2 người nói và lưu file WAV.

    Parameters:
    - api_key: khóa API của AI Thực Chiến.
    - model: model ID, ví dụ "gemini-2.5-flash-preview-tts".
    - speaker1: tên người nói 1 (phải trùng với tên trong prompt).
    - voice1: tên giọng dựng sẵn cho người nói 1, ví dụ "Kore".
    - speaker2: tên người nói 2.
    - voice2: tên giọng dựng sẵn cho người nói 2.
    - text: đoạn hội thoại có cả người nói 1 và người nói 2.
    - output_wav_path: đường dẫn để lưu file WAV đầu ra.

    Returns: None (lưu file trên đĩa).
    """

    url = f"https://api.thucchien.ai/gemini/v1beta/models/{model}:generateContent"

    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }

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
                    "speakerVoiceConfigs": [
                        {
                            "speaker": speaker1,
                            "voiceConfig": {
                                "prebuiltVoiceConfig": {
                                    "voiceName": voice1
                                }
                            }
                        },
                        {
                            "speaker": speaker2,
                            "voiceConfig": {
                                "prebuiltVoiceConfig": {
                                    "voiceName": voice2
                                }
                            }
                        }
                    ]
                }
            }
        }
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()

    # giả sử lấy phần ứng viên đầu tiên
    audio_b64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    audio_bytes = base64.b64decode(audio_b64)

    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

    print(f"✅ File âm thanh đã lưu tại: {output_path}")
    print(f"🎤 Giọng: {voice_name} | Phong cách: {style or 'Mặc định'} | Tần số: {sample_rate}Hz")

    print(f"Saved audio to {output_path}")


api_key = "sk-YsqbaPD2sDcftsjdJG6FIA"
model   = "gemini-2.5-flash-preview-tts"

speaker1 = "Speaker1"
voice1   = "Kore"

speaker2 = "Speaker2"
voice2   = "Puck"

text = """Make Speaker1 sound tired and bored, and Speaker2 sound excited and happy:
Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess!"""

output_path = "test_dialogue.mp3"

tts_two_speakers(api_key, model,
                 speaker1, voice1,
                 speaker2, voice2,
                 text, output_path=output_path)
