# litellm-note

Dự án này chứa một bộ sưu tập các script Python để thực hiện các tác vụ liên quan đến AI, bao gồm chuyển văn bản thành giọng nói, tạo và chỉnh sửa hình ảnh, và tạo video.

## Chức năng

Tất cả các script tiện ích được đặt trong thư mục `utils/`.

### 1. Chuyển văn bản thành giọng nói (Text-to-Speech)

Các script này tương tác với API TTS của `api.thucchien.ai`.

*   **`utils/text_to_speech_gemini_single.py` (Khuyên dùng)**
    *   **Tính năng**: Hỗ trợ cả một và nhiều người nói, tự động phát hiện định dạng âm thanh (`.mp3`, `.wav`), và có cơ chế xử lý lỗi chi tiết. Đây là script linh hoạt và mạnh mẽ nhất.
*   **Các script khác**: `_gemini_multi.py`, `_gemini_2_person.py`, và `text_to_speech.py` là các phiên bản cũ hơn hoặc ít linh hoạt hơn. Chức năng của chúng đã được tích hợp trong `text_to_speech_gemini_single.py`.

### 2. Tạo và Chỉnh sửa Hình ảnh

Các script này sử dụng nhiều mô hình và endpoint khác nhau để tạo và tùy chỉnh hình ảnh.

*   **`utils/edit_img_from_prompt.py` (Tạo & Chỉnh sửa)**
    *   **Tính năng**: Sử dụng mô hình Gemini (`gemini-2.5-flash-image-preview`) để vừa **tạo ảnh mới** từ văn bản, vừa **chỉnh sửa một ảnh có sẵn** dựa trên mô tả.
    *   **Endpoint**: `/gemini/v1beta/models/...:generateContent`

*   **`utils/gen_single_img.py` (Tạo hàng loạt)**
    *   **Tính năng**: Sử dụng mô hình `imagen-4` để tạo ra **một hoặc nhiều hình ảnh** từ một mô tả văn bản duy nhất.
    *   **Endpoint**: `/images/generations`

*   **`utils/chat_gen_img.py` (Tạo ảnh kiểu "trò chuyện")**
    *   **Tính năng**: Tạo ảnh dựa trên mô tả văn bản và có thể nhận một hình ảnh đầu vào để "trò chuyện" hoặc tạo ra một nhân vật/khung cảnh tương tự.
    *   **Endpoint**: `/chat/completions`

### 3. Tạo Video

Các script này sử dụng mô hình Veo của Google để tạo video từ văn bản hoặc hình ảnh. Quá trình này là bất đồng bộ (yêu cầu thời gian để xử lý).

*   **`utils/gen_video_async_from_btc.py` (Workflow hoàn chỉnh)**
    *   **Tính năng**: Cung cấp một lớp `VeoVideoGenerator` để quản lý toàn bộ quy trình: bắt đầu tạo video, tự động kiểm tra trạng thái cho đến khi hoàn thành, và tải video về.
    *   **Đầu vào**: Chỉ hỗ trợ tạo video từ văn bản (text-to-video).

*   **`utils/video_generator.py` (Các hàm riêng lẻ)**
    *   **Tính năng**: Cung cấp các hàm độc lập cho từng bước: `start_video_generation`, `check_video_status`, `download_video`.
    *   **Điểm nổi bật**: Hỗ trợ cả tạo video từ văn bản (**text-to-video**) và từ hình ảnh (**image-to-video**) thông qua hàm `start_video_with_image`.

## Hướng dẫn sử dụng chung

1.  **Cấu hình API Key**: Mở file script bạn muốn sử dụng và thay thế giá trị API key (thường là `"sk-1234"`) bằng API key hợp lệ của bạn.
2.  **Cài đặt thư viện**:
    ```bash
    pip install -r requirements.txt
    # Hoặc cài đặt thủ công nếu cần
    # pip install requests Pillow matplotlib opencv-python
    ```
3.  **Chạy script**:
    ```bash
    python utils/<tên_script>.py
    ```
4.  **Kiểm tra kết quả**: Các file media (âm thanh, ảnh, video) sẽ được tạo trong thư mục `assets/` hoặc thư mục được chỉ định trong script.
