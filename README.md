# Review Management System

A production-ready FastAPI backend designed to manage review histories, calculate performance trends, and process sentiment analysis asynchronously.

## 🚀 Features

- **Trends API**: Calculates the top 5 categories based on the average stars of the *latest* version of each review.
- **Category API**: Fetches latest reviews for a specific category with **Cursor Pagination** (15 items per page).
- **Asynchronous Logging**: Uses **Celery** and **Redis** to log API access without blocking the main request flow.
- **LLM Integration**: Automatically detects and fills missing `tone` and `sentiment` using an LLM (with a graceful mock fallback for local testing).

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Task Queue**: Celery + Redis
- **Migrations**: Alembic
- **Containerization**: Docker & Docker-Compose

## 📦 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/himanshu3729k/ReviewHistory_backend
cd ReviewHistory_backend
```

### 2. Run with Docker

Ensure Docker Desktop is running, then execute:

```bash
docker-compose up --build
```

### 3. Initialize Database

```bash
docker-compose exec web alembic upgrade head
```

### 4. Access the API

Open the following URL in your browser to view the interactive Swagger UI:

```
https://reviews-api-olqp.onrender.com/docs
```

## 🧠 Architectural Highlights

- **Window Functions**: Utilized `ROW_NUMBER() OVER` to efficiently filter the latest review versions across thousands of records.
- **Resilience**: Implemented a mock fallback in the LLM service to ensure the system remains functional even if external API keys are missing.
- **Scalability**: Decoupled heavy logging and AI processing from the request-response cycle using background workers.

---
