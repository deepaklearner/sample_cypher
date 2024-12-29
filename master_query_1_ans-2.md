To create a scalable and maintainable FastAPI project that includes several API endpoints for interacting with Neo4j IAM data, while also offering features like versioning and pagination, we need to structure the project logically. Below is a suggested project structure, code implementation, and instructions for how different teams can interact with the API via Unix commands.

### Project Structure
```
fastapi-neo4j-iam-api/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point of the FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   ├── supervisor_hierarchy.py  # Endpoints for supervisor hierarchy
│   │   ├── user_management.py      # User-related endpoints
│   │   ├── roles_management.py     # Roles-related endpoints
│   │   ├── permission_management.py # Permissions-related endpoints
│   │   ├── health.py              # Health check endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # Pydantic models for data validation
│   │   ├── supervisor.py
│   │   ├── role.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── neo4j_utils.py         # Helper functions to interact with Neo4j
│   │   ├── config.py              # Configuration handling (e.g., reading from config files)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### FastAPI Code Implementation

#### 1. **`main.py`** - Entry point for FastAPI application
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import supervisor_hierarchy, user_management, roles_management, permission_management, health

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)

# Include all the different routes (endpoints)
app.include_router(supervisor_hierarchy.router, prefix="/api/v1/supervisors", tags=["supervisors"])
app.include_router(user_management.router, prefix="/api/v1/users", tags=["users"])
app.include_router(roles_management.router, prefix="/api/v1/roles", tags=["roles"])
app.include_router(permission_management.router, prefix="/api/v1/permissions", tags=["permissions"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
```

#### 2. **`supervisor_hierarchy.py`** - Example of Supervisor Hierarchy Endpoints
```python
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.supervisor import Supervisor
from app.utils.neo4j_utils import get_supervisors_from_db

router = APIRouter()

# Endpoint to get a list of supervisors
@router.get("/", response_model=List[Supervisor])
async def get_supervisors(offset: int = 0, limit: int = 10):
    try:
        data = get_supervisors_from_db(offset=offset, limit=limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a specific supervisor by their employee ID
@router.get("/{employee_id}", response_model=Supervisor)
async def get_supervisor(employee_id: str):
    try:
        data = get_supervisors_from_db(employee_id=employee_id)
        if not data:
            raise HTTPException(status_code=404, detail="Supervisor not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 3. **`user_management.py`** - Example of User Management Endpoints
```python
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User
from app.utils.neo4j_utils import get_users_from_db

router = APIRouter()

# Endpoint to get all users
@router.get("/", response_model=List[User])
async def get_users(offset: int = 0, limit: int = 10):
    try:
        users = get_users_from_db(offset=offset, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 4. **`neo4j_utils.py`** - Helper functions for interacting with Neo4j
```python
from neo4j import GraphDatabase
from app.utils.config import get_neo4j_config

def get_db_driver():
    config = get_neo4j_config()
    uri = config['uri']
    user = config['user']
    password = config['password']
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def get_supervisors_from_db(offset: int = 0, limit: int = 10, employee_id: Optional[str] = None):
    driver = get_db_driver()
    query = "MATCH (s:Supervisor) RETURN s ORDER BY s.name SKIP $offset LIMIT $limit"
    if employee_id:
        query = "MATCH (s:Supervisor {employee_id: $employee_id}) RETURN s"
    with driver.session() as session:
        result = session.run(query, offset=offset, limit=limit, employee_id=employee_id)
        supervisors = [record['s'] for record in result]
    return supervisors

def get_users_from_db(offset: int = 0, limit: int = 10):
    driver = get_db_driver()
    query = "MATCH (u:User) RETURN u ORDER BY u.name SKIP $offset LIMIT $limit"
    with driver.session() as session:
        result = session.run(query, offset=offset, limit=limit)
        users = [record['u'] for record in result]
    return users
```

#### 5. **Pagination and Versioning**
- **Pagination**: We added `offset` and `limit` parameters in the query to implement pagination.
- **Versioning**: The API routes are versioned with `/api/v1/`, which allows backward compatibility for future versions.

### Models (`models` folder)
You should create Pydantic models to define the structure of data passed and received from the API.

Example (`supervisor.py`):
```python
from pydantic import BaseModel

class Supervisor(BaseModel):
    employee_id: str
    name: str
    manager_id: str
    department: str

    class Config:
        orm_mode = True
```

### Unix-based Interaction via Commands

To interact with this FastAPI application via Unix commands, you can use `curl` or other tools like `http` or `wget`. 

1. **Get Supervisors**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/supervisors/?offset=0&limit=10'
```

2. **Get a specific Supervisor**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/supervisors/EMP001'
```

3. **Get Users**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/users/?offset=0&limit=5'
```

4. **Check Health of API**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/health'
```

### Dockerizing the Application
To make the API easily deployable, you can create a `Dockerfile` and a `docker-compose.yml` to containerize and manage the application.

#### `Dockerfile`
```dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### `docker-compose.yml`
```yaml
version: '3.7'
services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=neo4j://localhost:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
```

### Running the Project
1. **Build and Run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access API**
After the server starts, you can access it via:
```
http://localhost:8000/docs
```

This FastAPI project structure supports scalable and maintainable development practices, allowing various teams to interact with IAM data through Unix-based commands. The API also offers versioning and pagination for large datasets.