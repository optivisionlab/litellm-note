import requests
import os

def text_to_speech(text_input, output_path, model="gemini-2.5-pro-preview-tts", voice="Puck"):
    """
    Converts text to speech using the thucchien.ai API and saves it to a file.

    Args:
        text_input (str): The text to convert to speech.
        output_path (str): The path to save the output audio file.
        model (str, optional): The TTS model to use. Defaults to "gemini-2.5-pro-preview-tts".
        voice (str, optional): The voice to use. Defaults to "Puck".
    """
    # --- Configuration ---
    AI_API_BASE = "https://api.thucchien.ai"
    AI_API_KEY = os.getenv("API_KEY")
    
    if not AI_API_KEY:
        raise ValueError("API_KEY environment variable not set. Please set it before running.")

    # --- Execution ---
    url = f"{AI_API_BASE}/audio/speech"
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {AI_API_KEY}"
    }
    data = {
      "model": model,
      "input": text_input,
      "voice": voice
    }

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Audio file successfully created at: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        # Try to print more details from the response if available
        if 'response' in locals() and response is not None:
            try:
                print(f"Error details: {response.json()}")
            except ValueError:
                print(f"Error details: {response.text}")
        return False

if __name__ == "__main__":
    # Example usage of the function
    
    print("========== start =========")
    prompt = '''
      Hello world! This is a test of the refactored text-to-speech function.
    '''
    output_filename = "speech_from_function.wav"

    # Ensure the assets directory exists
    assets_dir = "logs"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        
    output_filepath = os.path.join(assets_dir, output_filename)

    # Call the function
    text_to_speech(
      text_input=prompt, 
      output_path=output_filepath, 
      model="gemini-2.5-pro-preview-tts", 
      voice="Puck"
      )
    print("========== end =========")
