Below is the full code for each file in the project structure.

### **Project Structure**
```
iam_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   └── supervisors.py
│   │   ├── v2/
│   │   │   ├── __init__.py
│   │   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── supervisor.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── neo4j_service.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── pagination.py
├── requirements.txt
└── run.sh
```

---

### **1. `app/__init__.py`**
This file can be empty, it just marks the directory as a package.

```python
# Empty, marks directory as a package
```

### **2. `app/main.py`**

```python
from fastapi import FastAPI
from app.api.v1 import users, supervisors
from app.api.v2 import users as users_v2

app = FastAPI()

# Registering API version 1 routes
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(supervisors.router, prefix="/v1/supervisors", tags=["Supervisors"])

# Registering API version 2 routes
app.include_router(users_v2.router, prefix="/v2/users", tags=["Users"])
```

### **3. `app/api/__init__.py`**

This file can be empty as well.

```python
# Empty, marks directory as a package
```

---

### **4. `app/api/v1/users.py`**

```python
from fastapi import APIRouter, Query
from app.services.neo4j_service import Neo4jService
from app.utils.pagination import Pagination

router = APIRouter()

@router.get("/")
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    neo4j_service = Neo4jService()
    users_data = neo4j_service.get_users(page, per_page)
    return Pagination.create_paginated_response(users_data, page, per_page)
```

### **5. `app/api/v1/supervisors.py`**

```python
from fastapi import APIRouter, Query
from app.services.neo4j_service import Neo4jService
from app.utils.pagination import Pagination

router = APIRouter()

@router.get("/")
async def get_supervisors(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    neo4j_service = Neo4jService()
    supervisors_data = neo4j_service.get_supervisors(page, per_page)
    return Pagination.create_paginated_response(supervisors_data, page, per_page)
```

### **6. `app/api/v2/users.py`**

```python
from fastapi import APIRouter, Query
from app.services.neo4j_service import Neo4jService
from app.utils.pagination import Pagination

router = APIRouter()

@router.get("/")
async def get_users_v2(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    neo4j_service = Neo4jService()
    users_data = neo4j_service.get_users(page, per_page)
    return Pagination.create_paginated_response(users_data, page, per_page)
```

---

### **7. `app/models/__init__.py`**

This file can be empty as well.

```python
# Empty, marks directory as a package
```

---

### **8. `app/models/user.py`**

```python
# Define the User model (it can be used in future)
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
```

### **9. `app/models/supervisor.py`**

```python
# Define the Supervisor model (it can be used in future)
class Supervisor:
    def __init__(self, name: str, department: str):
        self.name = name
        self.department = department
```

---

### **10. `app/services/__init__.py`**

This file can be empty as well.

```python
# Empty, marks directory as a package
```

---

### **11. `app/services/neo4j_service.py`**

```python
from neo4j import GraphDatabase
from typing import List, Dict

class Neo4jService:
    def __init__(self):
        self.uri = "neo4j://localhost:7687"  # URI to the Neo4j instance
        self.driver = GraphDatabase.driver(self.uri, auth=("neo4j", "password"))

    def get_users(self, page: int, per_page: int) -> List[Dict]:
        query = f"""
        MATCH (u:User) 
        RETURN u
        SKIP { (page - 1) * per_page } 
        LIMIT { per_page }
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"user": record["u"]} for record in result]

    def get_supervisors(self, page: int, per_page: int) -> List[Dict]:
        query = f"""
        MATCH (s:Supervisor) 
        RETURN s
        SKIP { (page - 1) * per_page } 
        LIMIT { per_page }
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"supervisor": record["s"]} for record in result]
```

---

### **12. `app/utils/__init__.py`**

This file can be empty as well.

```python
# Empty, marks directory as a package
```

---

### **13. `app/utils/config.py**

```python
# This file will be used to handle app-specific configuration settings in the future.
# For now, it's empty.
```

---

### **14. `app/utils/pagination.py`**

```python
from typing import List, Dict

class Pagination:
    @staticmethod
    def create_paginated_response(data: List[Dict], page: int, per_page: int):
        total_records = len(data)
        total_pages = (total_records + per_page - 1) // per_page  # Calculate total pages
        return {
            "page": page,
            "per_page": per_page,
            "total_records": total_records,
            "total_pages": total_pages,
            "data": data[(page - 1) * per_page : page * per_page]  # Paginated data slice
        }
```

---

### **15. `requirements.txt`**

```
fastapi==0.98.0
uvicorn==0.22.0
neo4j==5.5.0
```

---

### **16. `run.sh`**

```bash
#!/bin/bash

# Base URL of the FastAPI application
BASE_URL="http://localhost:8000"

# Get users (API v1)
get_users() {
  curl -X 'GET' \
    "$BASE_URL/v1/users/?page=$1&per_page=$2" \
    -H 'accept: application/json'
}

# Get supervisors (API v1)
get_supervisors() {
  curl -X 'GET' \
    "$BASE_URL/v1/supervisors/?page=$1&per_page=$2" \
    -H 'accept: application/json'
}

# Check FastAPI server status
check_status() {
  curl -X 'GET' "$BASE_URL/" -H 'accept: application/json'
}

# Example usage: Call a specific function
if [ "$1" == "get_users" ]; then
  get_users $2 $3
elif [ "$1" == "get_supervisors" ]; then
  get_supervisors $2 $3
elif [ "$1" == "status" ]; then
  check_status
else
  echo "Usage: ./run.sh get_users <page> <per_page>"
  echo "       ./run.sh get_supervisors <page> <per_page>"
  echo "       ./run.sh status"
fi
```

---

### **Running the Application**

1. **Install Dependencies**:
   Run `pip install -r requirements.txt` to install the required Python packages.

2. **Run Neo4j Instance**:
   Ensure that you have Neo4j running and accessible at `localhost:7687` (or update the URI in `neo4j_service.py` if different).

3. **Start FastAPI Server**:
   To run the FastAPI server, use the following command:

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Make Unix-Based API Calls**:

   - **To Get Users**:
     ```bash
     ./run.sh get_users 1 10
     ```
     This will return a paginated list of users.

   - **To Get Supervisors**:
     ```bash
     ./run.sh get_supervisors 1 10
     ```
     This will return a paginated list of supervisors.

   - **To Check Server Status**:
     ```bash
     ./run.sh status
     ```

### **Extending the Application**

- You can extend the application by adding more routes and modifying the Neo4j queries.
- Future versions of the API can be added by creating new versioned directories and updating `main.py` to include them.
- Add authentication and logging as needed.