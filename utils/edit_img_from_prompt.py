import requests
import json
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np


# Hàm mới để sinh hoặc sửa ảnh bằng API Google Gemini
def generate_or_modify_image_gemini(prompt: str, output_filepath: str, api_key: str, 
                                    input_image_path: str = None, aspect_ratio: str = "1:1"):
    url = "https://api.thucchien.ai/gemini/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
    
    parts_list = [
        {"text": prompt}
    ]
    
    if input_image_path:
        try:
            with open(input_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            # Cố gắng suy luận mime_type từ phần mở rộng file hoặc mặc định là image/png
            mime_type = "image/png"
            if input_image_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = "image/jpeg"
            elif input_image_path.lower().endswith('.gif'):
                mime_type = "image/gif"

            parts_list.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": encoded_string
                }
            })
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file ảnh đầu vào tại đường dẫn {input_image_path}. Chỉ sinh ảnh từ prompt.")
            input_image_path = None # Đảm bảo không cố gắng sửa đổi nếu không tìm thấy ảnh
        except Exception as e:
            print(f"Lỗi khi đọc hoặc mã hóa hình ảnh đầu vào {input_image_path}: {e}. Chỉ sinh ảnh từ prompt.")
            input_image_path = None

    payload = json.dumps({
      "contents": [
        {
          "parts": parts_list
        }
      ],
      "generationConfig": {
          "imageConfig": {
              "aspectRatio": aspect_ratio
          }
      }
    })
    
    headers = {
      'Content-Type': 'application/json',
      'x-goog-api-key': api_key  # Sử dụng x-goog-api-key thay vì Authorization cho API Gemini
    }

    print(f"\nĐang gửi yêu cầu tới API Gemini với prompt: '{prompt[:50]}...' và ảnh đầu vào: {input_image_path is not None}\n")
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print("Phản hồi API Gemini:", data)

    try:
        # API Gemini trả về hình ảnh trong candidates[0].content.parts[0].inlineData.data
        image_base64_data = data['candidates'][0]['content']['parts'][0]['inlineData']['data']
        mime_type = data['candidates'][0]['content']['parts'][0]['inlineData']['mimeType']  # Sửa từ mime_type thành mimeType

        img_data = base64.b64decode(image_base64_data)
        img = Image.open(io.BytesIO(img_data))

        # Lưu ảnh
        # Cố gắng đảm bảo định dạng file đầu ra khớp với mime_type trả về nếu output_filepath không có extension
        final_output_filepath = output_filepath
        if '.' not in output_filepath or not output_filepath.split('.')[-1] in ['png', 'jpeg', 'jpg', 'gif']:
            extension = mime_type.split('/')[-1] if '/' in mime_type else 'png'
            final_output_filepath = f"{output_filepath}.{extension}"

        img_np = np.array(img)
        cv2.imwrite(final_output_filepath, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)) # OpenCV lưu theo BGR
        print(f"Hình ảnh đã được lưu thành: {final_output_filepath}")

        # Hiển thị ảnh (tùy chọn)
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Generated/Modified Image: {final_output_filepath}")
        plt.show()
        return final_output_filepath
    except KeyError as e:
        print(f"Lỗi: Không tìm thấy khóa {e} trong phản hồi API Gemini. Kiểm tra cấu trúc phản hồi.")
        print(f"Phản hồi đầy đủ: {data}")
    except IndexError as e:
        print(f"Lỗi: Index ngoài phạm vi. Có thể không có ứng viên hoặc phần nội dung nào trong phản hồi API Gemini: {e}")
        print(f"Phản hồi đầy đủ: {data}")
    except Exception as e:
        print(f"Lỗi khi xử lý hình ảnh từ phản hồi API Gemini: {e}")
        print(f"Phản hồi API đầy đủ: {data}")
    return None


api_key = 'sk-1234'

# --- Ví dụ 1: Sinh ảnh mới từ prompt bằng API Gemini ---
print("\n--- Ví dụ 1: Sinh ảnh mới từ prompt bằng API Gemini ---")
gemini_prompt_new_image = "the gray cat is going down the stairs"
gemini_output_new_image_filepath = "assets/cat_1.png"
generate_or_modify_image_gemini(gemini_prompt_new_image, gemini_output_new_image_filepath, api_key, aspect_ratio="16:9")

# --- Ví dụ 2: Sửa đổi ảnh hiện có bằng API Gemini ---
print("\n--- Ví dụ 2: Sửa đổi ảnh hiện có bằng API Gemini ---")
gemini_prompt_modify_image = "change the cat fur in the photo above to orange"
gemini_output_modified_image_filepath = "assets/cat_2.png"

# Đảm bảo file ảnh này tồn tại. Sử dụng ảnh vừa tạo hoặc một ảnh khác.
# Lưu ý: Nếu bạn chưa chạy Ví dụ 1, mystical_forest.png sẽ không tồn tại.
sample_input_image_to_modify_path = "assets/cat_1.png"

generate_or_modify_image_gemini(
    gemini_prompt_modify_image,
    gemini_output_modified_image_filepath,
    api_key,
    input_image_path=sample_input_image_to_modify_path,
    aspect_ratio="16:9"
)

print("\nCác file ảnh sẽ được lưu vào thư mục hiện tại.")
