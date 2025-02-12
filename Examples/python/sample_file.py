import requests
import time
import os

# API Endpoints
LOGIN_URL = "http://0.0.0.0:8000/users/login/"
UPLOAD_URL = "http://0.0.0.0:8000/stt_file/upload/"
RESULT_URL = "http://0.0.0.0:8000/stt_file/result/{result_key}/"

# User Credentials (Replace with actual credentials)
USERNAME = "testuser"
PASSWORD = "testpass"

# File path to upload (Replace with actual path)
FILE_PATH = "test_audio/test_audio.wav"
# Output file path
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

def upload_file(access_token):
    """Uploads an audio file and retrieves the result key."""
    headers = {"Authorization": f"Bearer {access_token}"}
    with open(FILE_PATH, "rb") as file:
        files = {"file": (FILE_PATH, file, "audio/wav")}
        response = requests.post(UPLOAD_URL, files=files, headers=headers)

    if response.status_code == 201:
        result_key = response.json().get("stt_result_key")
        print(f"File uploaded successfully. Result Key: {result_key}")
        return result_key
    else:
        print(f"Upload failed: {response.text}")
        return None

def get_transcription(result_key, access_token):
    """Polls the API until the transcription is completed and saves it to a file."""
    headers = {"Authorization": f"Bearer {access_token}"}
    while True:
        response = requests.get(RESULT_URL.format(result_key=result_key), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("stt_result_status")

            if status == "success":
                transcription = data.get("stt_result_script")
                
                # Save to file
                with open(RESULT_FILE, "w", encoding="utf-8") as f:
                    f.write(transcription)
                
                # Display file path
                abs_path = os.path.abspath(RESULT_FILE)
                print(f"\nTranscription saved to: {abs_path}")
                break
            elif status == "failed":
                print("Transcription failed.")
                break
            else:
                print("Processing... Checking again in 15 seconds.")
                time.sleep(15)
        else:
            print(f"Error retrieving transcription: {response.text}")
            break

if __name__ == "__main__":
    token = get_access_token()
    if token:
        result_key = upload_file(token)
        if result_key:
            get_transcription(result_key, token)
