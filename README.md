# 🌌 Planetarium API

Planetarium API is a backend application for managing astronomy shows, themes, and other features of a digital planetarium system. Built with Django REST Framework and powered by PostgreSQL in Docker.

## 🚀 Features

- JWT authentication
- Admin vs Read-Only permissions
- Swagger API documentation
- Custom validations
- PostgreSQL with persistent volume
- Dockerized deployment

## 🛠️ Technology Stack

- Python 3.11
- Django & Django REST Framework
- PostgreSQL 16
- Docker & Docker Compose
- JWT (via SimpleJWT)

---

## 📦 How to Run the Project with Docker Compose
### 0. Python and Docker must be installed.
### 1. Clone the Repository

```bash
git clone https://github.com/Sonemon/py-drf-PlanetariumAPI.git
cd planetarium-api
```

### 2. Create .env file from sample
```env
# Django
SECRET_KEY=<your-secret-key>
DEBUG=True/False

# DB
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_DB=<db_name>
POSTGRES_HOST=<db_host>
POSTGRES_PORT=<db_port>
```

### 3. Build and Run
```bash
docker-compose up --build
```
### Docker Compose will:
- Build the Django app image
- Start PostgreSQL
- Wait until the database is ready
- Run migrations
- Start the Django development server

### 4. Create Superuser 👤
After running the containers, open a new terminal and run:
```bash
docker-compose exec web python manage.py createsuperuser
```
Then follow the prompts to set up your admin account.

## 📚 API Documentation
Swagger documentation is available at:
```html
http://localhost:8000/api/schema/swagger-ui/
```
ReDoc documentation is available at:
```html
http://localhost:8000/api/schema/redoc/
```
## 💾 Database Persistence
PostgreSQL data is stored in a Docker volume named planetarium_db. This means your data will persist across container restarts.