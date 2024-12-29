To create a scalable and maintainable FastAPI-based REST API for the **Supervisor Hierarchy** project, we need to define clear endpoints that can interact with Neo4j data, ensure proper API versioning, handle pagination, and facilitate interaction through Unix-based commands.

Let's break down the structure of the REST API project based on your request:

### Project Structure

```plaintext
Supervisor_hierachy_api/
├── app/
│   ├── main.py                # FastAPI app setup and routing
│   ├── api/                   # Folder containing the versioned API endpoints
│   │   ├── v1/                # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py   # Contains endpoint definitions for v1
│   │   │   └── models.py      # Models for request/response validation
│   │   └── v2/                # API version 2 (future versioning)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # App configuration setup
│   ├── services/              # Logic for interacting with Neo4j and other services
│   │   ├── __init__.py
│   │   ├── graph_service.py   # Neo4j related services (for IAM data)
│   │   └── utils.py           # Helper functions (e.g., pagination)
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── helper.py          # Functions used in multiple places (from original helper.py)
│   │   └── retrieve_azure_creds.py  # Azure credentials from your original file
│   └── schemas/               # Pydantic models for request/response validation
│       ├── __init__.py
│       ├── request_models.py  # Request models (filters, pagination, etc.)
│       └── response_models.py # Response models (IAM data)
├── config/
│   ├── config.yaml            # Configuration file
├── requirements.txt           # Dependencies
├── README.md                  # Documentation for developers
├── generate_supervisor_hierachy.sh
└── generate_supervisor_hierachy.py
```

### FastAPI REST API with Pagination and Versioning

#### 1. **API Versioning**
We will version the API using path-based versioning (e.g., `/api/v1/` and `/api/v2/`).

#### 2. **Example Endpoints (5+)**

Here are examples of the 5 endpoints for version 1 (`/api/v1/`):

- **Get Supervisor Hierarchy**: `GET /api/v1/supervisor_hierarchy`
- **Get Supervisor by ID**: `GET /api/v1/supervisor/{id}`
- **Create Supervisor**: `POST /api/v1/supervisor`
- **Update Supervisor**: `PUT /api/v1/supervisor/{id}`
- **Delete Supervisor**: `DELETE /api/v1/supervisor/{id}`

Each endpoint will implement Neo4j operations (using Cypher queries) and return relevant IAM data.

#### 3. **Pagination**
We will implement pagination to fetch data in batches for larger datasets. For example, for the **Get Supervisor Hierarchy** endpoint, you can pass `limit` and `offset` as query parameters.

#### 4. **Unix-based Commands**
You can use Unix-based commands like `curl`, `wget`, or `http` (from the HTTPie tool) to interact with the API. For example:

```bash
# Fetch supervisor hierarchy (page 1 with 10 items per page)
curl "http://localhost:8000/api/v1/supervisor_hierarchy?limit=10&offset=0"

# Fetch supervisor by ID
curl "http://localhost:8000/api/v1/supervisor/1234"
```

### FastAPI Implementation

#### `app/main.py`

```python
from fastapi import FastAPI
from app.api.v1.endpoints import supervisor_hierarchy

app = FastAPI()

# Register versioned API routers
app.include_router(supervisor_hierarchy.router, prefix="/api/v1/supervisor", tags=["supervisor"])
```

#### `app/api/v1/endpoints.py`

