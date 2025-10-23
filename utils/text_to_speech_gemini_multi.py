import requests
import base64
import json
import wave
from typing import List, Dict
import os

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

    # print(json.dumps(payload))
    print("===== Call API =======")
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
api_key = os.getenv("API_KEY", "sk-1234")
model   = "gemini-2.5-flash-preview-tts"

# Cấu hình cho 3 người nói khác nhau (sử dụng các giọng đã biết là hoạt động)
speakers_config = [
    {"speaker": "Minh Anh", "voice": "Kore"},
    {"speaker": "Quốc Trung", "voice": "Puck"},
]

# Đoạn hội thoại với tên người nói tương ứng (xóa khoảng trắng thừa ở đầu)
text = '''
**KỊCH BẢN PODCAST**
**Chủ đề:** Vai trò của trí tuệ nhân tạo (AI) trong phát triển giáo dục và xã hội
**Nhân vật:**
*   **Minh Anh:** Host, người dẫn dắt câu chuyện
*   **Quốc Trung:** Chuyên gia về AI
Đoạn hội thoaị như sau:
**Minh Anh:** Xin chào mừng quý vị và các bạn đã quay trở lại với kênh podcast "Tương Lai Số". Trong thế giới không ngừng biến đổi của chúng ta, trí tuệ nhân tạo, hay AI, đang ngày càng khẳng định vai trò không thể thiếu trong nhiều lĩnh vực. Hôm nay, chúng ta sẽ cùng chuyên gia AI, anh Quốc Trung, thảo luận sâu hơn về chủ đề "Vai trò của AI trong phát triển giáo dục và xã hội". Chào anh Trung!
**Quốc Trung:** Chào Minh Anh và xin chào quý vị khán giả. Rất vui khi được tham gia chương trình.
**Minh Anh:** Thưa anh, khi nói về AI trong giáo dục, nhiều người thường nghĩ đến những điều khá xa vời. Anh có thể chia sẻ những ứng dụng thực tế nhất của AI đang thay đổi cách chúng ta dạy và học không?
**Quốc Trung:** Chắc chắn rồi. Một trong những ứng dụng mạnh mẽ nhất là "cá nhân hóa lộ trình học tập". AI có thể phân tích năng lực, tốc độ tiếp thu và cả những lỗ hổng kiến thức của từng học sinh. Từ đó, hệ thống sẽ tự động đề xuất bài giảng, bài tập phù hợp, giúp các em không bị tụt lại phía sau và cũng không cảm thấy nhàm chán. Hãy tưởng tượng mỗi học sinh có một gia sư ảo 24/7, đó chính là sức mạnh của AI.
**Minh Anh:** Điều đó thật ấn tượng! Nó phá vỡ hoàn toàn mô hình "một chương trình cho tất cả" truyền thống. Vậy còn vai trò của giáo viên thì sao ạ? Liệu AI có thay thế họ?
**Quốc Trung:** Đó là một lo ngại phổ biến, nhưng tôi lại có góc nhìn khác. AI không thay thế giáo viên, mà sẽ trở thành một trợ thủ đắc lực. Khi AI đảm nhận các công việc lặp đi lặp lại như chấm bài trắc nghiệm, quản lý tài liệu, giáo viên sẽ có nhiều thời gian hơn để tập trung vào việc truyền cảm hứng, hướng dẫn kỹ năng mềm và tương tác sâu hơn với học sinh. Vai trò của họ được nâng tầm lên thành người cố vấn, người định hướng.
'''

# Sửa tên file đầu ra cho đúng định dạng
output_path = "logs/test_multi_speaker_dialogue.wav"

# Gọi hàm mới
tts_multi_speakers(api_key=api_key,
                   model=model,
                   speakers_config=speakers_config,
                   text=text,
                #    base_url="https://generativelanguage.googleapis.com", # Có thể thay đổi nếu cần
                   output_path=output_path)
