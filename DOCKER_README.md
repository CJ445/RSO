# Docker Setup for RSO

This guide explains how to run the RSO application using Docker containers.

## Prerequisites

- Docker
- Docker Compose

## Docker Configuration

The application consists of three containerized services defined in `docker-compose.yml`:

1. **Frontend** (React): UI for interacting with the scheduler
   - Built using `Dockerfile.frontend`
   - Accessible at http://localhost:3000
   - Communicates with backend via http://localhost:5000

2. **Backend** (Flask): API endpoints for scheduling operations
   - Built using `Dockerfile.backend`
   - Accessible at http://localhost:5000
   - Connects to PostgreSQL database

3. **Database** (PostgreSQL): Stores all application data
   - Built using `Dockerfile.database`
   - Initializes with sample data from `database/setup.sql`
   - Data persists in Docker volume `rso-postgres-data`
   - Uses `database/wait-for-db.py` to ensure backend waits for database readiness

## Project Structure

```
RSO/
├── backend/                # Backend Python code
│   └── requirements.txt    # Python dependencies
├── database/               # Database initialization scripts
│   ├── setup.sql           # Database schema and sample data
│   └── wait-for-db.py      # Database connection helper
├── frontend/               # React frontend code
├── Dockerfile.backend      # Backend container configuration
├── Dockerfile.frontend     # Frontend container configuration
├── Dockerfile.database     # Database container configuration
└── docker-compose.yml      # Multi-service orchestration
```

## How to Run

### First-time Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mdriyaz-a/RSO.git
   cd RSO
   ```

2. Build and start all services:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Subsequent Runs

After the initial setup, you can simply use:
```bash
docker-compose up
```

To run in detached mode (in the background):
```bash
docker-compose up -d
```

To stop all services:
```bash
docker-compose down
```

## Data Persistence

PostgreSQL data is stored in a named Docker volume (`rso-postgres-data`), so your data will persist even if the containers are stopped or removed. The database is automatically initialized with sample data from `database/setup.sql` on first run.

## Environment Variables

The application uses these key environment variables:

- **Frontend**: `REACT_APP_API_URL=http://localhost:5000` (configured for browser communication)
- **Backend**: `FLASK_APP=backend/api.py` (updated for new directory structure)
- **Database**: Standard PostgreSQL configuration with sample data initialization

## Development Mode

For development with live reloading:

1. **Backend**: Volume mount maps `./backend` to `/app/backend` in container
2. **Frontend**: Volume mount enables hot reloading for React development
3. **Database**: Persistent volume ensures data survives container restarts

## Accessing Individual Services

### PostgreSQL Database

```bash
docker exec -it rso-db psql -U postgres -d RSO
```

### Backend Container

```bash
docker exec -it rso-backend /bin/bash
```

### Frontend Container

```bash
docker exec -it rso-frontend /bin/sh
```

## Troubleshooting

### Common Issues

1. **Backend can't connect to database**:
   ```bash
   docker-compose restart backend
   ```

2. **Database initialization failed**:
   ```bash
   docker-compose down -v  # Remove volumes
   docker-compose up --build  # Rebuild and reinitialize
   ```

3. **Frontend can't reach backend API**:
   - Verify `REACT_APP_API_URL=http://localhost:5000` in docker-compose.yml
   - Check that backend container is running: `docker-compose ps`

4. **Port conflicts**:
   - If ports 3000 or 5000 are in use, modify the port mappings in docker-compose.yml

### Viewing Logs

View logs for specific services:
```bash
docker-compose logs frontend
docker-compose logs backend
docker-compose logs db
```

Follow logs in real-time:
```bash
docker-compose logs -f backend
```

### Complete Reset

To completely rebuild everything and start fresh:
```bash
docker-compose down -v    # Stop and remove volumes
docker system prune       # Clean up unused Docker objects
docker-compose up --build # Rebuild and start
```

### Manual Database Access

Connect to PostgreSQL directly:
```bash
docker exec -it rso-db psql -U postgres -d RSO
```

Common queries:
```sql
-- View all tasks
SELECT * FROM tasks;

-- View current schedules
SELECT * FROM schedules;

-- Check database tables
\dt
```
