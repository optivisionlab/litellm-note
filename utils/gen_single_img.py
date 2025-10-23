import requests
import json
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os


def generate_image_from_prompt(prompt: str, image_filename: str, 
                               api_key: str, n: int = 1, aspect_ratio: str = "1:1"):
    url = "https://api.thucchien.ai/images/generations"

    payload = json.dumps({
      "model": "imagen-4",
      "prompt": prompt,
      "n": n,
      "aspect_ratio": aspect_ratio
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {api_key}'
    }

    print(f"Đang tạo ảnh với prompt: '{prompt[:50]}...'\n")
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print("Phản hồi API tạo ảnh:", data)

    try:
        # API này trả về một list các đối tượng data, mỗi đối tượng có b64_json
        for i, item in enumerate(data['data']):
            if 'b64_json' in item:
                base64_string = item['b64_json']
                img_data = base64.b64decode(base64_string)
                img = Image.open(io.BytesIO(img_data))

                # Lưu ảnh
                current_filename = f"{image_filename.split('.')[0]}_{i}.png"
                img_np = np.array(img)
                cv2.imwrite(current_filename, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
                print(f"Hình ảnh đã được lưu thành: {current_filename}")

                # Hiển thị ảnh (tùy chọn)
                plt.imshow(img)
                plt.axis('off')
                plt.title(f"Generated Image ({i+1}/{n}): {current_filename}")
                plt.show()
            elif 'url' in item:
                # Nếu API trả về URL, bạn sẽ cần một cách khác để tải và lưu ảnh
                print(f"API trả về URL: {item['url']}. Hiện tại chưa hỗ trợ tải ảnh từ URL.")
            else:
                print(f"Phản hồi không chứa b64_json hoặc url cho ảnh thứ {i+1}.")
    except KeyError as e:
        print(f"Lỗi: Không tìm thấy khóa {e} trong phản hồi API. Đảm bảo phản hồi có trường 'data' và 'b64_json'.")
        print(f"Phản hồi đầy đủ: {data}")
    except Exception as e:
        print(f"Lỗi khi xử lý hình ảnh: {e}")
        print(f"Phản hồi API đầy đủ: {data}")


print("\n--- Ví dụ 3: Tạo ảnh từ prompt bằng API images/generations ---")

prompt_text = """
The anime-style thief's design is characterized by a white suit, fedora, long coat, and signature monocle, 
creating an image that is both elegant and mysterious. He often appears amidst white smoke or under the moonlight, 
making each of his heists look like a grand magic show.
"""

output_image_filename = "assets/anime_thief.png"
api_key = os.getenv("API_KEY", "sk-1234")

generate_image_from_prompt(prompt_text, output_image_filename, api_key, n=1, aspect_ratio="1:1")

print("\nCác file ảnh sẽ được lưu vào thư mục hiện tại.")
