# Task Manager API

A lightweight async REST API for managing tasks, built with **FastAPI** and **aiosqlite**. Includes full CRUD operations, status filtering, and task completion tracking.

[![CI](https://github.com/adibmenchali/fastapi-tasks/actions/workflows/ci.yml/badge.svg)](https://github.com/adibmenchali/fastapi-tasks/actions/workflows/ci.yml)
---

## Tech Stack

- **FastAPI** — async web framework
- **aiosqlite** — async SQLite driver
- **Pydantic** — data validation and serialization
- **pytest + pytest-asyncio** — async test suite
- **GitHub Actions** — CI pipeline

---

## Features

- Create, read, update and delete tasks
- Filter tasks by status (`pending`, `in_progress`, `done`)
- Mark a task as complete with a dedicated endpoint (sets `completed_at` timestamp)
- Input validation with field constraints (title length, description length)
- Partial updates via `PATCH` — only send the fields you want to change
- Auto-generated interactive docs at `/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/tasks/` | List all tasks (optional `?status=` filter) |
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/{id}` | Get a single task |
| `PATCH` | `/tasks/{id}` | Partially update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `POST` | `/tasks/{id}/complete` | Mark a task as done |

### Task Schema

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "created_at": "2025-01-01T10:00:00Z",
  "completed_at": null
}
```

**Status values:** `pending` · `in_progress` · `done`

---

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (package manager)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

uv sync
```

### Run the server

```bash
uv run uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

---

## Running Tests

```bash
uv run pytest tests/ -v
```

---

## CI Pipeline

Every push to `main` or `dev` automatically triggers the GitHub Actions pipeline:

1. Installs dependencies
2. Runs the full test suite

If any test fails, the pipeline stops and the push is flagged. See the **Actions** tab for run history.