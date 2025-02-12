# Using LexiPen with Django

## Overview
This document provides instructions on how to use the two AI services (`whisper_file` and `whisper_streaming`) through Django.

---

## Authentication
Before using the API, you must authenticate using Django's JWT authentication system.

### **Sign Up a User**
Register a new user by sending a POST request to:
```plaintext
http://localhost:8000/users/signup
```

### **Log In as an Existing User**
If you already have an account, log in at:
```plaintext
http://localhost:8000/users/login
```

Upon successful authentication, you will receive an **access token**. Use this token in the `Authorization` header for API requests.

You can also refresh your token using Django's **token refresh API**.

---

## Whisper File AI Service
The `whisper_file` service provides AI-powered transcription of audio and video files.

### **1. Submit an Audio URL for Transcription**
- **Endpoint:** `POST /stt_file/url/`
- **Authentication Required:** Yes
- **Request Body:**
  ```json
  {
    "url": "https://example.com/audio.mp3",
    "timestamp": true
  }
  ```
- **Response:**
  ```json
  {
    "task_id": "12345abcde",
    "status": "pending",
    "message": "Transcription task created successfully."
  }
  ```

### **2. Upload an Audio File for Transcription**
- **Endpoint:** `POST /stt_file/upload/`
- **Authentication Required:** Yes
- **Request Body:** Multipart form-data with an audio file (`.mp3`, `.wav`, `.mp4`, etc.).
- **Response:**
  ```json
  {
    "task_id": "67890fghij",
    "status": "pending",
    "message": "File uploaded successfully and queued for transcription."
  }
  ```

### **3. Retrieve Transcription Results**
- **Endpoint:** `GET /stt_file/result/{stt_result_key}/`
- **Authentication Required:** Yes
- **Response:**
  ```json
  {
    "task_id": "12345abcde",
    "status": "completed",
    "transcription": "This is the transcribed text from the audio file."
  }
  ```

### **4. List Uploaded Audio Files**
- **Endpoint:** `GET /stt_file/list/`
- **Authentication Required:** Yes
- **Response:**
  ```json
  {
    "files": [
      {"file_id": "1", "name": "audio1.mp3", "status": "completed"},
      {"file_id": "2", "name": "audio2.wav", "status": "pending"}
    ]
  }
  ```

### **5. Retrieve Model Information**
- **Endpoint:** `GET /stt_file/model_info/`
- **Authentication Required:** Yes
- **Response:**
  ```json
  {
    "model": "Whisper v2.0",
    "language": "English",
    "accuracy": "98%"
  }
  ```

### **6. Update Application**
- **Endpoint:** `POST /stt_file/update-application/`
- **Authentication Required:** Yes
- **Request Body:** Multipart form-data with a ZIP file.
- **Response:**
  ```json
  {
    "message": "Application updated successfully."
  }
  ```

### **7. Retrieve UniKey Data**
- **Endpoint:** `GET /api/unikey-data/`
- **Authentication Required:** Yes
- **Response:**
  ```json
  {
    "unikey": {
      "status": "connected",
      "valid_until": "2025-12-31"
    }
  }
  ```

---

## AI Streaming Service
The `whisper_streaming` service allows real-time audio transcription using WebSocket.

### **1. Upload and Transcribe an Audio File**
- **Endpoint:** `POST /stt_streaming/stream/`
- **Authentication Required:** Yes
- **Request Body:** Multipart form-data with a `.wav` file.
- **Response:**
  ```json
  {
    "session_id": "abcdef123456",
    "status": "streaming",
    "message": "Streaming session started."
  }
  ```

### **2. Check WebSocket Server Status**
- **Endpoint:** `GET /stt_streaming/websocket-info/`
- **Authentication Required:** Yes
- **Response:**
  ```json
  {
    "status": "connected",
    "message": "WebSocket server is running."
  }
  ```

---

## API Documentation
For a full list of available API endpoints and request formats, visit:
```plaintext
http://localhost:8000/docs/
```

Use your access token to test API requests using Swagger UI.

---

## Conclusion
These AI services allow seamless transcription of audio and video files, whether by file upload or streaming. Ensure you authenticate before making requests and check the documentation for additional details.


