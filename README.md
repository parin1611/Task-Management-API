# Task Management API

A small production-style REST API built with:

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Pydantic
- JWT authentication
- Argon2 password hashing
- Pytest
- Uvicorn
- Docker
- GitHub Actions

## Features

- User registration
- JWT login
- Secure password hashing
- Authenticated task management
- Per-user task ownership
- Health check
- OpenAPI/Swagger documentation
- SQLite for local development
- Environment-based configuration
- Docker support
- GitHub Actions CI

## Project Structure

```text
task-management-api/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   └── schemas/
│       ├── auth.py
│       └── task.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_health.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
