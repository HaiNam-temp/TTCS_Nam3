Run Project With Docker

Current structure summary:
- Backend entrypoint: backend/main.py
- Backend image file: backend/Dockerfile
- Backend dependencies: backend/requirements.txt
- Frontend: frontend (React + Vite)
- Database: Postgres (service name: postgres, host port: 5444)

Start all services:

    docker compose up --build

Services and ports:
- backend API: http://localhost:8010
- frontend app: http://localhost:3000
- postgres: localhost:5444 (container 5432)

Stop services:

    docker compose down

Backend container command (in compose):

    uvicorn backend.main:app --host 0.0.0.0 --port 8010

Useful commands:

    docker compose logs -f app
    docker compose logs -f frontend
    docker compose exec app sh

Notes:
- Backend Dockerfile path is set in docker-compose.yml as backend/Dockerfile.
- Python dependencies for backend are installed from backend/requirements.txt.
