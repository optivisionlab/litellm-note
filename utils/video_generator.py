import requests
import base64
import time
import re
import os


BASE_URL = "https://api.thucchien.ai/gemini/v1beta"
DOWNLOAD_URL = "https://api.thucchien.ai/gemini/download/v1beta/files"

def start_video_generation(prompt, model, api_key, **params):
    """
    Bắt đầu tạo video bất đồng bộ.
    Returns: operation_name
    """
    url = f"{BASE_URL}/models/{model}:predictLongRunning"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": params
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    operation_name = data.get("name")
    print(f"✅ Tạo tác vụ thành công, operation_name = {operation_name}")
    return operation_name


def check_video_status(operation_name, api_key, wait=True, interval=10, timeout=300):
    """
    Kiểm tra trạng thái tạo video.
    Nếu wait=True, sẽ poll cho đến khi hoàn thành hoặc timeout.
    Returns: video_id hoặc None nếu chưa xong.
    """
    headers = {"x-goog-api-key": api_key}
    url = f"{BASE_URL}/{operation_name}"
    start_time = time.time()

    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        done = data.get("done", False)

        if done:
            try:
                uri = data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                print(f"🎬 Video sẵn sàng: {uri}")
                # Trích video_id từ URI Google API
                match = re.search(r'/files/([^:/]+)', uri)
                video_id = match.group(1) if match else None
                print(f"🎞 video_id = {video_id}")
                return video_id
            except Exception:
                print("⚠️ Không tìm thấy URI trong response.")
                return None

        if not wait:
            return None

        elapsed = time.time() - start_time
        if elapsed > timeout:
            print("⏰ Hết thời gian chờ, tác vụ chưa hoàn tất.")
            return None

        print(f"⏳ Chưa xong... chờ {interval}s rồi kiểm tra lại.")
        time.sleep(interval)


def download_video(video_id, api_key, output_path="output.mp4"):
    """
    Tải video đã sinh về máy.
    """
    headers = {"x-goog-api-key": api_key}
    url = f"{DOWNLOAD_URL}/{video_id}:download?alt=media"

    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"💾 Video đã tải về: {output_path}")
    return output_path


def start_video_with_image(prompt, image_path, model, api_key, **params):
    """
    Bắt đầu tạo video từ prompt + hình ảnh (image-to-video).
    Hình ảnh sẽ được mã hóa base64 và gửi kèm.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

    # Đọc file và mã hóa base64
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    # Xác định mime type
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"

    url = f"{BASE_URL}/models/{model}:predictLongRunning"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "instances": [{
            "prompt": prompt,
            "image": {
                "bytesBase64Encoded": img_base64,
                "mimeType": mime
            }
        }],
        "parameters": params
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    operation_name = data.get("name")
    print(f"✅ Đã tạo tác vụ image-to-video, operation_name = {operation_name}")
    return operation_name


# -------------------------
# 🧪 Ví dụ sử dụng: text 2 video

API_KEY = "sk-1234"
MODEL = "veo-3.0-generate-001"
PROMPT = "Video of the Vietnamese flag flying in Ba Dinh Square"

operation = start_video_generation(PROMPT, MODEL, API_KEY, aspectRatio="16:9", resolution="720p")
video_id = check_video_status(operation, API_KEY, wait=True, interval=15, timeout=600)
if video_id:
    download_video(video_id, API_KEY, output_path="assets/video_test_1.mp4")


# -------------------------
# 🧪 Ví dụ sử dụng: image 2 video

API_KEY = "sk-12343"
MODEL = "veo-3.0-generate-001"
PROMPT = "Video of the Vietnamese flag flying in Ba Dinh Square"
path_image = "assets/ba_dinh_hn.jpg"

operation = start_video_with_image(
        prompt=PROMPT,
        image_path=path_image,
        model=MODEL,
        api_key=API_KEY,
        aspectRatio="16:9",
        resolution="720p",
        personGeneration="allow_adult"
    )
video_id = check_video_status(operation, API_KEY, wait=True, interval=15, timeout=600)
if video_id:
    download_video(video_id, API_KEY, output_path="assets/ba_dinh_video.mp4")