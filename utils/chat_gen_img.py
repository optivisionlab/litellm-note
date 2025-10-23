import requests
import json
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os


# sinh hình ảnh theo kiểu chat, nghĩa là có thể mô tả qua 1 nhân vật có trước
def api_chat_completions(content: str, image_filename: str, api_key: str, input_image_path: str = None):
    url = "https://api.thucchien.ai/chat/completions"
    
    parts = []
    
    # Luôn thêm phần văn bản vào parts
    parts.append({
        "type": "text",
        "text": content
    })
    
    # Nếu có đường dẫn ảnh, đọc và mã hóa nó, sau đó thêm vào parts
    if input_image_path:
        try:
            with open(input_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            # Giả sử định dạng là PNG, bạn có thể thay đổi nếu cần (ví dụ: image/jpeg)
            base64_image_url = f"data:image/png;base64,{encoded_string}"
            parts.append({
                "type": "image_url",
                "image_url": {
                    "url": base64_image_url
                }
            })
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn {input_image_path}. Bỏ qua hình ảnh đầu vào.")
            return # Thoát hàm nếu không tìm thấy ảnh đầu vào
        except Exception as e:
            print(f"Lỗi khi đọc hoặc mã hóa hình ảnh {input_image_path}: {e}. Bỏ qua hình ảnh đầu vào.")
            return # Thoát hàm nếu có lỗi xử lý ảnh

    # Cấu trúc messages_list với một tin nhắn duy nhất chứa list các parts
    messages_list = [
        {
          "role": "user",
          "content": parts
        }
    ]

    payload = json.dumps({
      "model": "gemini-2.5-flash-image-preview",
      "messages": messages_list,
      "modalities": [
        "image"
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {api_key}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print(data)
    try:
        image_data_url = data['choices'][0]['message']['images'][0]['image_url']['url']
        base64_string = image_data_url.split(',')[1]

        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))

        # Optional: Hiển thị hình ảnh (có thể bỏ qua nếu chỉ muốn lưu)
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Generated Image: {image_filename}")
        plt.show()

        img_np = np.array(img)
        cv2.imwrite(image_filename, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
        print(f"Hình ảnh đã được lưu thành: {image_filename}")
    except (KeyError, IndexError) as e:
        print(f"Không thể lấy dữ liệu hình ảnh từ phản hồi API: {e}")
        print(f"Phản hồi API: {response.text}")



api_key = os.getenv("API_KEY", "sk-1234")

# # --- Ví dụ 1: Chỉ với nội dung văn bản (tương tự cURL bạn cung cấp) ---
# print("\n--- Ví dụ 1: Chỉ với nội dung văn bản ---")
# content_only_text = "A breathtaking scene where a majestic waterfall cascades down rugged cliffs, shimmering like silver threads under the warm sunlight. Lush greenery surrounds the falls—towering trees, vibrant flowers, and soft moss painting nature’s perfect canvas. Mist rises gently, forming a magical rainbow that arches across the sky, while birds soar gracefully above as if dancing to the music of nature. A dreamlike moment that blends serenity and beauty in one stunning view."
# filename_only_text = "waterfall_scene.png"
# api_chat_completions(content_only_text, filename_only_text, api_key)

# --- Ví dụ 2: Với nội dung văn bản và đường dẫn ảnh đầu vào ---
print("\n--- Ví dụ 2: Với nội dung văn bản và đường dẫn ảnh đầu vào ---")
new_content = """
The Phantom Thief's design is characterized by a white suit, fedora, long cape, 
and signature monocle, creating an image that is both elegant and mysterious. 
He often appears amidst white smoke or under the moonlight, making each of his heists look like a grand magic show. 
The thief's features are similar to the man below.
"""

image_with_path_filename = "character_from_image_description.png"
sample_image_path = "assets/sherlock.png" # Sử dụng ảnh của bạn
api_chat_completions(new_content, image_with_path_filename, api_key, input_image_path=sample_image_path)
