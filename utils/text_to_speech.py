import requests

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai"
AI_API_KEY = "sk-YsqbaPD2sDcftsjdJG6FIA"  # Thay bằng API key của bạn

# --- Thực thi ---
url = f"{AI_API_BASE}/audio/speech"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {AI_API_KEY}"
}
data = {
  "model": "gemini-2.5-pro-preview-tts", # gemini-2.5-flash-preview-tts
  "input": "Hello world! This is a test of the text-to-speech API.",
  "voice": "Puck"
}

response = requests.post(url, headers=headers, json=data, stream=True)

if response.status_code == 200:
  with open("assets/speech_from_requests.mp3", "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
          f.write(chunk)
  print("File âm thanh đã được tạo thành công!")
else:
  print(f"Error: {response.status_code}")
  print(response.text)