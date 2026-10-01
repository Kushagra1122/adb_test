# Adbrew Todo App

Full-stack todo assignment for the Adbrew Backend SDE Intern role.

**Stack:** React (hooks) · Django REST · MongoDB · Docker Compose

## Features

- Create todos via form → `POST /todos/` → MongoDB
- List todos from backend → `GET /todos/` (no hardcoded data)
- List refreshes automatically after create
- Layered backend (repository → service → views) with validation and error handling
- Modular frontend (`api` / `hooks` / `components`)

## Project structure

```
├── Dockerfile
├── docker-compose.yml
└── src/
    ├── app/                 # React frontend (:3000)
    │   └── src/
    │       ├── api/         # HTTP client
    │       ├── components/  # TodoList, TodoForm
    │       └── hooks/       # useTodos
    ├── rest/                # Django API (:8000)
    │   └── rest/
    │       ├── views.py
    │       └── todos/       # repository, service, exceptions
    ├── requirements.txt
    └── db/                  # Mongo data volume (gitignored)
```

## Setup

### Prerequisites

- Docker Desktop
- Docker Compose

### Run

```bash
# from the repository root
export ADBREW_CODEBASE_PATH="$(pwd)/src"

docker-compose build
docker-compose up -d
```

### Verify

```bash
docker ps
# expect containers: app, api, mongo
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000/todos/ |
| MongoDB | `localhost:27017` |

### Useful commands

```bash
docker logs -f --tail=100 api
docker logs -f --tail=100 app
docker exec -it api bash
docker-compose down
```

## API

| Method | Path | Body | Response |
|--------|------|------|----------|
| `GET` | `/todos/` | — | `[{ id, description, created_at }, ...]` |
| `POST` | `/todos/` | `{ "description": "..." }` | Created todo (`201`) |

Invalid payloads return `400` with an `error` message.

## Notes

- React uses hooks only (no class components).
- Data is stored in MongoDB only (no Django models / serializers / SQLite for todos).
- Docker image was adjusted for modern Apple Silicon / Bookworm hosts; Mongo runs via the official `mongo:4.4` image while app/api share a lean Python + Node image.