```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.graph_service import Neo4jService
from app.schemas.request_models import SupervisorRequest
from app.schemas.response_models import SupervisorResponse

router = APIRouter()

neo4j_service = Neo4jService()

@router.get("/hierarchy", response_model=List[SupervisorResponse])
async def get_supervisor_hierarchy(limit: int = Query(10, le=100), offset: int = Query(0)):
    """
    Get the supervisor hierarchy, with pagination.
    """
    try:
        return await neo4j_service.get_supervisors(limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=SupervisorResponse)
async def get_supervisor(id: int):
    """
    Get a specific supervisor by ID.
    """
    try:
        supervisor = await neo4j_service.get_supervisor_by_id(id)
        if not supervisor:
            raise HTTPException(status_code=404, detail="Supervisor not found")
        return supervisor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=SupervisorResponse)
async def create_supervisor(supervisor: SupervisorRequest):
    """
    Create a new supervisor entry.
    """
    try:
        return await neo4j_service.create_supervisor(supervisor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=SupervisorResponse)
async def update_supervisor(id: int, supervisor: SupervisorRequest):
    """
    Update an existing supervisor by ID.
    """
    try:
        updated_supervisor = await neo4j_service.update_supervisor(id, supervisor)
        if not updated_supervisor:
            raise HTTPException(status_code=404, detail="Supervisor not found")
        return updated_supervisor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_supervisor(id: int):
    """
    Delete a supervisor by ID.
    """
    try:
        result = await neo4j_service.delete_supervisor(id)
        if not result:
            raise HTTPException(status_code=404, detail="Supervisor not found")
        return {"message": "Supervisor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### `app/services/graph_service.py`

```python
from app.helpers.retrieve_azure_creds import read_creds
from neo4j import GraphDatabase
from app.schemas.request_models import SupervisorRequest
from app.schemas.response_models import SupervisorResponse

class Neo4jService:
    def __init__(self):
        # Load Neo4j configurations (host, username, password, etc.)
        self.config = read_creds('./config/config.yaml')
        self.driver = GraphDatabase.driver(self.config['NE04']['HostURI'],
                                           auth=(self.config['NE04']['Username'], self.config['NE04']['Password']))
    
    async def get_supervisors(self, limit: int, offset: int):
        query = f"MATCH (s:Supervisor)-[:MANAGES]->(e:Employee) RETURN s, e SKIP {offset} LIMIT {limit}"
        with self.driver.session() as session:
            result = session.run(query)
            return [SupervisorResponse(s['s']['name'], s['s']['id'], e['e']['name']) for s, e in result]
    
    async def get_supervisor_by_id(self, supervisor_id: int):
        query = f"MATCH (s:Supervisor) WHERE s.id = {supervisor_id} RETURN s"
        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            if record:
                return SupervisorResponse(record['s']['name'], record['s']['id'])
            return None
    
    async def create_supervisor(self, supervisor: SupervisorRequest):
        query = f"CREATE (s:Supervisor {{name: '{supervisor.name}', id: '{supervisor.id}'}})"
        with self.driver.session() as session:
            session.run(query)
            return SupervisorResponse(supervisor.name, supervisor.id)
    
    async def update_supervisor(self, supervisor_id: int, supervisor: SupervisorRequest):
        query = f"MATCH (s:Supervisor) WHERE s.id = {supervisor_id} SET s.name = '{supervisor.name}'"
        with self.driver.session() as session:
            session.run(query)
            return SupervisorResponse(supervisor.name, supervisor.id)
    
    async def delete_supervisor(self, supervisor_id: int):
        query = f"MATCH (s:Supervisor) WHERE s.id = {supervisor_id} DELETE s"
        with self.driver.session() as session:
            result = session.run(query)
            return result.summary().counters.nodes_deleted > 0
```

### API Versioning (for v2)

You can create a new set of endpoints for **v2** in `app/api/v2/endpoints.py` and change the API behaviors, adding more features or enhancements.

### Pagination Helper (`app/helpers/utils.py`)

```python
def paginate(query: str, limit: int, offset: int) -> str:
    return f"{query} SKIP {offset} LIMIT {limit}"
```

### Unix-based Interactions (Example with `curl`)

```bash
# Get supervisor hierarchy with pagination
curl "http://localhost:8000/api/v1/supervisor/hierarchy?limit=10&offset=0"

# Create a new supervisor
curl -X 'POST' \
  'http://localhost:8000/api/v1/supervisor/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "id": 123
}'

# Update supervisor
curl -X 'PUT' \
  'http://localhost:8000/api/v1/supervisor/123' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Updated"
}'

# Delete supervisor
curl -X 'DELETE' 'http://localhost:8000/api/v1/supervisor/123'
```

### Conclusion

This setup uses FastAPI to create a REST API with pagination and versioning, allowing interaction via Unix commands like `curl`. The architecture ensures scalability and maintainability, while also using existing configurations and helpers from the original project.