import requests
import base64
import os
from typing import Union, List, Dict

# --- Cấu hình ---
# QUAN TRỌNG: Thay 'sk-1234' bằng API key hợp lệ của bạn từ thucchien.ai
# Lỗi 401 ("Authentication Error") xảy ra khi key này không hợp lệ hoặc bị thiếu.
AI_API_KEY = "sk-1234" 

# --- Model và Endpoint ---
BASE_URL = "https://api.thucchien.ai/gemini/v1beta/models"

def generate_speech_gemini(
    text: str,
    output_path: str,
    model: str = "gemini-2.5-pro-preview-tts",
    speakers: Union[str, List[Dict[str, str]]] = "Kore"
) -> bool:
    """
    Tạo file âm thanh từ văn bản sử dụng API Gemini Text-to-Speech của thucchien.ai.

    Args:
        text (str): Văn bản cần chuyển thành giọng nói.
        output_path (str): Đường dẫn để lưu file âm thanh đầu ra (ví dụ: 'assets/speech.mp3').
        model (str): Model Gemini TTS sẽ sử dụng.
        speakers (Union[str, List[Dict[str, str]]]): 
            - Για 1 người nói: Tên của giọng nói (ví dụ: "Kore", "Puck").
            - Για nhiều người nói: Một danh sách các dictionary, mỗi dict chứa 'speaker' và 'voiceName'.
              Ví dụ: [{"speaker": "Speaker1", "voiceName": "Puck"}, {"speaker": "Speaker2", "voiceName": "Zephyr"}]

    Returns:
        bool: True nếu thành công, False nếu có lỗi.
    """
    url = f"{BASE_URL}/{model}:generateContent"
    headers = {
        "x-goog-api-key": AI_API_KEY, # Sử dụng header theo tài liệu Gemini
        "Content-Type": "application/json"
    }

    # Xây dựng speechConfig dựa trên đầu vào `speakers`
    speech_config = {}
    if isinstance(speakers, str):
        # Trường hợp một người nói
        speech_config = {
            "voiceConfig": {
                "prebuiltVoiceConfig": {"voiceName": speakers}
            }
        }
    elif isinstance(speakers, list):
        # Trường hợp nhiều người nói
        speaker_voice_configs = []
        for speaker_info in speakers:
            speaker_voice_configs.append({
                "speaker": speaker_info["speaker"],
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": speaker_info["voiceName"]}
                }
            })
        speech_config = {
            "multiSpeakerVoiceConfig": {
                "speakerVoiceConfigs": speaker_voice_configs
            }
        }

    # Xây dựng toàn bộ request body
    data = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": speech_config
        }
    }

    # Gửi yêu cầu
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Ném lỗi nếu status code là 4xx hoặc 5xx

        response_data = response.json()
        # Trích xuất cả dữ liệu âm thanh và mime type
        audio_part = response_data["candidates"][0]["content"]["parts"][0]
        audio_data_base64 = audio_part["inlineData"]["data"]
        mime_type = audio_part.get("inlineData", {}).get("mimeType", "audio/mpeg") # Mặc định là mp3 nếu không có
        
        print(f"API trả về định dạng âm thanh: {mime_type}")

        # Xác định phần mở rộng file từ mime type
        extension = ".mp3" # Mặc định
        if mime_type == "audio/mpeg":
            extension = ".mp3"
        elif mime_type == "audio/wav":
            extension = ".wav"
        elif mime_type == "audio/ogg":
            extension = ".ogg"
        
        # Tạo tên file cuối cùng với phần mở rộng đúng
        final_output_path = os.path.splitext(output_path)[0] + extension
        
        audio_bytes = base64.b64decode(audio_data_base64)
        
        # Tạo thư mục nếu chưa tồn tại
        output_dir = os.path.dirname(final_output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(final_output_path, "wb") as f:
            f.write(audio_bytes)
            
        print(f"File âm thanh đã được tạo thành công tại: {final_output_path}")
        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"Lỗi HTTP: {http_err}")
        print(f"Nội dung phản hồi: {response.text}")
    except (KeyError, IndexError) as e:
        print(f"Không tìm thấy dữ liệu âm thanh trong phản hồi: {e}")
        print("Phản hồi nhận được:", response.text)
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")
    
    return False

# --- MAIN: Ví dụ cách sử dụng ---
if __name__ == "__main__":
    # --- Ví dụ 1: Một người nói ---
    print("--- Đang tạo file âm thanh cho một người nói ---")
    single_speaker_text = "Xin chào Việt Nam, tôi là Quang"
    single_speaker_output = os.path.join("assets", "speech_single_speaker.mp3")
    generate_speech_gemini(
        text=single_speaker_text,
        output_path=single_speaker_output,
        speakers="Zephyr" # Chọn một giọng nói khác
    )
    print("-" * 20)

    # --- Ví dụ 2: Nhiều người nói ---
    print("--- Đang tạo file âm thanh cho nhiều người nói ---")
    multi_speaker_text = """
    Hôm nay trời thật đẹp cùng đến với phóng sự sau:
    Speaker1: Hôm nay bạn có đi đâu không ?
    Speaker2: Hôm nay tôi đi chơi ở hồ tây.
    """
    multi_speaker_output = os.path.join("assets", "speech_multi_speaker.mp3")
    speaker_definitions = [
        {"speaker": "Speaker1", "voiceName": "Puck"},
        {"speaker": "Speaker2", "voiceName": "Leda"}
    ]
    generate_speech_gemini(
        text=multi_speaker_text,
        output_path=multi_speaker_output,
        speakers=speaker_definitions
    )
    print("-" * 20)
