I'll provide the full code for each file in the FastAPI project based on the existing Neo4j IAM system. Here's the complete code structure:

## 1. src/main.py

```python
from fastapi import FastAPI
from src.api.v1.router import api_router
from src.core.config import settings, config, logger

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_V1_STR)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    logger.info(f"Running in {config['environment']} environment")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 2. src/core/config.py

```python
from pydantic import BaseSettings
from src.utils.helper import read_yaml_file, initialize_main_logger

class Settings(BaseSettings):
    PROJECT_NAME: str = "IAM API"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
config = read_yaml_file('./config/config.yaml')
logger = initialize_main_logger()
```

## 3. src/db/neo4j.py

```python
from neo4j import GraphDatabase
from src.utils.helper import read_creds
from src.core.config import logger

def get_neo4j_db():
    try:
        database_configs = read_creds('./config/config.yaml')
        uri = database_configs['NE04J']['HostURI']
        username = database_configs['NE04J']['Username']
        password = database_configs['NE04J']['Password']
        driver = GraphDatabase.driver(uri, auth=(username, password))
        return driver.session()
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {str(e)}")
        raise
```

## 4. src/api/v1/router.py

```python
from fastapi import APIRouter
from src.api.v1.endpoints import users, roles, permissions, hierarchy, reports

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(hierarchy.router, prefix="/hierarchy", tags=["hierarchy"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
```

## 5. src/api/v1/endpoints/users.py

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from src.db.neo4j import get_neo4j_db
from src.models.pydantic_models import User, UserCreate
from src.core.config import logger
from src.utils.helper import get_memory_usage
from typing import List

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_neo4j_db)
):
    try:
        query = "MATCH (u:User) RETURN u.id, u.name, u.email SKIP $skip LIMIT $limit"
        result = db.run(query, skip=skip, limit=limit)
        users = [User(**record["u"]) for record in result]
        logger.info(f"Retrieved {len(users)} users. Memory usage: {get_memory_usage()} bytes")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db = Depends(get_neo4j_db)):
    try:
        query = "CREATE (u:User {id: $id, name: $name, email: $email}) RETURN u"
        result = db.run(query, id=user.id, name=user.name, email=user.email)
        created_user = User(**result.single()["u"])
        logger.info(f"Created user: {created_user.id}")
        return created_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 6. src/api/v1/endpoints/roles.py

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from src.db.neo4j import get_neo4j_db
from src.models.pydantic_models import Role
from src.core.config import logger
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Role])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_neo4j_db)
):
    try:
        query = "MATCH (r:Role) RETURN r.id, r.name SKIP $skip LIMIT $limit"
        result = db.run(query, skip=skip, limit=limit)
        roles = [Role(**record["r"]) for record in result]
        logger.info(f"Retrieved {len(roles)} roles")
        return roles
    except Exception as e:
        logger.error(f"Error retrieving roles: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 7. src/api/v1/endpoints/permissions.py

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from src.db.neo4j import get_neo4j_db
from src.models.pydantic_models import Permission
from src.core.config import logger
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Permission])
async def get_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_neo4j_db)
):
    try:
        query = "MATCH (p:Permission) RETURN p.id, p.name SKIP $skip LIMIT $limit"
        result = db.run(query, skip=skip, limit=limit)
        permissions = [Permission(**record["p"]) for record in result]
        logger.info(f"Retrieved {len(permissions)} permissions")
        return permissions
    except Exception as e:
        logger.error(f"Error retrieving permissions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 8. src/api/v1/endpoints/hierarchy.py

```python
from fastapi import APIRouter, Depends, HTTPException
from src.db.neo4j import get_neo4j_db
from src.models.pydantic_models import HierarchyNode
from src.core.config import logger
from typing import List

router = APIRouter()

@router.get("/{user_id}", response_model=List[HierarchyNode])
async def get_hierarchy(user_id: str, db = Depends(get_neo4j_db)):
    try:
        query = """
        MATCH (u:User {id: $user_id})-[:REPORTS_TO*]->(m:User)
        RETURN u.id as id, u.name as name, u.title as title, m.id as manager_id
        """
        result = db.run(query, user_id=user_id)
        hierarchy = [HierarchyNode(**record) for record in result]
        logger.info(f"Retrieved hierarchy for user: {user_id}")
        return hierarchy
    except Exception as e:
        logger.error(f"Error retrieving hierarchy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 9. src/api/v1/endpoints/reports.py

```python
from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.core.config import logger
from src.utils.helper import generate_supervisor_hierarchy_report

router = APIRouter()

@router.post("/generate_supervisor_hierarchy")
async def generate_report(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(generate_supervisor_hierarchy_report)
        return {"message": "Report generation started in the background"}
    except Exception as e:
        logger.error(f"Error starting report generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 10. src/models/pydantic_models.py

```python
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class Role(BaseModel):
    id: str
    name: str

class Permission(BaseModel):
    id: str
    name: str

class HierarchyNode(BaseModel):
    id: str
    name: str
    title: str
    manager_id: str
```

## 11. run.sh

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
        call_api "/users" "POST" '{"name": "'$2'", "email": "'$3'"}'
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
    "generate_report")
        call_api "/reports/generate_supervisor_hierarchy" "POST"
        ;;
    *)
        echo "Unknown command. Available commands: get_users, create_user, get_roles, get_permissions, get_hierarchy, generate_report"
        ;;
esac
```

This FastAPI project structure incorporates the existing helper.py and retrieve_azure_creds.py files, implements versioning, includes pagination where appropriate, and provides multiple endpoints accessible via Unix commands. The project is scalable and maintainable, allowing for easy addition of new endpoints and features.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/8978744/5812171a-51b8-4ec1-b6a0-221fe157e53b/paste.txt