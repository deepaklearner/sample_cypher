To create a scalable and maintainable FastAPI project with proper naming conventions, we can break it down into the following structure. This will allow different teams to interact with the Neo4j IAM data through Unix-based commands.

We'll have 20+ REST API endpoints, with at least five endpoints outlined in this example. We'll include features for versioning, pagination, and documentation. I'll guide you through the project layout and provide examples of how different teams can interact with it.

### FastAPI Project Structure
```
IAM_FastAPI/
├── app/
│   ├── __init__.py              # FastAPI app initialization
│   ├── main.py                  # Entry point for FastAPI server
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── supervisor.py    # Supervisor-related endpoints
│   │   │   ├── user.py          # User-related endpoints
│   │   │   ├── auth.py          # Authentication-related endpoints
│   │   │   └── utils.py         # Utility functions (e.g., pagination)
│   │   ├── v2/
│   │   │   ├── __init__.py
│   │   │   ├── supervisor.py    # Updated supervisor endpoints for v2
│   │   │   ├── user.py          # Updated user endpoints for v2
│   │   │   └── utils.py         # Updated utility functions for v2
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User schema
│   │   ├── supervisor.py        # Supervisor schema
│   │   └── common.py            # Common models, e.g., pagination
│   ├── services/
│   │   ├── __init__.py
│   │   ├── supervisor_service.py # Logic for supervisor-related queries
│   │   ├── user_service.py      # Logic for user-related queries
│   │   └── neo4j_service.py     # Interactions with Neo4j
│   ├── config/
│   │   └── config.yaml          # Application configuration (Neo4j, server settings)
│   └── requirements.txt         # Dependencies (FastAPI, Neo4j, etc.)
├── scripts/
│   ├── fetch_supervisor_data.sh  # Shell script for fetching supervisor data
│   ├── fetch_user_data.sh        # Shell script for fetching user data
│   └── fetch_auth_data.sh        # Shell script for authentication
├── README.md
└── Dockerfile                   # Docker file for containerization
```

### 1. FastAPI `main.py` Entry Point
```python
from fastapi import FastAPI
from app.api.v1 import supervisor, user, auth

app = FastAPI(
    title="IAM Neo4j API",
    description="API for managing IAM data with Neo4j backend.",
    version="1.0.0"
)

# Include versioned API routes
app.include_router(supervisor.router, prefix="/v1/supervisors", tags=["supervisors"])
app.include_router(user.router, prefix="/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/v1/auth", tags=["authentication"])
```

### 2. Example `supervisor.py` Endpoint (with Pagination)
```python
from fastapi import APIRouter, HTTPException, Query
from app.models.supervisor import Supervisor
from app.services.supervisor_service import get_supervisor_hierarchy
from app.models.common import PaginatedResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[Supervisor])
async def get_supervisor_data(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    """
    Retrieve a paginated list of supervisors in the organization.
    """
    try:
        data, total = await get_supervisor_hierarchy(page, page_size)
        return PaginatedResponse(data=data, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. Example `user.py` Endpoint
```python
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services.user_service import get_user_info

router = APIRouter()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    Retrieve details of a specific user.
    """
    try:
        user = await get_user_info(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 4. Pagination Response Model
```python
from pydantic import BaseModel
from typing import List, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel):
    data: List[T]
    total: int
    page: int
    page_size: int
```

### 5. Service Layer Logic (e.g., `supervisor_service.py`)
```python
from app.services.neo4j_service import query_neo4j
from app.models.supervisor import Supervisor
from typing import List, Tuple

async def get_supervisor_hierarchy(page: int, page_size: int) -> Tuple[List[Supervisor], int]:
    query = """
    MATCH (supervisor:User)-[:MANAGES]->(employee:User)
    RETURN supervisor.employeeNumber AS employee_number,
           supervisor.firstName AS first_name,
           supervisor.lastName AS last_name
    SKIP $skip LIMIT $limit
    """
    skip = (page - 1) * page_size
    result, total = await query_neo4j(query, {"skip": skip, "limit": page_size})
    return [Supervisor(**record) for record in result], total
```

### 6. Neo4j Interaction (`neo4j_service.py`)
```python
from neo4j import AsyncGraphDatabase
from app.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from typing import List, Dict, Any

# Connect to Neo4j
driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

async def query_neo4j(query: str, parameters: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], int]:
    async with driver.session() as session:
        result = await session.run(query, parameters or {})
        data = [record.data() for record in result]
        total = len(data)  # A more efficient total count can be fetched separately
        return data, total
```

### 7. Shell Scripts for Teams (e.g., `fetch_supervisor_data.sh`)
```bash
#!/bin/bash
# Fetch supervisor data from the FastAPI service

API_URL="http://localhost:8000/v1/supervisors"

# Get the first page of supervisor data with a limit of 10 items per page
curl -X 'GET' "$API_URL?page=1&page_size=10" -H 'accept: application/json'
```

### 8. Versioning and API Documentation
The FastAPI project includes automatic versioning via the URL prefix (`/v1/` in this example). FastAPI will also auto-generate API documentation for each version, which can be accessed via:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 9. Example Request (Unix Command)
Teams can use Unix-based commands to interact with the API by using `curl` commands. For example:

- **Fetching supervisor data:**
```bash
curl -X 'GET' 'http://localhost:8000/v1/supervisors?page=1&page_size=10' -H 'accept: application/json'
```

- **Fetching user data by ID:**
```bash
curl -X 'GET' 'http://localhost:8000/v1/users/12345' -H 'accept: application/json'
```

- **Authenticating a user:**
```bash
curl -X 'POST' 'http://localhost:8000/v1/auth/login' -H 'accept: application/json' -d '{"username": "user", "password": "pass"}'
```

### 10. Dependencies (`requirements.txt`)
```
fastapi
uvicorn
neo4j
pydantic
```

### 11. Dockerfile
```dockerfile
FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY ./app /app

# Expose port and start FastAPI server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Summary:
1. The project is organized with a clean structure for scalability and maintainability.
2. Different teams can interact with the Neo4j IAM data via Unix commands using `curl`.
3. The project supports versioning via URL prefixes (e.g., `/v1/`, `/v2/`).
4. Pagination is supported for endpoints that return large datasets.
5. The FastAPI server is containerized with Docker for easy deployment.

