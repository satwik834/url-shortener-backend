# URL Shortener Backend

A robust and scalable URL Shortener backend built with **FastAPI**, **PostgreSQL** (via SQLAlchemy & Alembic), and **Redis** (for rate-limiting and fast operational tracking). It provides a full set of features including User Authentication, URL Shortening (with Base62 encoding), Rate Limiting, and Click Tracking.

## Features
- **User Authentication**: Secure registration and login using JWT (`python-jose`) and Argon2 password hashing.
- **URL Shortening**: Base62 encoded short links for maximum brevity.
- **Link Management**: Users can retrieve all their shortened links or delete specific short links.
- **Click Tracking**: High-performance click tracking using Redis (which can be flushed back to PostgreSQL).
- **Rate Limiting**: Protects shortening endpoints against spam/abuse per user.
- **Dockerized**: Ready-to-go `Dockerfile` and `entrypoint.sh` for seamless containerized deployment.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy & Alembic
- **Caching & Rate Limiting**: Redis
- **Authentication**: JWT & Argon2

## Prerequisites
- Python 3.12+
- PostgreSQL server running locally or accessible
- Redis server running locally or accessible

## Environment Variables
The application requires a `.env` file at the root of the `backend/` directory. Create one and populate the following based on your setup:
```env
# Database configuration
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis configuration
REDIS_URL=redis://localhost:6379/0

# Authentication
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Local Installation

1. **Clone the repository** (if you haven't already) and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Run the Development Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`. You can access the interactive Swagger UI at `http://localhost:8000/docs`.

## Docker Deployment

The backend is fully dockerized. To build and run using Docker:

1. **Build the image**:
   ```bash
   docker build -t url-shortener-backend .
   ```

2. **Run the container**:
   _Ensure you pass your environment variables or a `.env` file._
   ```bash
   docker run -p 8000:8000 --env-file .env url-shortener-backend
   ```
   *Note: Using `docker-compose.yml` is recommended to orchestrate PostgreSQL, Redis, and this API container together.*

## API Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Health check route | No |
| `POST` | `/register` | Register a new user | No |
| `POST` | `/login` | Authenticate user & get access token | No |
| `POST` | `/shorten` | Shorten a provided long URL | Yes |
| `GET` | `/links` | Fetch all URLs shortened by current user | Yes |
| `GET` | `/{short_code}` | Redirect to the original long URL | No |
| `DELETE`| `/{short_code}` | Delete a specific short link | Yes |
| `POST` | `/test/me` | Test current authentication context | Yes |
| `POST` | `/admin/flush_clicks` | Flush Redis click counts to PostgreSQL database | No |

## Contributing
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License
Distributed under the MIT License. See `LICENSE` for more information.
