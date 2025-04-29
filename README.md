---

````md
# Tally System Backend

This repository contains the backend for the Tally System, built using Django and PostgreSQL. It provides RESTful APIs for managing data and integrates with the frontend.

---

## 📌 Prerequisites

Ensure you have the following installed:

- Python 3.10+
- PostgreSQL
- Docker & Docker Compose
- Git

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/kentcanonigo/tally-system-backend
cd tally-system-backend
```
````

### 2️⃣ Environment Setup

Create a `.env` file in the project root:

```ini
DB_NAME=tally_db
DB_USER=tally_user
DB_PASSWORD=tally_password
DB_HOST=127.0.0.1
DB_PORT=5432
DEBUG=True
```

---

### 3️⃣ Running the Project

#### ✅ Using Docker (Recommended)

```sh
docker-compose up --build -d
```

This spins up both the Django backend and PostgreSQL in containers.

#### ⚙️ Local Run (Without Docker)

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 📘 API Documentation (Swagger & ReDoc)

Once the server is running (either via Docker or locally), the API documentation will be available automatically.

> 🧠 These docs are generated live based on the current models, serializers, and views.

### 🔗 Swagger UI (Interactive)

- URL: [http://localhost:8000/docs/swagger/](http://localhost:8000/docs/swagger/)
- Allows you to **test endpoints**, view request/response formats, and check status codes.

### 📖 ReDoc (Static, Clean Look)

- URL: [http://localhost:8000/docs/redoc/](http://localhost:8000/docs/redoc/)
- Ideal for referencing endpoint structures without interaction.

---

## 💡 For Frontend Developers

You don’t need to ask for backend routes manually — just open `/docs/swagger/` to see:

- All available endpoints (e.g., `/customers/`, `/tally-sessions/`, etc.)
- Expected payloads for POST/PUT
- Real-time request testing (no need for Postman)

This allows you to build or test the frontend quickly using **actual live data**.

---

## 🧪 Testing the API

You can still use Postman if preferred:

- **Base URL**: `http://localhost:8000/`
- Example Endpoint:
  ```http
  POST /customers/
  ```
  Body (JSON):
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```

---

## 🔄 Useful Commands

```sh
# Apply DB changes
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run backend tests
pytest
```

---

## 📦 Deployment Notes

When preparing for production:

- Set `DEBUG=False` in your `.env`
- Use Gunicorn or another WSGI server
- Serve via Nginx with HTTPS
- Protect the `/docs/` endpoints if needed (for security)

---

## 📜 Contributing

1. Fork this repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit and push your code
4. Open a Pull Request
