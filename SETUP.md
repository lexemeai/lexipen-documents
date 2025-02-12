## Running AI Services

To run AI services, navigate to each AI service folder and start the service using its respective Docker Compose file. Ensure that models are placed in the designated directory alongside `app.py`, and configure the `.env` file for each service accordingly.

### Prerequisite: Navigate to the `/NE3-backend` directory

```bash
cd NE3-backend
```

### Running `whisper_file`

Navigate to the service directory:
```bash
cd AI_Services/whisper_file
```

#### Running on CPU:
```bash
docker compose -f docker-compose.cpu.yml build
docker compose -f docker-compose.cpu.yml up
```

#### Running on GPU:
```bash
docker compose -f docker-compose.gpu.yml build
docker compose -f docker-compose.gpu.yml up
```

### Running `whisper_streaming`

Navigate to the service directory:
```bash
cd ../whisper_streaming
```

#### Running on CPU:
```bash
docker compose -f docker-compose.cpu.yml build
docker compose -f docker-compose.cpu.yml up
```

#### Running on GPU:
```bash
docker compose -f docker-compose.gpu.yml build
docker compose -f docker-compose.gpu.yml up
```

## Running Django Backend

Navigate back to the main directory:
```bash
cd ../..
```

#### Building and running the Django service:
```bash
docker compose build
docker compose up
```

#### Running database migrations after building the container:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations users stt_file
docker compose exec web python manage.py migrate
```

### If you already have the Docker images:

If you have pre-built images, load them before running the project:
```bash
cd images
docker load -i ne3-backend-django.tar
docker load -i whisper_streaming-nevisa_file.tar
docker load -i whisper_file-nevisa_file.tar
```

## Running AI Services (Without Rebuilding)

### Running `whisper_file`
Navigate to the service directory:
```bash
cd AI_Services/whisper_file
```

#### Running on CPU:
```bash
docker compose -f docker-compose.cpu.yml up
```

#### Running on GPU:
```bash
docker compose -f docker-compose.gpu.yml up
```

### Running `whisper_streaming`
Navigate to the service directory:
```bash
cd ../whisper_streaming
```

#### Running on CPU:
```bash
docker compose -f docker-compose.cpu.yml up
```

#### Running on GPU:
```bash
docker compose -f docker-compose.gpu.yml up
```

## Running Django Backend (Without Rebuilding)

Navigate back to the main directory:
```bash
cd ../..
```

```bash
docker compose up
```

#### Running database migrations:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations users stt_file
docker compose exec web python manage.py migrate
```

## Authentication and API Access

To use the AI services, you need to create a user account and authenticate with an access token.

### **Sign Up a User**
Go to the following URL to register a new user:
👉 [http://localhost:8000/users/signup](http://localhost:8000/users/signup)

Once you sign up, you'll receive an **access token** that you must use to authenticate API requests.

### **Log In as an Existing User**
If you have already created a user, you can log in with your credentials at:
👉 [http://localhost:8000/users/login](http://localhost:8000/users/login)

This allows you to reuse your existing user account without signing up again.

### **Authentication Method**
The authentication system uses **Django's JWT (JSON Web Token)** authentication. If needed, you can use the **token refresh API** to manage token expiration and integrate authentication into your own service implementation.

### **Access API Documentation (Swagger UI)**
To explore and test the available API endpoints, visit:
👉 [http://localhost:8000/docs/](http://localhost:8000/docs/)

Use your access token to authenticate and start using the AI services! 🚀
Here is the requested section properly formatted in Markdown:

```md
# Running Sample Test Scripts

Once the AI services and the Django backend are up and running, you can test the system using the provided sample scripts.

## Setup a Virtual Environment

Before running the sample scripts, it's recommended to create a Python virtual environment and install the necessary dependencies:

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

2. **Install required dependencies:**
   ```bash
   pip install websockets requests
   ```

## Run Sample Scripts

### **Test File-Based Transcription**

To test `whisper_file`, run:
```bash
python3 sample_file.py
```

### **Test Streaming Transcription**

To test `whisper_streaming`, run:
```bash
python3 sample_streaming.py
```

These scripts will verify that the AI services are running correctly and can process input files or streaming data. If any errors occur, check the logs of the respective Docker containers using:

```bash
docker compose logs -f
```
