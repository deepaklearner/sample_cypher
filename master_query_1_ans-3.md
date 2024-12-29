To create a scalable and maintainable FastAPI project with proper naming conventions, we will structure it in a modular way, supporting multiple endpoints (including supervisor hierarchy), versioning, pagination, and Unix-based commands. Below is a detailed breakdown of how the project can be structured, followed by the FastAPI implementation.

### Project Structure

```
fastapi_iam_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── supervisor_hierarchy.py
│   │   │   ├── users.py
│   │   │   ├── roles.py
│   │   │   └── permissions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   └── permission.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── neo4j_service.py
│   │   └── report_service.py
│   ├── config.py
│   ├── utils.py
│   └── logging_config.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### 1. FastAPI Implementation

We'll start by defining the FastAPI app, adding versioning, pagination, and multiple endpoints.

#### app/main.py

```python
from fastapi import FastAPI
from app.api.v1 import supervisor_hierarchy, users, roles, permissions
from app.config import settings

app = FastAPI(title="IAM API", version="1.0")

# Registering routes
app.include_router(supervisor_hierarchy.router, prefix="/v1/supervisor_hierarchy", tags=["Supervisor Hierarchy"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(roles.router, prefix="/v1/roles", tags=["Roles"])
app.include_router(permissions.router, prefix="/v1/permissions", tags=["Permissions"])

@app.get("/")
async def root():
    return {"message": "Welcome to IAM API"}
```

#### app/api/v1/supervisor_hierarchy.py

This file contains the supervisor hierarchy endpoint, with pagination and a sample query to interact with Neo4j.

```python
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.services.neo4j_service import get_supervisor_hierarchy

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_supervisor_hierarchy_data(
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, le=100),
    department: Optional[str] = None
):
    """
    Get a paginated list of supervisor hierarchy.
    - `offset`: Starting point for pagination.
    - `limit`: Number of records to fetch.
    - `department`: Optional filter by department.
    """
    try:
        result = await get_supervisor_hierarchy(offset=offset, limit=limit, department=department)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### app/services/neo4j_service.py

This service handles interactions with the Neo4j database. It includes a function to fetch supervisor hierarchy with pagination.

```python
from neo4j import GraphDatabase
from app.config import settings

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
        )

    async def get_supervisor_hierarchy(self, offset: int, limit: int, department: str = None):
        query = """
        MATCH (n:User)-[:REPORTS_TO]->(m:User)
        WHERE n.managerid IS NOT NULL
        """
        if department:
            query += f" AND n.department = '{department}'"
        query += " RETURN n, m SKIP $offset LIMIT $limit"
        
        with self.driver.session() as session:
            result = session.run(query, offset=offset, limit=limit)
            return [record.data() for record in result]

neo4j_service = Neo4jService()

async def get_supervisor_hierarchy(offset: int, limit: int, department: str = None):
    return await neo4j_service.get_supervisor_hierarchy(offset, limit, department)
```

#### app/api/v1/users.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/all")
async def get_all_users():
    return {"message": "Returning all users"}
```

#### app/api/v1/roles.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/all")
async def get_all_roles():
    return {"message": "Returning all roles"}
```

#### app/api/v1/permissions.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/all")
async def get_all_permissions():
    return {"message": "Returning all permissions"}
```

### 2. Pagination Support

We’re already using pagination for the supervisor hierarchy endpoint, where `offset` and `limit` are provided as query parameters. This allows teams to request large datasets in chunks, ensuring the API is scalable and responsive.

### 3. Versioning

API versioning is handled via FastAPI’s `prefix` option in `include_router` to ensure different versions of the API are accessible through URLs like `/v1/...`.

### 4. Configuration Settings

Create a configuration file `app/config.py` to hold environment-specific variables like the Neo4j connection URI.

#### app/config.py

```python
import os

class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")

settings = Settings()
```

### 5. Unix-based Commands

To interact with the FastAPI application via Unix-based commands, we can use `curl` or `wget` commands from the terminal.

**Examples of interacting with the API:**

1. **Get Supervisor Hierarchy with Pagination**:

```bash
curl -X 'GET' 'http://localhost:8000/v1/supervisor_hierarchy?offset=0&limit=10'
```

2. **Get All Users**:

```bash
curl -X 'GET' 'http://localhost:8000/v1/users/all'
```

3. **Get All Roles**:

```bash
curl -X 'GET' 'http://localhost:8000/v1/roles/all'
```

4. **Get All Permissions**:

```bash
curl -X 'GET' 'http://localhost:8000/v1/permissions/all'
```

5. **Supervisor Hierarchy with Department Filter**:

```bash
curl -X 'GET' 'http://localhost:8000/v1/supervisor_hierarchy?offset=0&limit=10&department=HR'
```

### 6. Dockerfile (Optional)

For containerization and deployment, you can use a `Dockerfile` to package the FastAPI application.

```dockerfile
# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app/

# Expose the API port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7. Requirements (Optional)

In the `requirements.txt`, add the dependencies like FastAPI, Neo4j driver, and Uvicorn.

```
fastapi
uvicorn
neo4j
```

### 8. README.md (Optional)

Provide documentation on how to set up and run the project, along with how different teams can interact with the endpoints.

```markdown
# IAM FastAPI Project

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn app.main:app --reload`

## Endpoints

### GET /v1/supervisor_hierarchy

#### Query Parameters:
- `offset`: Integer (default 0)
- `limit`: Integer (default 10)
- `department`: String (optional)

### GET /v1/users/all
### GET /v1/roles/all
### GET /v1/permissions/all
```

### Conclusion

With this setup, the FastAPI project is scalable, versioned, and supports interactions through Unix-based commands. It also allows pagination for large data queries, and is ready for future growth with new endpoints for different IAM functionalities.