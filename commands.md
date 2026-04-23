# Project Commands Cheat Sheet

This file documents all the essential commands required for managing and developing both the backend and frontend of this project.

## 📂 1. Directory Structure Command
To view the structure of the project without ignoring `.gitignore` paths, use `tree`. If you want to skip `node_modules`, `.next`, and Python virtual environments:
```bash
# View project tree excluding node_modules and other irrelevant folders
tree -I 'node_modules|.next|__pycache__|.git|.venv'
```

---

## 🐘 2. ORM Commands (Backend: SQLModel + Alembic)
The backend uses **SQLModel**. Although currently the tables are generated using `SQLModel.metadata.create_all(engine)`, it is recommended to use **Alembic** for migrations when the database schema changes over time. 

*(Note: SQLModel does not require an "ORM client generation" command like Prisma does. It uses Python models natively.)*

```bash
# Initialize Alembic (only needed once to create the alembic directory)
cd backend && alembic init alembic

# Create a new migration script (run this when you change something in app/models.py)
alembic revision --autogenerate -m "description_of_change"

# Apply all pending migrations to update the database schema
alembic upgrade head

# Revert the last migration step
alembic downgrade -1
```

If you wish to use **Prisma Python** or **openapi-ts** for frontend client generation later, those commands would look like this:
```bash
# Example: If you are using openapi-ts to generate frontend API client from FastAPI
npm run generate-client
```

---

## 🐳 3. Docker Commands
Docker and Docker Compose are used to run the frontend and backend services together smoothly. Make sure your Docker daemon is running before executing these.

```bash
# Build and start all containers in the background (detached mode)
docker compose up -d --build

# Start all containers without rebuilding them (attached, so you see logs)
docker compose up

# View real-time logs for all running containers
docker compose logs -f

# View logs for a specific service (e.g., backend or frontend)
docker compose logs -f backend

# Stop the running containers (does not remove them or the network)
docker compose stop

# Stop the running containers AND remove containers, networks, and anonymous volumes
docker compose down

# Stop the containers and remove everything, INCLUDING persistent database volumes
docker compose down -v
```

---

## 4. Backend Lint + Type Commands (FastAPI)

### Check lint errors (Ruff):

```bash
docker compose exec backend ruff check app/
```

### Fix lint errors automatically (Ruff):

```bash
docker compose exec backend ruff check app/ --fix
```

### Check formatting errors (Black):

```bash
docker compose exec backend black --check app/
```

### Fix formatting errors automatically (Black):

```bash
docker compose exec backend black app/
```

### Check type errors (mypy):

```bash
docker compose exec backend mypy app/
```

Type errors cannot be auto-fixed — mypy tells you what is wrong and you fix them manually.

### Run all three in order (recommended before every push):

```bash
docker compose exec backend black app/
docker compose exec backend ruff check app/ --fix
docker compose exec backend mypy app/
```

## 5. Frontend Lint + Type Commands (Next.js)

### Check lint errors (ESLint):

```bash
docker compose exec frontend npm run lint
```

### Fix lint errors automatically (ESLint):

```bash
docker compose exec frontend npm run lint -- --fix
```

### Check formatting errors (Prettier):

```bash
docker compose exec frontend npx prettier --check src/
```

### Fix formatting errors automatically (Prettier):

```bash
docker compose exec frontend npx prettier --write src/
```

### Check type errors (TypeScript):

```bash
docker compose exec frontend npx tsc --noEmit
```

Type errors cannot be auto-fixed — tsc tells you what is wrong and you fix them manually.

### Run all three in order (recommended before every push):

```bash
docker compose exec frontend npx prettier --write src/
docker compose exec frontend npm run lint -- --fix
docker compose exec frontend npx tsc --noEmit
```

---

## 🚀 5. Manual Running (Without Docker)

### Backend (FastAPI)
```bash
cd backend
# Starts the server with live reloading
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
# Starts the Next.js dev server
npm run dev
```
