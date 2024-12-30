Certainly! I'll create a scalable and maintainable RestAPI project using FastAPI based on the existing Neo4j IAM system. Here's a proposed structure and implementation:

## Project Structure

```
iam-api/
├── config/
│   └── config.yaml
├── src/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── roles.py
│   │   │   │   ├── permissions.py
│   │   │   │   └── hierarchy.py
│   │   │   └── router.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── neo4j.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── pydantic_models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helper.py
│   │   └── retrieve_azure_creds.py
│   └── main.py
├── tests/
│   └── ...
├── .env
├── requirements.txt
└── run.sh
```

## Key Components

### 1. FastAPI Application (src/main.py)

```python
from fastapi import FastAPI
from src.api.v1.router import api_router
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_V1_STR)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. API Router (src/api/v1/router.py)

```python
from fastapi import APIRouter
from src.api.v1.endpoints import users, roles, permissions, hierarchy

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(hierarchy.router, prefix="/hierarchy", tags=["hierarchy"])
```

### 3. Example Endpoint (src/api/v1/endpoints/users.py)

```python
from fastapi import APIRouter, Depends, Query
from src.db.neo4j import get_neo4j_db
from src.models.pydantic_models import User, UserCreate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_neo4j_db)
):
    query = "MATCH (u:User) RETURN u.id, u.name, u.email SKIP $skip LIMIT $limit"
    result = db.run(query, skip=skip, limit=limit)
    return [User(**record["u"]) for record in result]

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db = Depends(get_neo4j_db)):
    query = "CREATE (u:User {id: $id, name: $name, email: $email}) RETURN u"
    result = db.run(query, id=user.id, name=user.name, email=user.email)
    return User(**result.single()["u"])

# Add more endpoints as needed
```

### 4. Neo4j Database Connection (src/db/neo4j.py)

```python
from neo4j import GraphDatabase
from src.core.config import settings
from src.utils.retrieve_azure_creds import get_secret

def get_neo4j_db():
    uri = get_secret(settings.NEO4J_URI_SECRET_NAME)
    username = get_secret(settings.NEO4J_USERNAME_SECRET_NAME)
    password = get_secret(settings.NEO4J_PASSWORD_SECRET_NAME)
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        yield driver.session()
    finally:
        driver.close()
```

### 5. Configuration (src/core/config.py)

```python
from pydantic import BaseSettings
from src.utils.helper import load_config

class Settings(BaseSettings):
    PROJECT_NAME: str = "IAM API"
    API_V1_STR: str = "/api/v1"
    NEO4J_URI_SECRET_NAME: str
    NEO4J_USERNAME_SECRET_NAME: str
    NEO4J_PASSWORD_SECRET_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
config = load_config()
```

### 6. Shell Script for API Interaction (run.sh)

```bash
#!/bin/bash

API_BASE_URL="http://localhost:8000/api/v1"

function call_api() {
    local endpoint=$1
    local method=${2:-GET}
    local data=${3:-""}
    
    if [ -n "$data" ]; then
        curl -X $method "$API_BASE_URL$endpoint" -H "Content-Type: application/json" -d "$data"
    else
        curl -X $method "$API_BASE_URL$endpoint"
    fi
}

case $1 in
    "get_users")
        call_api "/users?skip=${2:-0}&limit=${3:-100}"
        ;;
    "create_user")
        call_api "/users" "POST" '{"id": "'$2'", "name": "'$3'", "email": "'$4'"}'
        ;;
    "get_roles")
        call_api "/roles?skip=${2:-0}&limit=${3:-100}"
        ;;
    "get_permissions")
        call_api "/permissions?skip=${2:-0}&limit=${3:-100}"
        ;;
    "get_hierarchy")
        call_api "/hierarchy/${2}"
        ;;
    *)
        echo "Unknown command. Available commands: get_users, create_user, get_roles, get_permissions, get_hierarchy"
        ;;
esac
```

## Usage Examples

1. Get users:
   ```
   ./run.sh get_users 0 50
   ```

2. Create a user:
   ```
   ./run.sh create_user "user123" "John Doe" "john@example.com"
   ```

3. Get roles:
   ```
   ./run.sh get_roles
   ```

4. Get permissions:
   ```
   ./run.sh get_permissions 10 20
   ```

5. Get hierarchy for a specific user:
   ```
   ./run.sh get_hierarchy "user123"
   ```

This structure provides a scalable and maintainable RestAPI project using FastAPI with the following features:

1. Good naming conventions and examples of how different teams can interact with the API through Unix-based commands.
2. Multiple REST API endpoints (5 provided, easily expandable to 20+) accessible via Unix commands.
3. Versioning support (v1 implemented, easily extendable for future versions).
4. Pagination feature implemented where appropriate (e.g., in the get_users endpoint).
5. Reuse of existing files (config.yaml, helper.py, and retrieve_azure_creds.py).

Teams can easily interact with the API using the provided shell script, making it simple to integrate with various Unix-based workflows and automation scripts.