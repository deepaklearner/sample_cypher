Requirement
Create a rest api for neo4j using python fast api for 30+ different use cases like read data related to IAM.
It should have below characteristics:
1. It should be asynchronous and cabale to scale 50k requests a sec.
2. Also create a unix shell script to invoke it.
3. suggest good name and folder structure to organize the code for neo4j connection related python to put in util or anything you think better. 
4. Keep environment variables in yaml file inside config folder.

scripts/
├── user_api.sh            # Script for user-related API calls (e.g., create user, update user)
├── role_api.sh            # Script for role-related API calls (e.g., assign role, list roles)
├── permissions_api.sh     # Script for permission-related API calls (e.g., grant permissions)
├── auth_api.sh            # Script for authentication/authorization
└── invoke_all.sh          # (Optional) Script to invoke all APIs sequentially


iam-neo4j-api/
│
├── app/
│   ├── __init__.py              # To mark the app directory as a Python package
│   ├── main.py                  # FastAPI application setup (routes, initialization)
│   ├── models/                  # Folder to store Pydantic models
│   │   └── iam_models.py        # Pydantic models related to IAM (e.g., user, role)
│   ├── db/                      # Database-related logic and utilities
│   │   ├── __init__.py          # To mark the db directory as a Python package
│   │   └── neo4j_utils.py       # Neo4j connection setup, query execution functions
│   ├── api/                     # Folder for storing API route logic
│   │   └── iam_routes.py        # IAM-related FastAPI routes (e.g., user creation, role assignment)
│   ├── services/                # Business logic layer, separate from routes
│   │   └── iam_service.py       # IAM-specific business logic (e.g., checking roles, permissions)
│   ├── config.py                # Configuration for the FastAPI app (e.g., environment variables)
│   └── utils.py                 # Utility functions that don’t fit elsewhere (e.g., data validation, logging)
│
├── scripts/                     # Folder for scripts, such as API testing
│   └── invoke_api.sh            # Shell script to invoke FastAPI endpoints (for testing)
│
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration (optional, if using Docker)
└── README.md                    # Project documentation
