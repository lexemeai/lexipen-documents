import asyncio
import websockets
import requests
import os
import wave
import re

# API Endpoints
LOGIN_URL = "http://0.0.0.0:8000/users/login/"
WEBSOCKET_URL = "ws://localhost:8002/ws/"

# User Credentials (Replace with actual credentials)
USERNAME = "testuser"
PASSWORD = "testpass"

# File path to upload (Replace with actual path)
FILE_PATH = "test_audio/test_audio.wav"
RESULT_FILE = "results.txt"

def get_access_token():
    """Logs in and retrieves the access token."""
    response = requests.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        access_token = response.json().get("access")
        print("Login successful. Access token retrieved.")
        return access_token
    else:
        print(f"Login failed: {response.text}")
        return None

async def stream_audio_and_transcribe(file_path, uri):
    """Streams audio to WebSocket ASR server and receives transcription."""
    transcription = []
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server at {uri}.")
            
            with wave.open(file_path, "rb") as wav_file:
                if wav_file.getsampwidth() != 2:
                    raise ValueError("Only PCM16 WAV files are supported.")
                
                print("Streaming audio...")
                while True:
                    chunk = wav_file.readframes(4096*2)
                    if not chunk:
                        break
                    await websocket.send(chunk)
                    
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=10)
                        if response:
                            transcription.append(response)
                            print(f"Received transcript: {response}")
                    except asyncio.TimeoutError:
                        pass
                
                await websocket.send(b"")  # Indicate end of stream
                print("Audio streaming complete.")
                
                while True:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=10)
                        if response:
                            transcription.append(response)
                            print(f"Final transcript: {response}")
                        else:
                            break
                    except asyncio.TimeoutError:
                        break
        
        # Filter out numbers from the transcription
        clean_transcription = " ".join(re.sub(r"\d+", "", text).strip() for text in transcription if text.strip())
        
        return clean_transcription if clean_transcription else "No transcription received."

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket closed by server.")
        return "No transcription received."
    except Exception as e:
        print(f"Error while streaming audio: {e}")
        return "Error during WebSocket communication."

if __name__ == "__main__":
    token = get_access_token()
    if token:
        loop = asyncio.get_event_loop()
        transcription = loop.run_until_complete(stream_audio_and_transcribe(FILE_PATH, WEBSOCKET_URL))
        
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            f.write(transcription)
        
        print(f"Transcription saved to: {os.path.abspath(RESULT_FILE)}")
