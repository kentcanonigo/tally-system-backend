# Tally System Backend

This repository contains the backend for the Tally System, built using Django and PostgreSQL. It provides APIs for managing data and integrates with the frontend.

## 📌 Prerequisites
Ensure you have the following installed:
- Python 3.10+
- PostgreSQL
- Docker & Docker Compose
- Git

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/kentcanonigo/tally-system-backend
cd tally-system-backend
```

### 2️⃣ **Setup Environment Variables**
Create a `.env` file in the project root:
```ini
DB_NAME=tally_db
DB_USER=tally_user
DB_PASSWORD=tally_password
DB_HOST=127.0.0.1
DB_PORT=5432
DEBUG=True
```

### 3️⃣ **Run with Docker (Recommended)**
```sh
docker-compose up --build -d
```
This starts the Django backend and PostgreSQL database in separate containers.

### 4️⃣ **Run Locally (Without Docker)**
TODO: add steps for installing postgres (or refer to notion)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 **Testing the API with Postman**
1. Open Postman.
2. Set the **Base URL**: `http://localhost:8000/api/`
3. Example Request: **Create a Customer**
   - Endpoint: `POST /customers/`
   - Headers: `{ "Content-Type": "application/json" }`
   - Body:
     ```json
     {
       "name": "John Doe",
       "email": "john@example.com"
     }
     ```
4. Click **Send** and check the response.

---

## 🔄 **Useful Commands**
```sh
# Create migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for Django Admin)
python manage.py createsuperuser

# Run tests
pytest
```

---

## 📦 **Deployment**
For production, ensure:
- `DEBUG=False` in `.env`
- Use a **production-ready WSGI server** (e.g., Gunicorn)
- Enable **HTTPS** and configure a **reverse proxy** (e.g., Nginx)

---

## 📜 **Contributing**
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes and push: `git push origin feature-name`
4. Open a Pull Request.
