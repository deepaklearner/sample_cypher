can you please create a sample project for me with good naming conventions which is easier to scale and also easier to maintain? also i want the different teams to access this api using unix

Certainly! Below is an example of how to structure a scalable and maintainable FastAPI project with good naming conventions. I’ll guide you through a modular structure, explain how to organize the code for easy scaling, and provide examples of how different teams can interact with the API through Unix-based commands.

### Sample Project Structure

We will use a modular structure where each component is separated by functionality (e.g., user management, access management, roles management). This will make it easier to maintain, test, and scale the application.

#### Project Directory Layout
```
iam-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup and routing
│   ├── models/                 # Neo4j database interaction models
│   │   ├── __init__.py
│   │   ├── user.py             # User-related database operations
│   │   ├── resource.py         # Resource-related database operations
│   │   ├── role.py             # Role-related database operations
│   │   ├── access.py           # Access control (permissions)
│   ├── routes/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── user_routes.py      # Routes for user-related operations
│   │   ├── resource_routes.py  # Routes for resource-related operations
│   │   ├── role_routes.py      # Routes for role-related operations
│   │   ├── access_routes.py    # Routes for access control operations
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py     # Business logic for user operations
│   │   ├── resource_service.py # Business logic for resource operations
│   │   ├── role_service.py     # Business logic for role operations
│   │   ├── access_service.py   # Business logic for access operations
│   ├── utils/                  # Utility functions (e.g., for logging, validation)
│   │   ├── __init__.py
│   │   ├── logger.py           # Custom logging utility
│   │   ├── exceptions.py       # Custom exception handlers
│   ├── config.py               # Configuration settings (e.g., Neo4j URI, credentials)
│   └── requirements.txt        # Python dependencies (e.g., fastapi, neo4j)
├── scripts/                     # Optional Unix scripts
│   ├── setup_neo4j.sh           # Script to set up Neo4j database
│   ├── deploy_api.sh            # Script to deploy FastAPI app
├── .gitignore
└── README.md
```

### 1. **Main FastAPI App (app/main.py)**

This is the entry point of the FastAPI application. It includes the app setup, routes registration, and initialization of dependencies (e.g., Neo4j connection).

```python
from fastapi import FastAPI
from app.routes import user_routes, resource_routes, role_routes, access_routes

app = FastAPI(title="IAM API")

# Registering routes from different modules
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(resource_routes.router, prefix="/resources", tags=["Resources"])
app.include_router(role_routes.router, prefix="/roles", tags=["Roles"])
app.include_router(access_routes.router, prefix="/access", tags=["Access Control"])
```

### 2. **Database Models (app/models/)**

In this directory, we will store the database interaction code using Neo4j's `py2neo` or `neo4j` Python driver.

#### **app/models/user.py**

```python
from neo4j import GraphDatabase

class UserModel:
    def __init__(self, db: GraphDatabase):
        self.db = db

    def get_user(self, user_id: str):
        query = """
        MATCH (u:User {id: $user_id})
        RETURN u
        """
        result = self.db.run(query, user_id=user_id)
        return result.single()

    def create_user(self, user_data: dict):
        query = """
        CREATE (u:User {id: $id, name: $name, email: $email})
        RETURN u
        """
        result = self.db.run(query, **user_data)
        return result.single()
```

#### **app/models/access.py**

```python
class AccessModel:
    def __init__(self, db: GraphDatabase):
        self.db = db

    def assign_access(self, user_id: str, resource_id: str):
        query = """
        MATCH (u:User {id: $user_id}), (r:Resource {id: $resource_id})
        CREATE (u)-[:HAS_ACCESS]->(r)
        RETURN u, r
        """
        self.db.run(query, user_id=user_id, resource_id=resource_id)
        return {"message": "Access granted successfully"}
```

### 3. **Routes (app/routes/)**

This directory contains the FastAPI route definitions. Each module (user, resource, role, access) will have its own route file to handle related requests.

#### **app/routes/user_routes.py**

```python
from fastapi import APIRouter
from app.services.user_service import UserService

router = APIRouter()

user_service = UserService()

@router.post("/")
def create_user(user_data: dict):
    return user_service.create_user(user_data)

@router.get("/{user_id}")
def get_user(user_id: str):
    return user_service.get_user(user_id)
```

#### **app/routes/access_routes.py**

```python
from fastapi import APIRouter
from app.services.access_service import AccessService

router = APIRouter()

access_service = AccessService()

@router.post("/grant")
def grant_access(user_id: str, resource_id: str):
    return access_service.assign_access(user_id, resource_id)
```

### 4. **Services (app/services/)**

The services handle the business logic for user operations, role management, access control, etc.

#### **app/services/user_service.py**

```python
from app.models.user import UserModel

class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def create_user(self, user_data: dict):
        return self.user_model.create_user(user_data)

    def get_user(self, user_id: str):
        return self.user_model.get_user(user_id)
```

#### **app/services/access_service.py**

```python
from app.models.access import AccessModel

class AccessService:
    def __init__(self):
        self.access_model = AccessModel()

    def assign_access(self, user_id: str, resource_id: str):
        return self.access_model.assign_access(user_id, resource_id)
```

### 5. **Configuration (app/config.py)**

Store configuration values like Neo4j connection details and other environment-specific settings.

```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
```

### 6. **Unix Scripts (scripts/)**

You can add custom scripts for deployment and management of the API and database. For example:

#### **scripts/setup_neo4j.sh**
This script could be used to set up the Neo4j database (e.g., start a container, import data, or configure the database).

```bash
#!/bin/bash
# Start Neo4j container
docker run --name neo4j -d -p 7687:7687 -p 7474:7474 --env NEO4J_AUTH=neo4j/password neo4j
echo "Neo4j started!"
```

#### **scripts/deploy_api.sh**

A deployment script to run the FastAPI server on a Unix-based system.

```bash
#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI application using Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. **Requirements (requirements.txt)**

```txt
fastapi
uvicorn
neo4j
python-dotenv
```

### 8. **Git Ignore (.gitignore)**

```txt
*.pyc
__pycache__/
.env
.venv
```

---

### How Teams Can Use the API from Unix

Teams can interact with the API using Unix commands (curl or HTTP client tools like `httpie`). For example:

- **Security and Risk Management Team:**
    - **Check if a user has access to a resource:**
      ```bash
      curl -X 'GET' 'http://localhost:8000/access/check_access/{user_id}/{resource_id}'
      ```

- **IAM Team:**
    - **Grant a user access to a resource:**
      ```bash
      curl -X 'POST' 'http://localhost:8000/access/grant' -d '{
        "user_id": "12345",
        "resource_id": "abc123"
      }'
      ```

- **HR Team:**
    - **Add a new user:**
      ```bash
      curl -X 'POST' 'http://localhost:8000/users' -d '{
        "id": "12345",
        "name": "John Doe",
        "email": "john.doe@example.com"
      }'
      ```

### Conclusion

This project structure follows best practices by modularizing the code into specific areas (models, routes, services) and includes easy-to-understand naming conventions. The inclusion of Unix-based scripts makes it simple for different teams to interact with the API directly from the terminal. This setup ensures that the project is scalable, maintainable, and easy to deploy.